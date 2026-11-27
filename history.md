# 作業履歴

## 2026-11-27 オートマウス・スクロールのレイヤー番号を修正
- 理由: Keymap Editorでレイヤー順が変わり、overlayの番号が実際の並び（0 QWERTY / 1 COMMON / 2 FUNCTION / 3 NUM / 4 AML / 5 SYS）とずれていた。ボール操作でNUMがオンになり、スクロールがCOMMONで効く状態だった。
- 変更: `circa40_right.overlay` の `zip_temp_layer` を 3→2（FUNCTION）、`scroll-layer` の `layers` を 1→3（NUM）に変更。コメントも更新。README の配列説明を現在のキーマップに合わせて書き直し。
- 影響: `circa40_right`（Central）のみ。キーマップ自体と左手の変更なし。
- 確認: Actionsのビルド。実機検証は未実施。
- 次の一手: 右手を書き込み、ボールを動かすとFUNCTION（クリック）になること、NUMホールド中にスクロールになることを確認。

## 2026-11-12 ディープスリープ無効化
- 理由: 左側が反応しなくなる症状の切り分けと、ディープスリープ不要の要望に対応。
- 変更: `config/circa40.conf` の `CONFIG_ZMK_SLEEP` を `y` → `n` に変更し、不要な `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000` を削除。
- 影響: `xiao_ble//zmk` の `circa40_left`（Peripheral）と `circa40_right`（Central）。レイヤー、split/BLE設定、スタック、ACLバッファ、依存関係の変更なし。待機時の電池消費は増える可能性あり。
- 確認: 差分と設定の重複を確認。ビルド・実機検証は未実施。
- 次の一手: 左右のファームウェアをビルドして書き込み、15分以上放置後の入力を確認。
