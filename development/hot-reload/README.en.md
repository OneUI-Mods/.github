# OneUI Mods live updates

[日本語](README.md)

[The update matrix](apps.json) tracks every package in OneUI Mods Manager. Each app builds and updates independently. The matrix records partial coverage when only one feature or host can update live.

## Verify an update

Load a supported baseline in the target process once. Build a new APK with a higher version code and the existing release signer. Keep the target process running and execute the following from the OneUI Mods workspace.

```sh
python3 .github/development/hot-reload/hot_update.py list
python3 .github/development/hot-reload/hot_update.py apply GalaxyGameMonitor app-release.apk --serial SERIAL
```

Use `--host` when the app supports multiple or user-selected host processes. The command verifies the catalog signer, APK identity, version, and the selected host's PID. Success requires the host to log the new generation without changing PID. The command reports failure if it cannot observe the transition.

## Build a new module or feature

- Use one libxposed API 102 entry. Use the same hook registration path for initial load and hot reload. Use stable hook IDs and detach obsolete hooks after registering the new ones. [Module lifecycle](https://libxposed.github.io/api/io/github/libxposed/api/XposedModuleInterface.html)
- Keep startup and reconnection separate. Identify which component owns observers, workers, timers, views, Binder, and native state. Transfer only classloader-neutral state and stop resources owned by the previous generation. Decline an update while a session cannot be handed off safely.
- Log `ONEUI_MODS_HOT_RELOAD package=<applicationId> version=<versionCode> pid=<PID>` after applying the new logic. Test repeated edits, changed hook targets, rejected updates, and continued use of the active feature. [API 102 entry example](HookEntry.example.kt)
- When the whole hook module needs a stable lifecycle, signed, typed code can still update an isolated feature such as a drawing policy. Keep Android resources and long-lived state in the host. [Signed logic loader example](SignedLogic.example.kt)
- For the apps' own running debug variants, Android Studio can apply supported changes in place. Structural edits, OS startup hooks, and native libraries may require a different deployment path. Keep session ownership separate from replaceable logic in new persistent services. [Android Studio Apply Changes](https://developer.android.com/studio/run#apply-changes)

## Migration verification

An `api102` entry means the listed processes implement the API 102 callbacks. It is not an app-wide guarantee or a report of validation on a Galaxy. Each host needs to load a supported baseline once through its normal lifecycle. If a host defers an update while busy, the module can request it again through the API 102 service once the host is idle.

| App | Current boundary |
| --- | --- |
| One UI Home Tweaks | API 102 for SystemUI, launcher, Developer options, wallpaper preview and the `system_server` focus backend. A generation that exported the legacy focus Binder defers reload. |
| Galaxy Glass Tools | API 102 for SystemUI, launcher, Samsung Capture, helper processes and scoped system apps. Live Compose modifiers keep a resident draw callback with a replaceable delegate. |
| Galaxy Capture Tools | API 102 for SystemUI, Samsung Capture, screenshot workers and `system_server`. Existing captures and unexpired target selection defer reload. |
| HomePod Bridge | API 102 for SystemUI when routing and capture are idle. The dedicated HAL uses its existing startup lifecycle. |
| Legacy Game Tools | Kotlin changes can reload when the native library is byte-for-byte unchanged. JNI changes take effect at the next game start. |
| Rain Compatibility Tools | Replacement resource recovery runs from the signed companion APK. The embedded LSPatch API 93 hook registration is resident and changes at the next startup. |

Completion requires two consecutive updates in each supported host, unchanged process IDs, and a functional check after the update. For hosts that defer while busy, also verify that refusal preserves the active workload and that retrying when idle succeeds.
