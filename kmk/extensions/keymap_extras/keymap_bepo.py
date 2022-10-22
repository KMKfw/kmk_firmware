from kmk.extensions.keymap_extras.base import KeyMapConverter
from kmk.keys import KC


class BEPO(KeyMapConverter):
    MAPPING = {
        # Row 1
        'DOLLAR': KC.GRV,  # $
        'DQUOTE': KC.N1,  # "
        'LDAQ': KC.N2,  # «
        'RDAQ': KC.N3,  # »
        'LPRN': KC.N4,  # (
        'RPRN': KC.N5,  # )
        'AT': KC.N6,  # @
        'PLUS': KC.N7,  # +
        'MINUS': KC.N8,  # -
        'SLASH': KC.N9,  # /
        'ASTERISK': KC.N0,  # *
        'EQUAL': KC.MINS,  # =
        'PERCENT': KC.EQL,  # %
        # Row 2
        'B': KC.Q,  # B
        'EACUTE': KC.W,  # É
        'P': KC.E,  # P
        'O': KC.R,  # O
        'EGRAVE': KC.T,  # È
        'DCIR': KC.Y,  # ^ (dead)
        'V': KC.U,  # V
        'D': KC.I,  # D
        'L': KC.O,  # L
        'J': KC.P,  # J
        'Z': KC.LBRC,  # Z
        'W': KC.RBRC,  # W
        # Row 3
        'A': KC.A,  # A
        'U': KC.S,  # U
        'I': KC.D,  # I
        'E': KC.F,  # E
        'COMM': KC.G,  # ,
        'COMMA': KC.G,  # ,
        'C': KC.H,  # C
        'T': KC.J,  # T
        'S': KC.K,  # S
        'R': KC.L,  # R
        'N': KC.SCLN,  # N
        'M': KC.QUOT,  # M
        'CCED': KC.BSLS,  # Ç
        # Row 4
        'ECIR': KC.NUBS,  # Ê
        'AGRAVE': KC.Z,  # À
        'Y': KC.X,  # Y
        'X': KC.C,  # X
        'DOT': KC.V,  # .
        'K': KC.B,  # K
        'QUOTE': KC.N,  # '
        'Q': KC.M,  # Q
        'G': KC.COMM,  # G
        'H': KC.DOT,  # H
        'F': KC.SLSH,  # F
        # Shifted symbols
        # Row 1
        'HASH': KC.LSFT(KC.GRV),  # #
        'N1': KC.LSFT(KC.N1),  # 1
        'N2': KC.LSFT(KC.N2),  # 2
        'N3': KC.LSFT(KC.N3),  # 3
        'N4': KC.LSFT(KC.N4),  # 4
        'N5': KC.LSFT(KC.N5),  # 5
        'N6': KC.LSFT(KC.N6),  # 6
        'N7': KC.LSFT(KC.N7),  # 7
        'N8': KC.LSFT(KC.N8),  # 8
        'N9': KC.LSFT(KC.N9),  # 9
        'N0': KC.LSFT(KC.N0),  # 0
        'DEG': KC.LSFT(KC.MINS),  # °
        'GRAVE': KC.LSFT(KC.EQL),  # `
        # Row 2
        'EXLM': KC.LSFT(KC.Y),  # !
        # Row 3
        'SCLN': KC.LSFT(KC.G),  # ;
        # Row 4
        'COLN': KC.LSFT(KC.V),  # :
        'QUES': KC.LSFT(KC.N),  # ?
        # Row 5
        'NBSP': KC.LSFT(KC.SPC),  # (non-breaking space)
        # AltGr symbols
        # Row 1
        'NDSH': KC.RALT(KC.GRV),  # –
        'MDSH': KC.RALT(KC.N1),  # —
        'LESS': KC.RALT(KC.N2),  # <
        'GRTR': KC.RALT(KC.N3),  # >
        'LBRC': KC.RALT(KC.N4),  # [
        'RBRC': KC.RALT(KC.N5),  # ]
        'CIRC': KC.RALT(KC.N6),  # ^
        'PLMN': KC.RALT(KC.N7),  # ±
        'MMNS': KC.RALT(KC.N8),  # −
        'DIV': KC.RALT(KC.N9),  # ÷
        'MUL': KC.RALT(KC.N0),  # ×
        'NEQL': KC.RALT(KC.MINS),  # ≠
        'PERM': KC.RALT(KC.EQL),  # ‰
        # Row 2
        'PIPE': KC.RALT(KC.Q),  # |
        'DACUTE': KC.RALT(KC.W),  # ´ (dead)
        'AMPR': KC.RALT(KC.E),  # &
        'OE': KC.RALT(KC.R),  # Œ
        'DGRAVE': KC.RALT(KC.T),  # ` (dead)
        'IEXL': KC.RALT(KC.Y),  # ¡
        'CARN': KC.RALT(KC.U),  # ˇ (dead)
        'ETH': KC.RALT(KC.I),  # Ð
        'DSLS': KC.RALT(KC.O),  # / (dead)
        'IJ': KC.RALT(KC.P),  # Ĳ
        'SCHW': KC.RALT(KC.LBRC),  # Ə
        'BREV': KC.RALT(KC.RBRC),  # ˘ (dead)
        # Row 3
        'AE': KC.RALT(KC.A),  # Æ
        'UGRAVE': KC.RALT(KC.S),  # Ù
        'DTREMA': KC.RALT(KC.D),  # ¨ (dead)
        'EURO': KC.RALT(KC.F),  # €
        'COPY': KC.RALT(KC.H),  # ©
        'THRN': KC.RALT(KC.J),  # Þ
        'SS': KC.RALT(KC.K),  # ẞ
        'REGD': KC.RALT(KC.L),  # ®
        'DTIL': KC.RALT(KC.SCLN),  # ~ (dead)
        'MACR': KC.RALT(KC.QUOTE),  # ¯ (dead)
        'CEDL': KC.RALT(KC.BSLS),  # ¸ (dead)
        # Row 4
        'BSLS': KC.RALT(KC.Z),  # (backslash)
        'LCBR': KC.RALT(KC.X),  # {
        'RCBR': KC.RALT(KC.C),  # }
        'ELLP': KC.RALT(KC.V),  # …
        'TILD': KC.RALT(KC.B),  # ~
        'IQUE': KC.RALT(KC.LSFT(KC.N)),  # ¿
        'RNGA': KC.RALT(KC.M),  # ° (dead)
        'DGRK': KC.RALT(KC.COMM),  # µ (dead Greek key)
        'DAGG': KC.RALT(KC.DOT),  # †
        'OGON': KC.RALT(KC.SLSH),  # ˛ (dead)
        # Row 5
        'UNDS': KC.RALT(KC.SPC),  # _
        # Shift+AltGr symbols
        # Row 1
        'PARA': KC.LSFT(KC.RALT(KC.GRV)),  # ¶
        'DLQU': KC.LSFT(KC.RALT(KC.N1)),  # „
        'LDQU': KC.LSFT(KC.RALT(KC.N2)),  # “
        'RDQU': KC.LSFT(KC.RALT(KC.N3)),  # ”
        'LEQL': KC.LSFT(KC.RALT(KC.N4)),  # ≤
        'GEQL': KC.LSFT(KC.RALT(KC.N5)),  # ≥
        'NOT': KC.LSFT(KC.RALT(KC.N7)),  # ¬
        'QRTR': KC.LSFT(KC.RALT(KC.N8)),  # ¼
        'HALF': KC.LSFT(KC.RALT(KC.N9)),  # ½
        'TQTR': KC.LSFT(KC.RALT(KC.N0)),  # ¾
        'PRIM': KC.LSFT(KC.RALT(KC.MINS)),  # ′
        'DPRM': KC.LSFT(KC.RALT(KC.EQL)),  # ″
        # Row 2
        'BRKP': KC.LSFT(KC.RALT(KC.Q)),  # ¦
        'DACU': KC.LSFT(KC.RALT(KC.W)),  # ˝ (dead)
        'SECT': KC.LSFT(KC.RALT(KC.E)),  # §
        # Row 3
        'DOTA': KC.LSFT(KC.RALT(KC.D)),  # ˙ (dead)
        'CURR': KC.LSFT(KC.RALT(KC.F)),  # ¤ (dead)
        'HORN': KC.LSFT(KC.RALT(KC.G)),  # ̛  (dead)
        'LNGS': KC.LSFT(KC.RALT(KC.H)),  # ſ
        'TM': KC.LSFT(KC.RALT(KC.L)),  # ™
        'MORD': KC.LSFT(KC.RALT(KC.QUOTE)),  # º
        'DCMM': KC.LSFT(KC.RALT(KC.BSLS)),  # , (dead)
        # Row 4
        'LSQU': KC.LSFT(KC.RALT(KC.X)),  # ‘
        'TAPO': KC.LSFT(KC.RALT(KC.C)),  # ’
        'MDDT': KC.LSFT(KC.RALT(KC.V)),  # ·
        'KEYB': KC.LSFT(KC.RALT(KC.B)),  # ⌨
        'HOKA': KC.LSFT(KC.RALT(KC.N)),  # ̉  (dead)
        'DOTB': KC.LSFT(KC.RALT(KC.M)),  # ̣  (dead)
        'DDAG': KC.LSFT(KC.RALT(KC.DOT)),  # ‡
        'FORD': KC.LSFT(KC.RALT(KC.SLSH)),  # ª
    }
