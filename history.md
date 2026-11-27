# 作業履歴

## 2026-11-27 Bluetooth 安定化設定を AroundFortyRB から移植
- 理由: 左手が反応しなくなる症状の対策。AroundFortyRB で使っている BLE 安定化設定を試す。
- 変更: `circa40.conf`（左右共通）に BLE 試験的機能無効、BT RX/HCI TX スタック、ACL 251、接続間隔 15ms 固定、2M PHY 無効、接続数上限 6、BLE/低優先度スタックを追加。`circa40_left.conf` に Split Peripheral スタック、`circa40_right.conf` に送信出力 +8dBm、Split Central スタック、Input スタックを追加。
- 移植しなかったもの: スリープ設定（Circa40 は 11/12 に無効化済み）、RGB LED、ヒープ、ZMK Studio、キーボード名、バッテリー代理表示。
- 確認: Actions のビルドと `.config` ダンプでの実効値。実機検証は未実施。
- 次の一手: 左右とも書き込み（設定が変わるので念のため settings-reset → 通常ファーム）、数日使って左手の切断が出るか確認。

## 2026-11-12 ディープスリープ無効化
- 理由: 左側が反応しなくなる症状の切り分けと、ディープスリープ不要の要望に対応。
- 変更: `config/circa40.conf` の `CONFIG_ZMK_SLEEP` を `y` → `n` に変更し、不要な `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000` を削除。
- 影響: `xiao_ble//zmk` の `circa40_left`（Peripheral）と `circa40_right`（Central）。レイヤー、split/BLE設定、スタック、ACLバッファ、依存関係の変更なし。待機時の電池消費は増える可能性あり。
- 確認: 差分と設定の重複を確認。ビルド・実機検証は未実施。
- 次の一手: 左右のファームウェアをビルドして書き込み、15分以上放置後の入力を確認。
