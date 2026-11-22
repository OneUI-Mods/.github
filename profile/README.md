# OneUI Mods

[日本語](https://github.com/OneUI-Mods/.github/blob/main/profile/README.md) · [English](https://github.com/OneUI-Mods/.github/blob/main/profile/README.en.md)

Samsung Galaxy / One UI向けの、非公式のカスタマイズアプリ・モジュールを公開しています。ホーム、ステータスバー、カメラ、録画、接続、診断など、目的に合わせて必要なアプリを選べます。

[アプリをまとめて管理](https://github.com/OneUI-Mods/OneUIModsManager/releases/latest) · [F-Droidで入手](https://oneui-mods.github.io/fdroid/) · [全リポジトリ](https://github.com/orgs/OneUI-Mods/repositories)

[開発用のホット更新と対応状況](../development/hot-reload/README.md)

## はじめに

[OneUI Mods Manager](https://github.com/OneUI-Mods/OneUIModsManager)から、アプリ一覧、インストール状況、各リポジトリのGitHub Releaseを確認できます。安定版・実験版の切り替え、更新内容の確認、APKのダウンロードと更新に対応しています。管理アプリ自体にroot・Vectorは不要です。

個別に導入する場合は、各アプリのREADMEで対応環境と導入手順を確認し、Releasesから署名済みrelease APKを入手してください。

## ホーム・表示

| アプリ | できること |
| --- | --- |
| [Galaxy Adaptive Bar](https://github.com/OneUI-Mods/galaxy-adaptive-statusbar) | 背景に合わせたステータスバーの配色とアニメーション |
| [One UI Home Tweaks](https://github.com/OneUI-Mods/OneUIHomeTweaks) | ホーム・アプリ履歴・クイックパネル・設定画面の調整 |
| [Dark App Tools](https://github.com/OneUI-Mods/DarkAppTools) | セサミ・povoのダーク表示 |

## カメラ・キャプチャ

| アプリ | できること |
| --- | --- |
| [Galaxy Camera Tools](https://github.com/OneUI-Mods/GalaxyCameraTools) | Samsung Camera・Camera Assistant・Expert RAWの機能拡張 |
| [Galaxy Capture Tools](https://github.com/OneUI-Mods/GalaxyCaptureTools) | 画面録画・スクリーンショットの機能拡張 |
| [Galaxy Shutter Mute Manager](https://github.com/OneUI-Mods/galaxy-shutter-mute-manager) | シャッター音の設定を管理 |
| [Galaxy Shutter Mute](https://github.com/OneUI-Mods/galaxy-shutter-mute) | カメラのシャッター音を調整 |

## 接続・共有

| アプリ | できること |
| --- | --- |
| [Tail ADB](https://github.com/OneUI-Mods/tail-adb) | Tailscale経由のADB接続 |
| [Secure Folder Bridge](https://github.com/OneUI-Mods/secure-folder-bridge) | 通常側・仕事用のファイルマネージャーからSecure Folderを読み書き |
| [HomePod Bridge](https://github.com/OneUI-Mods/HomePodBridge) | Galaxyのメディア出力からHomePod / HomePod miniへ音声を転送 |
| [SIM Pilot](https://github.com/OneUI-Mods/sim-pilot) | デュアルSIMの通信回線切り替えを支援 |

## 端末・診断

| アプリ | できること |
| --- | --- |
| [Galaxy Charge Monitor](https://github.com/OneUI-Mods/GalaxyChargeMonitor) | 充電状態・温度制限・充電設定を読み取り専用で監視 |
| [Galaxy Game Monitor](https://github.com/OneUI-Mods/GalaxyGameMonitor) | ゲームブースターでCPU・GPU負荷を最大クロック基準の表示に切り替え |
| [Galaxy DIAG](https://github.com/OneUI-Mods/galaxy-diag) | モデムの測定・診断用接続を準備 |
| [Galaxy Service Panel](https://github.com/OneUI-Mods/galaxy-service-panel) | Samsung Service Modeの表示を整理 |
| [Galaxy Update Guard](https://github.com/OneUI-Mods/galaxy-update-guard) | GalaxyのOSアップデートを停止・復元 |
| [Galaxy Reload](https://github.com/OneUI-Mods/galaxy-reload) | SystemUIの再読み込み |
| [SleepStore](https://github.com/OneUI-Mods/SleepStore) | ディープスリープ中のアプリのストア更新表示を支援 |

## 省電力・互換性

| アプリ | できること |
| --- | --- |
| [App Battery Tools](https://github.com/OneUI-Mods/app-battery-tools) | 対応アプリごとに不要な電池消費を抑制 |
| [Legacy Game Tools](https://github.com/OneUI-Mods/legacy-game-tools) | 対応する古い体験版ゲームの起動互換性を改善 |
| [Rain Compatibility Tools](https://github.com/OneUI-Mods/rain-compatibility-tools) | Rainの起動失敗の診断とリソース生成の限定的な補修 |

## 配布と対応環境

- **GitHub Releases**：各アプリの変更内容と署名済みrelease APKを公開しています。
- **OneUI Mods Manager**：[公開カタログ](https://github.com/OneUI-Mods/OneUIModsManager/blob/main/catalog/apps.json)から一覧を取得し、各リポジトリのリリースを直接確認します。
- **専用F-Droidリポジトリ**：[追加方法と掲載状況](https://oneui-mods.github.io/fdroid/)を確認できます。公式F-Droidへの掲載とは別の配布元です。

対応する端末・Android / One UIのバージョン、root・Vector・Shizukuなどの条件はアプリごとに異なります。実験的な機能や未検証の環境は、各READMEとリリース説明で案内しています。

## 不具合報告・開発

不具合や機能の提案は、対象リポジトリのIssuesへお願いします。アプリのバージョン、端末名、Android / One UIのバージョン、再現手順があると調査しやすくなります。

ソースとライセンスは各リポジトリで公開しています。ビルド・実装・検証については、各アプリの開発者向けドキュメントを参照してください。

開発・管理：ryuya0124。Samsungとは無関係の非公式プロジェクトです。
