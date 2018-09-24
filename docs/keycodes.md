# Keycodes Overview

When defining a [keymap](keymap.md) each key needs a valid key definition. This page documents the symbols that correspond to keycodes that are available to you in QMK.

This is a reference only. Each group of keys links to the page documenting their functionality in more detail.

## [Basic Keycodes](keycodes_basic.md)

|Key                    |Aliases             |Description                                    |
|-----------------------|--------------------|-----------------------------------------------|
|`KC.NO`                |                    |Ignore this key (NOOP)                         |
|`KC.TRANSPARENT`       |`KC.TRNS`           |Use the next lowest non-transparent key        |
|`KC.A`                 |                    |`a` and `A`                                    |
|`KC.B`                 |                    |`b` and `B`                                    |
|`KC.C`                 |                    |`c` and `C`                                    |
|`KC.D`                 |                    |`d` and `D`                                    |
|`KC.E`                 |                    |`e` and `E`                                    |
|`KC.F`                 |                    |`f` and `F`                                    |
|`KC.G`                 |                    |`g` and `G`                                    |
|`KC.H`                 |                    |`h` and `H`                                    |
|`KC.I`                 |                    |`i` and `I`                                    |
|`KC.J`                 |                    |`j` and `J`                                    |
|`KC.K`                 |                    |`k` and `K`                                    |
|`KC.L`                 |                    |`l` and `L`                                    |
|`KC.M`                 |                    |`m` and `M`                                    |
|`KC.N`                 |                    |`n` and `N`                                    |
|`KC.O`                 |                    |`o` and `O`                                    |
|`KC.P`                 |                    |`p` and `P`                                    |
|`KC.Q`                 |                    |`q` and `Q`                                    |
|`KC.R`                 |                    |`r` and `R`                                    |
|`KC.S`                 |                    |`s` and `S`                                    |
|`KC.T`                 |                    |`t` and `T`                                    |
|`KC.U`                 |                    |`u` and `U`                                    |
|`KC.V`                 |                    |`v` and `V`                                    |
|`KC.W`                 |                    |`w` and `W`                                    |
|`KC.X`                 |                    |`x` and `X`                                    |
|`KC.Y`                 |                    |`y` and `Y`                                    |
|`KC.Z`                 |                    |`z` and `Z`                                    |
|`KC.N1`                |                    |`1` and `!`                                    |
|`KC.N2`                |                    |`2` and `@`                                    |
|`KC.N3`                |                    |`3` and `#`                                    |
|`KC.N4`                |                    |`4` and `$`                                    |
|`KC.N5`                |                    |`5` and `%`                                    |
|`KC.N6`                |                    |`6` and `^`                                    |
|`KC.N7`                |                    |`7` and `&`                                    |
|`KC.N8`                |                    |`8` and `*`                                    |
|`KC.N9`                |                    |`9` and `(`                                    |
|`KC.N0`                |                    |`0` and `)`                                    |
|`KC.ENTER`             |`KC.ENT`            |Return (Enter)                                 |
|`KC.ESCAPE`            |`KC.ESC`            |Escape                                         |
|`KC.BSPACE`            |`KC.BSPC`           |Delete (Backspace)                             |
|`KC.TAB`               |                    |Tab                                            |
|`KC.SPACE`             |`KC.SPC`            |Spacebar                                       |
|`KC.MINUS`             |`KC.MINS`           |`-` and `_`                                    |
|`KC.EQUAL`             |`KC.EQL`            |`=` and `+`                                    |
|`KC.LBRACKET`          |`KC.LBRC`           |`[` and `{`                                    |
|`KC.RBRACKET`          |`KC.RBRC`           |`]` and `}`                                    |
|`KC.BSLASH`            |`KC.BSLS`           |`\` and <code>&#124;</code>                    |
|`KC.NONUS_HASH`        |`KC.NUHS`           |Non-US `#` and `~`                             |
|`KC.SCOLON`            |`KC.SCLN`           |`;` and `:`                                    |
|`KC.QUOTE`             |`KC.QUOT`           |`'` and `"`                                    |
|`KC.GRAVE`             |`KC.GRV`, `KC.ZKHK` |<code>&#96;</code> and `~`, JIS Zenkaku/Hankaku|
|`KC.COMMA`             |`KC.COMM`           |`,` and `<`                                    |
|`KC.DOT`               |                    |`.` and `>`                                    |
|`KC.SLASH`             |`KC.SLSH`           |`/` and `?`                                    |
|`KC.CAPSLOCK`          |`KC.CLCK`, `KC.CAPS`|Caps Lock                                      |
|`KC.F1`                |                    |F1                                             |
|`KC.F2`                |                    |F2                                             |
|`KC.F3`                |                    |F3                                             |
|`KC.F4`                |                    |F4                                             |
|`KC.F5`                |                    |F5                                             |
|`KC.F6`                |                    |F6                                             |
|`KC.F7`                |                    |F7                                             |
|`KC.F8`                |                    |F8                                             |
|`KC.F9`                |                    |F9                                             |
|`KC.F10`               |                    |F10                                            |
|`KC.F11`               |                    |F11                                            |
|`KC.F12`               |                    |F12                                            |
|`KC.PSCREEN`           |`KC.PSCR`           |Print Screen                                   |
|`KC.SCROLLLOCK`        |`KC.SLCK`           |Scroll Lock                                    |
|`KC.PAUSE`             |`KC.PAUS`, `KC.BRK` |Pause                                          |
|`KC.INSERT`            |`KC.INS`            |Insert                                         |
|`KC.HOME`              |                    |Home                                           |
|`KC.PGUP`              |                    |Page Up                                        |
|`KC.DELETE`            |`KC.DEL`            |Forward Delete                                 |
|`KC.END`               |                    |End                                            |
|`KC.PGDOWN`            |`KC.PGDN`           |Page Down                                      |
|`KC.RIGHT`             |`KC.RGHT`           |Right Arrow                                    |
|`KC.LEFT`              |                    |Left Arrow                                     |
|`KC.DOWN`              |                    |Down Arrow                                     |
|`KC.UP`                |                    |Up Arrow                                       |
|`KC.NUMLOCK`           |`KC.NLCK`           |Keypad Num Lock and Clear                      |
|`KC.KP_SLASH`          |`KC.PSLS`           |Keypad `/`                                     |
|`KC.KP_ASTERISK`       |`KC.PAST`           |Keypad `*`                                     |
|`KC.KP_MINUS`          |`KC.PMNS`           |Keypad `-`                                     |
|`KC.KP_PLUS`           |`KC.PPLS`           |Keypad `+`                                     |
|`KC.KP_ENTER`          |`KC.PENT`           |Keypad Enter                                   |
|`KC.KP_1`              |`KC.P1`             |Keypad `1` and End                             |
|`KC.KP_2`              |`KC.P2`             |Keypad `2` and Down Arrow                      |
|`KC.KP_3`              |`KC.P3`             |Keypad `3` and Page Down                       |
|`KC.KP_4`              |`KC.P4`             |Keypad `4` and Left Arrow                      |
|`KC.KP_5`              |`KC.P5`             |Keypad `5`                                     |
|`KC.KP_6`              |`KC.P6`             |Keypad `6` and Right Arrow                     |
|`KC.KP_7`              |`KC.P7`             |Keypad `7` and Home                            |
|`KC.KP_8`              |`KC.P8`             |Keypad `8` and Up Arrow                        |
|`KC.KP_9`              |`KC.P9`             |Keypad `9` and Page Up                         |
|`KC.KP_0`              |`KC.P0`             |Keypad `0` and Insert                          |
|`KC.KP_DOT`            |`KC.PDOT`           |Keypad `.` and Delete                          |
|`KC.NONUS_BSLASH`      |`KC.NUBS`           |Non-US `\` and <code>&#124;</code>             |
|`KC.APPLICATION`       |`KC.APP`            |Application (Windows Menu Key)                 |
|`KC.POWER`             |                    |System Power (macOS)                           |
|`KC.KP_EQUAL`          |`KC.PEQL`           |Keypad `=`                                     |
|`KC.F13`               |                    |F13                                            |
|`KC.F14`               |                    |F14                                            |
|`KC.F15`               |                    |F15                                            |
|`KC.F16`               |                    |F16                                            |
|`KC.F17`               |                    |F17                                            |
|`KC.F18`               |                    |F18                                            |
|`KC.F19`               |                    |F19                                            |
|`KC.F20`               |                    |F20                                            |
|`KC.F21`               |                    |F21                                            |
|`KC.F22`               |                    |F22                                            |
|`KC.F23`               |                    |F23                                            |
|`KC.F24`               |                    |F24                                            |
|`KC.EXECUTE`           |`KC.EXEC`           |Execute                                        |
|`KC.HELP`              |                    |Help                                           |
|`KC.MENU`              |                    |Menu                                           |
|`KC.SELECT`            |`KC.SLCT`           |Select                                         |
|`KC.STOP`              |                    |Stop                                           |
|`KC.AGAIN`             |`KC.AGIN`           |Again                                          |
|`KC.UNDO`              |                    |Undo                                           |
|`KC.CUT`               |                    |Cut                                            |
|`KC.COPY`              |                    |Copy                                           |
|`KC.PASTE`             |`KC.PSTE`           |Paste                                          |
|`KC.FIND`              |                    |Find                                           |
|`KC._MUTE`             |                    |Mute (macOS)                                   |
|`KC._VOLUP`            |                    |Volume Up (macOS)                              |
|`KC._VOLDOWN`          |                    |Volume Down (macOS)                            |
|`KC.LOCKING_CAPS`      |`KC.LCAP`           |Locking Caps Lock                              |
|`KC.LOCKING_NUM`       |`KC.LNUM`           |Locking Num Lock                               |
|`KC.LOCKING_SCROLL`    |`KC.LSCR`           |Locking Scroll Lock                            |
|`KC.KP_COMMA`          |`KC.PCMM`           |Keypad `,`                                     |
|`KC.KP_EQUAL_AS400`    |                    |Keypad `=` on AS/400 keyboards                 |
|`KC.INT1`              |`KC.RO`             |JIS `\` and <code>&#124;</code>                |
|`KC.INT2`              |`KC.KANA`           |JIS Katakana/Hiragana                          |
|`KC.INT3`              |`KC.JYEN`           |JIS `¥`                                        |
|`KC.INT4`              |`KC.HENK`           |JIS Henkan                                     |
|`KC.INT5`              |`KC.MHEN`           |JIS Muhenkan                                   |
|`KC.INT6`              |                    |JIS Numpad `,`                                 |
|`KC.INT7`              |                    |International 7                                |
|`KC.INT8`              |                    |International 8                                |
|`KC.INT9`              |                    |International 9                                |
|`KC.LANG1`             |`KC.HAEN`           |Hangul/English                                 |
|`KC.LANG2`             |`KC.HANJ`           |Hanja                                          |
|`KC.LANG3`             |                    |JIS Katakana                                   |
|`KC.LANG4`             |                    |JIS Hiragana                                   |
|`KC.LANG5`             |                    |JIS Zenkaku/Hankaku                            |
|`KC.LANG6`             |                    |Language 6                                     |
|`KC.LANG7`             |                    |Language 7                                     |
|`KC.LANG8`             |                    |Language 8                                     |
|`KC.LANG9`             |                    |Language 9                                     |
|`KC.ALT_ERASE`         |`KC.ERAS`           |Alternate Erase                                |
|`KC.SYSREQ`            |                    |SysReq/Attention                               |
|`KC.CANCEL`            |                    |Cancel                                         |
|`KC.CLEAR`             |`KC.CLR`            |Clear                                          |
|`KC.PRIOR`             |                    |Prior                                          |
|`KC.RETURN`            |                    |Return                                         |
|`KC.SEPARATOR`         |                    |Separator                                      |
|`KC.OUT`               |                    |Out                                            |
|`KC.OPER`              |                    |Oper                                           |
|`KC.CLEAR_AGAIN`       |                    |Clear/Again                                    |
|`KC.CRSEL`             |                    |CrSel/Props                                    |
|`KC.EXSEL`             |                    |ExSel                                          |
|`KC.LCTRL`             |`KC.LCTL`           |Left Control                                   |
|`KC.LSHIFT`            |`KC.LSFT`           |Left Shift                                     |
|`KC.LALT`              |                    |Left Alt                                       |
|`KC.LGUI`              |`KC.LCMD`, `KC.LWIN`|Left GUI (Windows/Command/Meta key)            |
|`KC.RCTRL`             |`KC.RCTL`           |Right Control                                  |
|`KC.RSHIFT`            |`KC.RSFT`           |Right Shift                                    |
|`KC.RALT`              |                    |Right Alt                                      |
|`KC.RGUI`              |`KC.RCMD`, `KC.RWIN`|Right GUI (Windows/Command/Meta key)           |
|`KC.SYSTEM_POWER`      |`KC.PWR`            |System Power Down                              |
|`KC.SYSTEM_SLEEP`      |`KC.SLEP`           |System Sleep                                   |
|`KC.SYSTEM_WAKE`       |`KC.WAKE`           |System Wake                                    |
|`KC.AUDIO_MUTE`        |`KC.MUTE`           |Mute                                           |
|`KC.AUDIO_VOL_UP`      |`KC.VOLU`           |Volume Up                                      |
|`KC.AUDIO_VOL_DOWN`    |`KC.VOLD`           |Volume Down                                    |
|`KC.MEDIA_NEXT_TRACK`  |`KC.MNXT`           |Next Track (Windows)                           |
|`KC.MEDIA_PREV_TRACK`  |`KC.MPRV`           |Previous Track (Windows)                       |
|`KC.MEDIA_STOP`        |`KC.MSTP`           |Stop Track (Windows)                           |
|`KC.MEDIA_PLAY_PAUSE`  |`KC.MPLY`           |Play/Pause Track                               |
|`KC.MEDIA_SELECT`      |`KC.MSEL`           |Launch Media Player (Windows)                  |
|`KC.MEDIA_EJECT`       |`KC.EJCT`           |Eject (macOS)                                  |
|`KC.MAIL`              |                    |Launch Mail (Windows)                          |
|`KC.CALCULATOR`        |`KC.CALC`           |Launch Calculator (Windows)                    |
|`KC.MY_COMPUTER`       |`KC.MYCM`           |Launch My Computer (Windows)                   |
|`KC.WWW_SEARCH`        |`KC.WSCH`           |Browser Search (Windows)                       |
|`KC.WWW_HOME`          |`KC.WHOM`           |Browser Home (Windows)                         |
|`KC.WWW_BACK`          |`KC.WBAK`           |Browser Back (Windows)                         |
|`KC.WWW_FORWARD`       |`KC.WFWD`           |Browser Forward (Windows)                      |
|`KC.WWW_STOP`          |`KC.WSTP`           |Browser Stop (Windows)                         |
|`KC.WWW_REFRESH`       |`KC.WREF`           |Browser Refresh (Windows)                      |
|`KC.WWW_FAVORITES`     |`KC.WFAV`           |Browser Favorites (Windows)                    |
|`KC.MEDIA_FAST_FORWARD`|`KC.MFFD`           |Next Track (macOS)                             |
|`KC.MEDIA_REWIND`      |`KC.MRWD`           |Previous Track (macOS)                         |


## [US ANSI Shifted Symbols]

|Key                     |Aliases            |Description        |
|------------------------|-------------------|-------------------|
|`KC.TILDE`              |`KC.TILD`          |`~`                |
|`KC.EXCLAIM`            |`KC.EXLM`          |`!`                |
|`KC.AT`                 |                   |`@`                |
|`KC.HASH`               |                   |`#`                |
|`KC.DOLLAR`             |`KC.DLR`           |`$`                |
|`KC.PERCENT`            |`KC.PERC`          |`%`                |
|`KC.CIRCUMFLEX`         |`KC.CIRC`          |`^`                |
|`KC.AMPERSAND`          |`KC.AMPR`          |`&`                |
|`KC.ASTERISK`           |`KC.ASTR`          |`*`                |
|`KC.LEFT_PAREN`         |`KC.LPRN`          |`(`                |
|`KC.RIGHT_PAREN`        |`KC.RPRN`          |`)`                |
|`KC.UNDERSCORE`         |`KC.UNDS`          |`_`                |
|`KC.PLUS`               |                   |`+`                |
|`KC.LEFT_CURLY_BRACE`   |`KC.LCBR`          |`{`                |
|`KC.RIGHT_CURLY_BRACE`  |`KC.RCBR`          |`}`                |
|`KC.PIPE`               |                   |<code>&#124;</code>|
|`KC.COLON`              |`KC.COLN`          |`:`                |
|`KC.DOUBLE_QUOTE`       |`KC.DQUO`, `KC.DQT`|`"`                |
|`KC.LEFT_ANGLE_BRACKET` |`KC.LABK`, `KC.LT` |`<`                |
|`KC.RIGHT_ANGLE_BRACKET`|`KC.RABK`, `KC.GT` |`>`                |
|`KC.QUESTION`           |`KC.QUES`          |`?`                |


