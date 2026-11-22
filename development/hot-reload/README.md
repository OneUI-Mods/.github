# OneUI Modsのホット更新

[English](README.en.md)

`apps.json` は管理アプリのカタログにある全アプリについて、利用できる更新経路と移行状況を追跡します。`list` はカタログと照合し、登録漏れと古い項目を検出します。各アプリは単体でビルドと更新ができます。

## 開発中に反映する

1. テスト対象のプロセスが、ホット更新対応版を少なくとも一度読み込んだ状態にします。
2. 新しい版は `versionCode` を上げ、既存の配布鍵で署名したAPKを用意します。
3. 対象プロセスを開いたまま次のコマンドを実行します。必要なら `--host` で対象の実際のプロセス名を指定します。

```sh
python3 .github/development/hot-reload/hot_update.py list
python3 .github/development/hot-reload/hot_update.py apply GalaxyGameMonitor app-release.apk --serial SERIAL
```

`apply` はカタログの署名、APKのパッケージ、versionCodeを照合して上書きします。同じPIDから新しいコードの適用ログを受けた場合に成功を返します。対象未起動、PIDの変化、適用ログなしはエラーです。

## 新規モジュール・新機能

- libxposed API 102のJavaエントリは1クラスにします。初回とホット更新の両方から、同じフック登録処理を呼び出します。[モジュールのライフサイクル](https://libxposed.github.io/api/io/github/libxposed/api/XposedModuleInterface.html)
- フックには機能単位の安定したIDを割り当てます。登録先が同じメソッドならIDで差し替えられます。対象が変わる更新では不要な旧ハンドルも解除します。[HookBuilder](https://libxposed.github.io/api/io/github/libxposed/api/XposedInterface.HookBuilder.html)
- 初回の `Application.attach` と、既に動作中のアプリへ接続し直す処理を分けます。画面やBinder、購読、タイマー、ワーカー、ネイティブ資源の所有者を明確にし、片付けと再接続を実装します。旧モジュールのインスタンスを次の世代に渡さず、対象側のClassLoaderなど世代に依存しない情報で再接続します。
- 処理中に安全な引き継ぎができなければ `onHotReloading` で更新を見送ります。対応確認後に `autoHotReload=true` を設定します。既存のクラッシュ保護、認証、デバイスの対象範囲を維持します。
- 更新後の処理を実際に登録できた時点で `ONEUI_MODS_HOT_RELOAD package=<applicationId> version=<versionCode> pid=<PID>` を記録します。対象メソッド変更、連続更新、監視の二重登録、失敗時の挙動を確認します。[フックだけを持つモジュールの例](HookEntry.example.kt)

フック全体の入れ替えが難しいアプリでは、レンダリングの計算や最適化ポリシーから、署名付きAPKで更新できる独立した実装に移せます。通常のフック、描画の状態、ネイティブ資源はホスト側に持たせると、使用中の画面を維持できます。[署名付き実装の読み込み例](SignedLogic.example.kt)

モジュールを持たないアプリの開発では、実行中のdebug版にAndroid StudioのApply Changesを使える場合があります。APK上書き時の自アプリのプロセス維持、OSの起動時処理、JNIやHALの差し替えは別の実行要件があります。恒久的に動くサービスには、セッションの所有者と更新可能なロジックを分け、処理の境界で切り替えられるようにします。[Android Studio Apply Changes](https://developer.android.com/studio/run#apply-changes)

| 状態 | 更新経路 |
| --- | --- |
| `api102` | API 102のホット更新コールバックを実装済み |
| `signed-code` | 署名済みコードの独自差し替え。対象プロセスを記載 |
| `lifecycle` | 実行中のコールバックや資源の移行が未実装 |
| `service` | 常駐サービスや接続の引き継ぎが未実装 |
| `native` | ネイティブ・OS起動・旧APIへの依存があり、専用の移行が必要 |
| `app` | APK自身が対象。開発用Apply Changesを利用可能な範囲で使用 |

## 移行確認の基準

一覧の `api102` は、列挙したプロセスにAPI 102の更新処理があることを示します。アプリ全体やGalaxyでの検証済みを示すものではありません。初回のみ、対応版を対象プロセスに通常の方法で読み込ませます。作業中の更新を見送られた場合は、対象がアイドルになってから、そのモジュールのAPI 102サービスで再要求できます。

| アプリ | 現在の境界 |
| --- | --- |
| One UI Home Tweaks | SystemUI、ホーム、開発者向け設定、壁紙プレビュー、履歴フォーカスの `system_server` に対応。フォーカスの旧Binderを渡した世代では更新を見送る |
| Galaxy Glass Tools | SystemUI・ホーム・Samsung Capture・各補助プロセス・対象システムアプリに対応。表示中のCompose Modifierは描画コールバックの処理だけを差し替える |
| Galaxy Capture Tools | SystemUI、Samsung Capture、専用ワーカー、`system_server` に対応。実行中の録画・画面共有・有効な選択候補があれば更新を見送る |
| HomePod Bridge | 接続や音声経路の解放処理が終わればSystemUI側を更新。専用HALは既存の起動手順で読み込む |
| Legacy Game Tools | ネイティブライブラリが同一ならKotlin側を更新。JNIの変更は次回ゲーム起動時に読み込む |
| Rain Compatibility Tools | リソース復旧処理を署名付きAPKから差し替える。埋め込みLSPatch API 93のフック登録は常駐し、登録方法の変更は次回起動時に読み込む |

対応完了の確認は、対象ごとに連続2回の更新を行い、同じPIDで新しいコードが動くことと、更新前の機能が使えることを確かめます。録画・接続・操作中に見送る対象では、見送り後に使い続けられ、アイドル後の再試行で更新されることも確認します。
