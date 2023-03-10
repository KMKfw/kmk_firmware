# はじめに
> Life was like a box of chocolates. You never know what you're gonna get.

KMK は[CircuitPython](https://circuitpython.org/)の上に配置されるキーボード用の実装レイヤーです。
そのため、[CircuitPython をサポートするほとんどのボード](https://circuitpython.org/downloads)と互換性があります。

 最新の安定したバージョンを使用することをおすすめします。(>5.0)
使用可能やおすすめなデバイスは[こちら](Officially_Supported_Microcontrollers.md)から確認できます。

CircuitPython の最適化バージョン（特定のボードの容量制限に対処した、プリインストールされた関連モジュールの選択が可能なバージョン）も提供しています。


## TL;DR クイックスタートガイド
> To infinity and beyond!

1. CircuitPython をボードに[インストール](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython)する。


2. マスターブランチから[KMK のコピー](https://github.com/KMKfw/kmk_firmware/archive/refs/heads/master.zip)を取得。


3. ファイルを展開し、KMK フォルダーと boot.py ファイルを USB ドライブのルート（CIRCUITPY と表示されることが多い）にコピーする。


4. 同じルートディレクトリー（boot.py と同レベル）に新規で*code.py* または *main.py*のファイルを作成する。中身は以下の例とする。

***重要：*** GP0 / GP1 ピンを使用ボードに合わせて下さい


```
print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP0,)
keyboard.row_pins = (board.GP1,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.A,]
]

if __name__ == '__main__':
    keyboard.go()
```

1. ワイヤーなどで GPIO 0 と GPIO 1（またはほかに指定したピン）を接続する。


2. "A"や"Q"(キーボードのレイアウトによって異なる)が表示されたら、完成！


## とりあえず一通り動くようになったので、もっとに先へ進みたい場合
> This is your last chance. After this, there is no turning back. You take the blue pill—the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes. Remember: all I'm offering is the truth. Nothing more.

### フルサポートされているキーボードを持っている場合
 あなたのキーボードとマイコンが正式にサポートされている場合、[こちらのページ](https://github.com/KMKfw/boards)から`kb.py` と `main.py`を"flash drive"のルートに落とす必要があります。より高度な手順は[こちら](config_and_keymap.md)から確認できます。

 Circuitpython を使用する場合、 [boot.py](/boot.py)も必要になります。

### ほかに自作ボードなどを持っていて、カスタマイズされた KMK を導入したい場合

最初にデバイスの動作や具体的なマトリックス構成についてしっかり理解してください。
QMK チームが提供している手配線キーボード用の[ガイド](https://docs.qmk.fm/#/hand_wire)と[ドキュメント](http://pcbheaven.com/wikipages/How_Key_Matrices_Works/) を確認できます。

要旨をつかめてきたら：
- [ここ](config_and_keymap.md) と [ここ](keys.md)を見て、code.py / main.py ファイルをカスタイマイズできます。

- 使用可能なキーコードの[リファレンス](keycodes.md)があります。

- [インターナショナル](international.md)は、US 配列以外のキーボードにキーを追加する拡張機能で、[メディアキー](media_keys.md)は・・・メディアにキーを追加する拡張機能です。

さらに先へ進むと：
- [シーケンス](sequences.md) 一つのアクションで複数のキーストロークを送信するために使用します。
- [レイヤー](layers.md)でタッチ一つでキーボードの全体の動きを変えることができます。

- [モドタップ](holdtap.md) でキーの押し/長押しの動作を設定し、何回押されたかによって[タップダンス](tapdance.md)を設定します。

RGB や分裂型などの機能を楽しめたい場合は、ビルトイン[モジュール](modules.md)と[拡張機能](extensions.md)を見てみてください！

私たちが提供する、いろんな [ユーザー事例](https://github.com/KMKfw/user_keymaps)や[ドキュメント](https://github.com/KMKfw/kmk_firmware/tree/master/docs)からアイデアを得ることもできます。


## ヘルプ/サポート
> Roads? Where we're going we don't need roads.

デバッグについてのヘルプが必要な場合は[こちら](debugging.md)。

KMK についてサポートが必要な場合や、コミュニケーションをとりたい場合は[こちら](https://kmkfw.zulipchat.com)。

チャットで助けを求める場合やバグ レポートを開く場合は、可能であれば KMK
のコピーが最新であることを確認してください。
