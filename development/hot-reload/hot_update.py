#!/usr/bin/env python3
"""Install a newer signed APK and verify that one already running host applied it."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

PROCESS = re.compile(r"[A-Za-z][A-Za-z0-9_.]*(?::[A-Za-z0-9_.]+)?\Z")
APK_PACKAGE = re.compile(r"^package: name='([^']+)' versionCode='(\d+)'", re.M)
SUPPORTED = {"api102", "signed-code"}


def run(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT, timeout=90)


def read_catalog(path):
    entries = json.loads(path.read_text())["apps"]
    return {entry["repo"]: entry for entry in entries}


def find_tools():
    sdk = Path(os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
               or Path.home() / "Library/Android/sdk")
    directory = sdk / "build-tools"
    versions = [item for item in directory.iterdir() if re.fullmatch(r"\d+(\.\d+)*", item.name)]
    if not versions:
        raise ValueError("Android SDK build-tools are required")
    builds = max(versions, key=lambda item: tuple(map(int, item.name.split("."))))
    return sdk / "platform-tools/adb", builds / "aapt2", builds / "apksigner"


def process_id(adb, host):
    try:
        result = adb("shell", "pidof", host).split()
    except subprocess.CalledProcessError as error:
        if error.returncode == 1 and not error.output.strip():
            raise ValueError(f"{host} is not running") from error
        raise
    if len(result) != 1 or not result[0].isdecimal():
        raise ValueError(f"Expected one running process for {host}, found {result}")
    return result[0]


def installed_version(adb, package):
    data = adb("shell", "dumpsys", "package", package)
    match = re.search(r"^\s+versionCode=(\d+)\b", data, re.M)
    if not match:
        raise ValueError(f"{package} is not installed")
    return int(match[1])


def saw_update(log, marker, version, pid, package=None):
    name = rf" package={re.escape(package)}" if package else ""
    prefix = rf"\b{re.escape(marker)}{name} version={version}\s+pid={pid}\b"
    return re.search(prefix, log) is not None


def apply_update(args, packages, modes):
    info = modes[args.repository]
    host = args.host or (info.get("hosts") or [None])[0]
    if info["mode"] not in SUPPORTED:
        raise ValueError(f"{args.repository} has no managed live-update path")
    if not host or not PROCESS.fullmatch(host) or host in {"zygote", "zygote64", "system"}:
        raise ValueError("Select an exact running host with --host")
    if args.timeout < 1:
        raise ValueError("--timeout must be positive")
    if info.get("hostBase") and host.split(":", 1)[0] != info["hostBase"]:
        raise ValueError(f"Host must be a process of {info['hostBase']}")
    listed_host = host in info["hosts"]
    if host == "system_server" and not listed_host:
        raise ValueError("This module has no system_server update path")
    extra_host = bool(args.host) and (
        info.get("allowExplicitHost", False) or host.split(":", 1)[0] in info.get("hostBases", [])
    )
    if info["hosts"] and not listed_host and not extra_host:
        raise ValueError(f"Supported hosts: {', '.join(info['hosts'])}")
    apk = args.apk.resolve(strict=True)
    adb_bin, aapt, signer = find_tools()
    app = packages[args.repository]
    package = app["packageName"]

    def adb(*command):
        return run(adb_bin, "-s", args.serial, *command)

    signature = run(signer, "verify", "--print-certs", apk)
    digests = set(re.findall(r"(?im)certificate sha-256 digest:\s*([a-f0-9]{64})", signature.lower()))
    if len(digests) != 1 or not digests <= set(app["certificates"]):
        raise ValueError("APK signer does not match the OneUI Mods catalog")
    identity = APK_PACKAGE.search(run(aapt, "dump", "badging", apk))
    if identity is None or identity[1] != package:
        raise ValueError(f"APK package must be {package}")
    version = int(identity[2])
    current = installed_version(adb, package)
    minimum = info.get("hostMinimum", {}).get(host)
    if minimum is None:
        minimum = info["minimum"] if listed_host else info.get("explicitHostMinimum", info["minimum"])
    if current < minimum:
        raise ValueError(f"Install and load a baseline of versionCode {minimum}+ first")
    if version <= current:
        raise ValueError(f"APK versionCode {version} must exceed the installed versionCode {current}")
    pid = process_id(adb, host)
    # Discard buffered messages from before the requested install without clearing device logs.
    since = adb("shell", "date", "+%m-%d_%H:%M:%S").strip().replace("_", " ")
    if not re.fullmatch(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}", since):
        raise ValueError("Could not determine the device's log timestamp")
    print(f"Installing {package} {current} → {version}, watching {host} PID {pid}", flush=True)
    # APKs on IncFS may be invisible to the already running Vector daemon.
    print(adb("install", "--no-incremental", "--user", "0", "-r", str(apk)).strip())
    if installed_version(adb, package) != version:
        raise ValueError("Installed version did not change to the requested version")
    owner = package if info["marker"] == "ONEUI_MODS_HOT_RELOAD" else None
    deadline = time.monotonic() + args.timeout
    while True:
        if process_id(adb, host) != pid:
            raise ValueError("APK installed, but the host restarted")
        log = adb("logcat", "-d", "-T", since + ".000", "--pid", pid, "-v", "raw")
        if saw_update(log, info["marker"], version, pid, owner):
            if process_id(adb, host) != pid:
                raise ValueError("APK installed, but the host restarted after applying the update")
            print(f"Live update confirmed: {host} stayed at PID {pid}, versionCode {version}")
            return
        if time.monotonic() >= deadline:
            raise ValueError("APK installed, but the running process did not confirm it applied the new code")
        time.sleep(1)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path,
                        default=here.parents[2] / "OneUIModsManager/catalog/apps.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="check catalog coverage and list the current update path")
    apply = commands.add_parser("apply", help="install and verify on the explicitly selected device")
    apply.add_argument("repository")
    apply.add_argument("apk", type=Path)
    apply.add_argument("--serial", required=True)
    apply.add_argument("--host")
    apply.add_argument("--timeout", type=int, default=25)
    args = parser.parse_args()

    try:
        packages = read_catalog(args.catalog)
        modes = json.loads((here / "apps.json").read_text())
        if set(packages) != set(modes):
            raise ValueError(f"Catalog coverage changed: {', '.join(sorted(set(packages) ^ set(modes)))}")
        if args.command == "list":
            for repo, info in modes.items():
                print(f"{repo:<29} {info['mode']:<12} {info.get('owner', '')}")
            print(f"{len(modes)} entries")
        else:
            apply_update(args, packages, modes)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print(f"Live update not confirmed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.output:
            print(error.output.strip(), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