## [Internal Keycodes]

|Key          |Aliases    |Description                                                          |
|-------------|-----------|---------------------------------------------------------------------|
|`RESET`      |           |Put the keyboard into DFU mode for flashing                          |
|`DEBUG`      |           |Toggle debug mode                                                    |
|`KC.GESC`    |`GRAVE.ESC`|Escape when tapped, <code>&#96;</code> when pressed with Shift or GUI|
|`KC.LEAD`    |           |The [Leader key](feature_leader_key.md)                              |


## [Layer Switching]

|Key         |Description                                                               |
|-----------------|---------------------------------------------------------------------|
|`KC.DF(layer)`      |Switches the default layer                                           |
|`KC.MO(layer)`      |Momentarily activates layer, switches off when you let go            |
|`KC.LM(layer, mod)` |As `MO(layer)` but with `mod` active                                 |
|`KC.LT(layer, kc)`  |Momentarily activates layer if held, sends kc if tapped              |
|`KC.TG(layer)`      |Toggles the layer (enables it if no active, and vise versa)          |
|`KC.TO(layer)`      |Activates layer and deactivates all other layers                     |
|`KC.TT(layer)`      |Momentarily activates layer if held, toggles it if tapped repeatedly |


## [Backlighting] NOT IMPLEMENTED AT THIS TIME

