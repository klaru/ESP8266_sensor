# Code generated by font_to_py.py.
# Font: SF_Pixelate.ttf Char set:  %.0123456789:CEHLMOPTahlux°
# Cmd: font_to_py.py -x SF_Pixelate.ttf 8 SF_Pixelate.py -c 0123456789LPCOMETHluxhPa:% °.
version = '0.33'

def height():
    return 8

def baseline():
    return 8

def max_width():
    return 10

def hmap():
    return True

def reverse():
    return False

def monospaced():
    return False

def min_ch():
    return 32

def max_ch():
    return 176

_font =\
b'\x08\x00\x3c\x42\x42\x02\x3c\x40\x00\x40\x07\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x0a\x00\x22\x00\x52\x00\x24\x00\x24\x00\x08\x00'\
b'\x12\x00\x25\x00\x22\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x40'\
b'\x08\x00\x3c\x42\x42\x42\x42\x42\x42\x3c\x03\x00\x40\x40\x40\x40'\
b'\x40\x40\x40\x40\x08\x00\x3c\x42\x42\x02\x3c\x40\x40\x7e\x08\x00'\
b'\x3c\x42\x42\x02\x0c\x02\x42\x3c\x08\x00\x08\x08\x48\x48\x48\x7c'\
b'\x08\x08\x08\x00\x7e\x40\x40\x40\x3c\x02\x42\x3c\x08\x00\x3c\x42'\
b'\x42\x40\x7c\x42\x42\x3c\x08\x00\x7c\x04\x08\x10\x10\x20\x40\x40'\
b'\x08\x00\x3c\x42\x42\x42\x3c\x42\x42\x3c\x08\x00\x3c\x42\x42\x42'\
b'\x3e\x02\x42\x3c\x03\x00\x00\x00\x40\x00\x00\x00\x00\x40\x08\x00'\
b'\x3c\x42\x42\x02\x3c\x40\x00\x40\x08\x00\x3c\x42\x42\x40\x40\x40'\
b'\x42\x3c\x08\x00\x7c\x40\x40\x40\x7c\x40\x40\x7c\x08\x00\x42\x42'\
b'\x42\x42\x7e\x42\x42\x42\x08\x00\x40\x40\x40\x40\x40\x40\x40\x7c'\
b'\x0a\x00\x41\x00\x63\x00\x55\x00\x49\x00\x49\x00\x49\x00\x49\x00'\
b'\x49\x00\x08\x00\x3c\x42\x42\x42\x42\x42\x42\x3c\x08\x00\x7c\x42'\
b'\x42\x42\x7c\x40\x40\x40\x08\x00\x7c\x10\x10\x10\x10\x10\x10\x10'\
b'\x08\x00\x00\x00\x7c\x02\x02\x3e\x42\x3c\x08\x00\x40\x40\x7c\x42'\
b'\x42\x42\x42\x42\x03\x00\x40\x40\x40\x40\x40\x40\x40\x40\x08\x00'\
b'\x00\x00\x42\x42\x42\x42\x42\x3e\x08\x00\x00\x00\x44\x28\x28\x10'\
b'\x28\x44\x04\x00\x40\xe0\x00\x00\x00\x00\x00\x00'

_sparse =\
b'\x20\x00\x0a\x00\x25\x00\x14\x00\x2e\x00\x26\x00\x30\x00\x30\x00'\
b'\x31\x00\x3a\x00\x32\x00\x44\x00\x33\x00\x4e\x00\x34\x00\x58\x00'\
b'\x35\x00\x62\x00\x36\x00\x6c\x00\x37\x00\x76\x00\x38\x00\x80\x00'\
b'\x39\x00\x8a\x00\x3a\x00\x94\x00\x3f\x00\x9e\x00\x43\x00\xa8\x00'\
b'\x45\x00\xb2\x00\x48\x00\xbc\x00\x4c\x00\xc6\x00\x4d\x00\xd0\x00'\
b'\x4f\x00\xe2\x00\x50\x00\xec\x00\x54\x00\xf6\x00\x61\x00\x00\x01'\
b'\x68\x00\x0a\x01\x6c\x00\x14\x01\x75\x00\x1e\x01\x78\x00\x28\x01'\
b'\xb0\x00\x32\x01'

_mvfont = memoryview(_font)
_mvsp = memoryview(_sparse)
ifb = lambda l : l[0] | (l[1] << 8)

def bs(lst, val):
    while True:
        m = (len(lst) & ~ 7) >> 1
        v = ifb(lst[m:])
        if v == val:
            return ifb(lst[m + 2:])
        if not m:
            return 0
        lst = lst[m:] if v < val else lst[:m]

def get_ch(ch):
    doff = bs(_mvsp, ord(ch))
    width = ifb(_mvfont[doff : ])

    next_offs = doff + 2 + ((width - 1)//8 + 1) * 8
    return _mvfont[doff + 2:next_offs], 8, width
 