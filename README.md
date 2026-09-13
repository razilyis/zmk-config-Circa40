# zmk-config-Circa40

Circa40（XIAO nRF52840 Plus）のZMK設定です。**右手がCentral、左手がPeripheral**です。
ビルドはGitHub Actionsのみで行います。ZMKは`main`（Zephyr 4.1）を、PMW3610ドライバはZephyr 4.1対応版を、
それぞれコミットSHAで固定しています。ZMK v0.4は未リリースのため、タグではなく`main`をpinしています。
v0.4.0が出たら`config/west.yml`の`revision`をタグに差し替えるだけで済みます（Zephyrのバージョンは変わりません）。

## ビルドと書き込み

`main`へのpush、Pull Request、またはActionsの「Build Circa40 → Run workflow」でビルドします。
成功した実行の`firmware` artifactをダウンロードして展開します。

- `circa40-left.uf2`：左手
- `circa40-right-central.uf2`：右手（USB/Bluetoothの接続先）
- `circa40-settings-reset.uf2`：ペアリング情報の初期化専用。通常は書き込みません。
- `circa40-right-logging.uf2`：切り分け用。右手にUSB接続してドライバのログをシリアル出力します。通常は書き込みません。

XIAOをブートローダーモードにして、対応するUF2をコピーします。初回は左右とも書き込み、両方の電源を入れます。
既存のZMK設定から移行して左右がつながらない場合は、左右それぞれにsettings-resetを書いた後、対応する通常ファームウェアを書き直してください。
settings-resetは保存済みBluetooth情報を消去します。

## 配列

`config/circa40.keymap`で変更できます。各レイヤーは現行PCBに合わせた43位置です。
トラボを使用してSW45を実装しない場合も、その位置は残してください。

```text
SW1 SW2 SW3 SW4 SW5 SW6      SW22 SW23 SW24 SW25 SW26 SW27
SW7 SW8 SW9 SW10 SW11 SW12   SW28 SW29 SW30 SW31 SW32
SW13 SW14 SW15 SW16 SW17     SW33 SW34 SW35 SW36 SW37 SW38
SW18 SW19 SW20 SW21          SW39 SW40 SW45 SW41 SW42
```

初期配列はQWERTY。SW20はタップSpace／ホールドNUM、SW40はタップSpace／ホールドSYSです。
SW39は右クリック、SW41は左クリック、SW42はEnter。SW45は実装した場合Spaceです。
SYSレイヤーのSW2〜SW6でBluetoothプロファイル0〜4を選択、SW1で選択中プロファイルをクリアします。

## Keymap Editorの表示

`config/circa40.json` が [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/) 用の表示レイアウトです。
`circa40.keymap` と同名のJSONなので、GitHub連携で読み込まれます。更新後はエディターを再読み込みし、このリポジトリの最新の `main` を選択してください。
左右21/22キーの間隔と行のずれはPCB中心座標から19.05 mm単位に換算しています。SW45のみ指定された1.5U、それ以外は1Uの編集用表示です。
配列の順番は `circa40.dtsi` の43位置と一致し、SW45をトラボのために未実装にする場合も位置を削除しません。
JSON内の `row` / `col` はエディターの表示・整形用です。GPIOやマトリクスの列番号ではありません。
このJSONを変更してもファームウェアの左右通信設定やキー割り当ては変わりません。

KiCad付属Pythonで `tools/verify_pcb.py ../Circa40.kicad_pcb` を実行すると、マトリクスと表示順・PCB位置・左右の間隔・キーの重なりを確認できます。

## 基板との対応

2026-09-10の`Circa40.kicad_pcb`と回路図のラベルを照合。左右はGPIO配置が異なるため、overlayを交換しないでください。
ダイオードはスイッチ側がA、行側がKなので`col2row`です。

|信号|左手|右手|
|---|---|---|
|Col0〜3|P0.02 / P0.03 / P0.28 / P0.29|同左|
|Col4〜5|P0.15 / P0.19|P0.04 / P0.05|
|Row0〜3|P1.01 / P1.07 / P1.05 / P1.03|P1.11 / P1.12 / P1.13 / P1.14|

右J1：1=GND、2=MOTION(P1.15)、3=SDIO(P1.07)、4=CS(P1.05)、5=SCLK(P1.03)、6=3.3V。
PMW3610は3線式SPIでMOSI/MISOをSDIOに共用。初期600 CPIです。

> **FFCケーブルはAタイプ（両端の接点が同じ面）を使用してください。**
> Bタイプを挿すとJ1のピン順が1↔6で反転し、GNDと3.3Vが入れ替わって電源逆接になります。
> 実機ブリングアップ時にこれをやってセンサーが応答しなくなりました（Aタイプへ交換して復旧、センサーは無事）。

向きは実機確認の結果、`swap-xy`のみで4方向とも正しくなりました（`invert-x`/`invert-y`は不要）。
右overlayの`trackball`に設定済みです。
電源スイッチSW43/SW44はハードウェアで電池を切断するもので、キーマップには含みません。

## 注意

Actions成功はコンパイル確認です。実機では**キー入力・バッテリー測定・トラックボールの動作と方向・左右のBluetooth通信**を確認済みです。
**NUMレイヤーのスクロールと消費電流は未確認**です。

> トラックボールが「初期化ログは正常なのにカーソルが一切動かない」場合は、MOTION線（J1 pin 2 ↔ P1.15）の断線を疑ってください。
> ドライバはポーリングせずMOTION割り込みでのみセンサーを読むため、この1本だけが切れていても初期化は最後まで成功します。
> 判定には`circa40-right-logging`を焼いて、ボールを回しながら`zmk_hid_mouse_movement_set`が出るかを見ます。
Kconfigの指定ミスは警告なく無視されるため、設定を変えたときはActionsログの`.config`ダンプで実効値を確認してください。
この設定はPlusの追加GPIOを使用します。通常のXIAO nRF52840の端子配置とは異なります。
基板/CAD本体はこのリポジトリへコピーしていません。

参照：[ZMK](https://github.com/zmkfirmware/zmk/tree/641514a97db345f499dd50b0360e594270f008fe)、[PMW3610ドライバ](https://github.com/badjeff/zmk-pmw3610-driver/tree/44b4a76b74d293a93cec4ccb7e04cb8d29c10f93)、[Zephyr 4.1移行の解説](https://zmk.dev/blog/2025/12/09/zephyr-4-1)。