|Key      |Description                               |
|---------|------------------------------------------|
|`BL.TOGG`|Turn the backlight on or off              |
|`BL.STEP`|Cycle through backlight levels            |
|`BL.ON`  |Set the backlight to max brightness       |
|`BL.OFF` |Turn the backlight off                    |
|`BL.INC` |Increase the backlight level              |
|`BL.DEC` |Decrease the backlight level              |
|`BL.BRTG`|Toggle backlight breathing                |


## [Bluetooth] NOT IMPLEMENTED AT THIS TIME

|Key       |Description                                   |
|----------|----------------------------------------------|
|`OUT.AUTO`|Automatically switch between USB and Bluetooth|
|`OUT.USB` |USB only                                      |
|`OUT.BT`  |Bluetooth only                                |


## [Mouse Keys] NOT IMPLEMENTED AT THIS TIME

|Key             |Aliases  |Description                |
|----------------|---------|---------------------------|
|`KC.MS_UP`      |`KC.MS_U`|Mouse Cursor Up            |
|`KC.MS_DOWN`    |`KC.MS_D`|Mouse Cursor Down          |
|`KC.MS_LEFT`    |`KC.MS_L`|Mouse Cursor Left          |
|`KC.MS_RIGHT`   |`KC.MS_R`|Mouse Cursor Right         |
|`KC.MS_BTN1`    |`KC.BTN1`|Mouse Button 1             |
|`KC.MS_BTN2`    |`KC.BTN2`|Mouse Button 2             |
|`KC.MS_BTN3`    |`KC.BTN3`|Mouse Button 3             |
|`KC.MS_BTN4`    |`KC.BTN4`|Mouse Button 4             |
|`KC.MS_BTN5`    |`KC.BTN5`|Mouse Button 5             |
|`KC.MS_WH_UP`   |`KC.WH_U`|Mouse Wheel Up             |
|`KC.MS_WH_DOWN` |`KC.WH_D`|Mouse Wheel Down           |
|`KC.MS_WH_LEFT` |`KC.WH_L`|Mouse Wheel Left           |
|`KC.MS_WH_RIGHT`|`KC.WH_R`|Mouse Wheel Right          |
|`KC.MS_ACCEL0`  |`KC.ACL0`|Set mouse acceleration to 0|
|`KC.MS_ACCEL1`  |`KC.ACL1`|Set mouse acceleration to 1|
|`KC.MS_ACCEL2`  |`KC.ACL2`|Set mouse acceleration to 2|


