# OneUI Mods

[日本語](https://github.com/OneUI-Mods/.github/blob/main/profile/README.md) · English

Unofficial customization apps and modules for Samsung Galaxy / One UI. Choose the apps you need for the home screen, status bar, camera, capture, connectivity, and diagnostics.

[Manage the apps](https://github.com/OneUI-Mods/OneUIModsManager/releases/latest) · [Get them through F-Droid](https://oneui-mods.github.io/fdroid/) · [All repositories](https://github.com/orgs/OneUI-Mods/repositories)

[Developer hot updates and coverage](../development/hot-reload/README.en.md)

## Getting started

[OneUI Mods Manager](https://github.com/OneUI-Mods/OneUIModsManager) shows the app catalog, installation status, and each repository's GitHub Releases. It supports stable and prerelease channels, release notes, APK downloads, and updates. The manager itself does not require root or Vector.

To install an app individually, check its README for requirements and setup instructions, then download its signed release APK from Releases.

## Home screen and appearance

| App | What it does |
| --- | --- |
| [Galaxy Adaptive Bar](https://github.com/OneUI-Mods/galaxy-adaptive-statusbar) | Background-aware status-bar colors and animations |
| [One UI Home Tweaks](https://github.com/OneUI-Mods/OneUIHomeTweaks) | Adjustments to the home screen, recent apps, Quick Panel, and Settings |
| [Dark App Tools](https://github.com/OneUI-Mods/DarkAppTools) | Dark appearance for Sesame and povo |

## Camera and capture

| App | What it does |
| --- | --- |
| [Galaxy Camera Tools](https://github.com/OneUI-Mods/GalaxyCameraTools) | Features for Samsung Camera, Camera Assistant, and Expert RAW |
| [Galaxy Capture Tools](https://github.com/OneUI-Mods/GalaxyCaptureTools) | Extensions to screen recording and screenshots |
| [Galaxy Shutter Mute Manager](https://github.com/OneUI-Mods/galaxy-shutter-mute-manager) | Manage shutter-sound settings |
| [Galaxy Shutter Mute](https://github.com/OneUI-Mods/galaxy-shutter-mute) | Adjust the camera shutter sound |

## Connectivity and sharing

| App | What it does |
| --- | --- |
| [Tail ADB](https://github.com/OneUI-Mods/tail-adb) | ADB connections over Tailscale |
| [Secure Folder Bridge](https://github.com/OneUI-Mods/secure-folder-bridge) | Read and write Secure Folder files through normal and work-profile file managers |
| [HomePod Bridge](https://github.com/OneUI-Mods/HomePodBridge) | Send audio from Galaxy's media output picker to HomePod / HomePod mini |
| [SIM Pilot](https://github.com/OneUI-Mods/sim-pilot) | Assist mobile-data switching between two SIMs |

## Device tools and diagnostics

| App | What it does |
| --- | --- |
| [Galaxy Charge Monitor](https://github.com/OneUI-Mods/GalaxyChargeMonitor) | Read-only monitoring of charging state, thermal limits, and charging settings |
| [Galaxy Game Monitor](https://github.com/OneUI-Mods/GalaxyGameMonitor) | Switch Game Booster’s CPU and GPU readings to peak-clock-relative load |
| [Galaxy DIAG](https://github.com/OneUI-Mods/galaxy-diag) | Prepare modem measurement and diagnostic connectivity |
| [Galaxy Service Panel](https://github.com/OneUI-Mods/galaxy-service-panel) | Organize Samsung Service Mode information |
| [Galaxy Update Guard](https://github.com/OneUI-Mods/galaxy-update-guard) | Disable and restore Galaxy OS updates |
| [Galaxy Reload](https://github.com/OneUI-Mods/galaxy-reload) | Reload SystemUI |
| [SleepStore](https://github.com/OneUI-Mods/SleepStore) | Help stores show updates for deep-sleeping apps |

## Battery use and compatibility

| App | What it does |
| --- | --- |
| [Accessibility Keeper](https://github.com/OneUI-Mods/accessibility-keeper) | Keep accessibility permission after a force stop |
| [App Battery Tools](https://github.com/OneUI-Mods/app-battery-tools) | Reduce unnecessary battery use in supported apps |
| [Legacy Game Tools](https://github.com/OneUI-Mods/legacy-game-tools) | Improve startup compatibility for supported old game trials |
| [Rain Compatibility Tools](https://github.com/OneUI-Mods/rain-compatibility-tools) | Diagnose Rain startup failures and retry missing activity resources |

## Distribution and requirements

- **GitHub Releases:** each app publishes its release notes and signed release APKs.
- **OneUI Mods Manager:** fetches the [public catalog](https://github.com/OneUI-Mods/OneUIModsManager/blob/main/catalog/apps.json) and checks each repository's releases directly.
- **Dedicated F-Droid repository:** see [setup instructions and available apps](https://oneui-mods.github.io/fdroid/). This distribution source is separate from inclusion in official F-Droid.

New APKs generally require Android 17 (API 37) or later. OneUI Mods Manager, Galaxy Shutter Mute and its dedicated Manager, Galaxy Service Panel, SleepStore, Tail ADB, SIM Pilot, and Simeji Clean retain their previous requirements. Check each app's README for supported devices and setup requirements such as root, Vector, or Shizuku.

## Issues and development

Report bugs and feature suggestions in the relevant repository's Issues. Include the app version, device model, Android / One UI version, and reproduction steps when available.

Source and licenses are published in each repository. For build instructions, implementation details, and validation, see each app's developer documentation.

Developed and maintained by ryuya0124. This is an unofficial project, unaffiliated with Samsung.
