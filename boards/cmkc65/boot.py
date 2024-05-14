import board

from kmk.bootcfg import bootcfg

bootcfg(
    sense=board.P0_11,  # column
    #source=board.GP8, # row
    midi=False,
    mouse=False,
    storage=True,
    usb_id=('KMK Keyboards', 'CMKC 65%'),
)