## [Modifiers] NOT IMPLEMENTED AT THIS TIME

|Key       |Aliases               |Description                                         |
|----------|----------------------|----------------------------------------------------|
|`KC.HYPR` |                      |Hold Left Control, Shift, Alt and GUI               |
|`KC.MEH`  |                      |Hold Left Control, Shift and Alt                    |
|`LCTL(kc)`|                      |Hold Left Control and press `kc`                    |
|`LSFT(kc)`|`S(kc)`               |Hold Left Shift and press `kc`                      |
|`LALT(kc)`|                      |Hold Left Alt and press `kc`                        |
|`LGUI(kc)`|`LCMD(kc)`, `LWIN(kc)`|Hold Left GUI and press `kc`                        |
|`RCTL(kc)`|                      |Hold Right Control and press `kc`                   |
|`RSFT(kc)`|                      |Hold Right Shift and press `kc`                     |
|`RALT(kc)`|                      |Hold Right Alt and press `kc`                       |
|`RGUI(kc)`|`RCMD(kc)`, `LWIN(kc)`|Hold Right GUI and press `kc`                       |
|`HYPR(kc)`|                      |Hold Left Control, Shift, Alt and GUI and press `kc`|
|`MEH(kc)` |                      |Hold Left Control, Shift and Alt and press `kc`     |
|`LCAG(kc)`|                      |Hold Left Control, Alt and GUI and press `kc`       |
|`ALTG(kc)`|                      |Hold Right Control and Alt and press `kc`           |
|`SGUI(kc)`|`SCMD(kc)`, `SWIN(kc)`|Hold Left Shift and GUI and press `kc`              |
|`LCA(kc)` |                      |Hold Left Control and Alt and press `kc`            |


