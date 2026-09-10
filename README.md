# zmk-config-Circa40

Circa40（XIAO nRF52840 Plus）のZMK設定です。**右手がCentral、左手がPeripheral**です。
ビルドはGitHub Actionsのみで行います。ZMK v0.3.0と、それに対応するPMW3610ドライバのコミットを固定しています。

## ビルドと書き込み

`main`へのpush、Pull Request、またはActionsの「Build Circa40 → Run workflow」でビルドします。
成功した実行の`firmware` artifactをダウンロードして展開します。

- `circa40-left.uf2`：左手
- `circa40-right-central.uf2`：右手（USB/Bluetoothの接続先）
- `circa40-settings-reset.uf2`：ペアリング情報の初期化専用。通常は書き込みません。

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
向きは実機確認後、右overlayの`trackball`に`swap-xy`、`invert-x`、`invert-y`を追加して調整します。
電源スイッチSW43/SW44はハードウェアで電池を切断するもので、キーマップには含みません。

## 注意

Actions成功はコンパイル確認です。実機のキー入力・左右通信・センサーの動作と方向・消費電流は別途確認が必要です。
この設定はPlusの追加GPIOを使用します。通常のXIAO nRF52840の端子配置とは異なります。
基板/CAD本体はこのリポジトリへコピーしていません。

参照：[ZMK](https://github.com/zmkfirmware/zmk/tree/v0.3.0)、[PMW3610ドライバ](https://github.com/badjeff/zmk-pmw3610-driver/tree/5c5af40de4d8cdf55dc63c4c5907af1e52da6a95)。