## [Mod-Tap Keys] NOT IMPLEMENTED AT THIS TIME

|Key         |Aliases                                |Description                                            |
|------------|---------------------------------------|-------------------------------------------------------|
|`LCTL_T(kc)`|`CTL_T(kc)`                            |Left Control when held, `kc` when tapped               |
|`RCTL_T(kc)`|                                       |Right Control when held, `kc` when tapped              |
|`LSFT_T(kc)`|`SFT_T(kc)`                            |Left Shift when held, `kc` when tapped                 |
|`RSFT_T(kc)`|                                       |Right Shift when held, `kc` when tapped                |
|`LALT_T(kc)`|`ALT_T(kc)`                            |Left Alt when held, `kc` when tapped                   |
|`RALT_T(kc)`|`ALGR_T(kc)`                           |Right Alt when held, `kc` when tapped                  |
|`LGUI_T(kc)`|`LCMD_T(kc)`, `RWIN_T(kc)`, `GUI_T(kc)`|Left GUI when held, `kc` when tapped                   |
|`RGUI_T(kc)`|`RCMD_T(kc)`, `RWIN_T(kc)`             |Right GUI when held, `kc` when tapped                  |
|`C_S_T(kc)` |                                       |Left Control and Shift when held, `kc` when tapped     |
|`MEH_T(kc)` |                                       |Left Control, Shift and Alt when held, `kc` when tapped|
|`LCAG_T(kc)`|                                       |Left Control, Alt and GUI when held, `kc` when tapped  |
|`RCAG_T(kc)`|                                       |Right Control, Alt and GUI when held, `kc` when tapped |
|`ALL_T(kc)` |                                       |Left Control, Shift, Alt and GUI when held, `kc` when tapped - more info [here](http://brettterpstra.com/2012/12/08/a-useful-caps-lock-key/)|
|`SGUI_T(kc)`|`SCMD_T(kc)`, `SWIN_T(kc)`             |Left Shift and GUI when held, `kc` when tapped         |
|`LCA_T(kc)` |                                       |Left Control and Alt when held, `kc` when tapped       |


## [RGB Lighting] NOT IMPLEMENTED AT THIS TIME

|Key                |Aliases   |Description                                                         |
|-------------------|----------|--------------------------------------------------------------------|
|`RGB.TOG`          |          |Toggle RGB lighting on or off                                       |
|`RGB.MODE_FORWARD` |`RGB.MOD` |Cycle through modes, reverse direction when Shift is held           |
|`RGB.MODE_REVERSE` |`RGB.RMOD`|Cycle through modes in reverse, forward direction when Shift is held|
|`RGB.HUI`          |          |Increase hue                                                        |
|`RGB.HUD`          |          |Decrease hue                                                        |
|`RGB.SAI`          |          |Increase saturation                                                 |
|`RGB.SAD`          |          |Decrease saturation                                                 |
|`RGB.VAI`          |          |Increase value (brightness)                                         |
|`RGB.VAD`          |          |Decrease value (brightness)                                         |
|`RGB.MODE_PLAIN`   |`RGB.M_P `|Static (no animation) mode                                          |
|`RGB.MODE_BREATHE` |`RGB.M_B` |Breathing animation mode                                            |
|`RGB.MODE_RAINBOW` |`RGB.M_R` |Rainbow animation mode                                              |
|`RGB.MODE_SWIRL`   |`RGB.M_SW`|Swirl animation mode                                                |
|`RGB.MODE_SNAKE`   |`RGB.M_SN`|Snake animation mode                                                |
|`RGB.MODE_KNIGHT`  |`RGB.M_K` |"Knight Rider" animation mode                                       |
|`RGB.MODE_XMAS`    |`RGB.M_X` |Christmas animation mode                                            |
|`RGB.MODE_GRADIENT`|`RGB.M_G` |Static gradient animation mode                                      |
|`RGB.MODE_RGBTEST` |`RGB.M_T` |Red,Green,Blue test animation mode                                  |


## [RGB Matrix Lighting] NOT IMPLEMENTED AT THIS TIME

|Key                |Aliases   |Description                                                         |
|-------------------|----------|--------------------------------------------------------------------|
|`RGB.TOG`          |          |Toggle RGB lighting on or off                                       |
|`RGB.MODE_FORWARD` |`RGB.MOD` |Cycle through modes, reverse direction when Shift is held           |
|`RGB.MODE_REVERSE` |`RGB.RMOD`|Cycle through modes in reverse, forward direction when Shift is held|
|`RGB.HUI`          |          |Increase hue                                                        |
|`RGB.HUD`          |          |Decrease hue                                                        |
|`RGB.SAI`          |          |Increase saturation                                                 |
|`RGB.SAD`          |          |Decrease saturation                                                 |
|`RGB.VAI`          |          |Increase value (brightness)                                         |
|`RGB.VAD`          |          |Decrease value (brightness)                                         |
|`RGB.SPI`          |          |Increase effect speed (does no support eeprom yet)                  |
|`RGB.SPD`          |          |Decrease effect speed (does no support eeprom yet)                  |


## [One Shot Keys] NOT IMPLEMENTED AT THIS TIME

|Key         |Description                       |
|------------|----------------------------------|
|`OSM(mod)`  |Hold `mod` for one keypress       |
|`OSL(layer)`|Switch to `layer` for one keypress|


## [Swap Hands] NOT IMPLEMENTED AT THIS TIME

|Key        |Description                                                              |
|-----------|-------------------------------------------------------------------------|
|`SH.T(key)`|Sends `key` with a tap; momentary swap when held.                        |
|`SW.ON`    |Turns on swapping and leaves it on.                                      |
|`SW.OFF`   |Turn off swapping and leaves it off. Good for returning to a known state.|
|`SH.MON`   |Swaps hands when pressed, returns to normal when released (momentary).   |
|`SH.MOFF`  |Momentarily turns off swap.                                              |
|`SH.TG`    |Toggles swap on and off with every key press.                            |
|`SH.TT`    |Toggles with a tap; momentary when held.                                 |


## [Unicode Support] NOT IMPLEMENTED AT THIS TIME

|Key         |Aliases|                                                 |
|------------|-------|-------------------------------------------------|
|`UNICODE(n)`|`UC(n)`|Send Unicode character `n`                       |
|`X(n)`      |       |Send Unicode character `n` via a different method|
