# These are initialisation sequences for ST7701S displays. The contents are somewhat arcane.


def cmd(c, *args):
    """
    Create a command sequence
    :param c: The command (8 bit)
    :param args: zero or more arguments (8 bit values)
    :return: a list with the command, the argument count and the arguments
    """
    return [c, len(args)] + list(args)


ST7701S_1_INIT = (
    cmd(0x01)
    + cmd(0xFF, 0x77, 0x01, 0x00, 0x00, 0x10)
    + cmd(0xC0, 0x3B, 0x00)
    + cmd(0xC1, 0x0D, 0x02)
    + cmd(0xC2, 0x31, 0x05)
    + cmd(0xCD, 0x08)
    + cmd(
        0xB0,
        0x00,
        0x11,
        0x18,
        0x0E,
        0x11,
        0x06,
        0x07,
        0x08,
        0x07,
        0x22,
        0x04,
        0x12,
        0x0F,
        0xAA,
        0x31,
        0x18,
    )
    + cmd(
        0xB1,
        0x00,
        0x11,
        0x19,
        0x0E,
        0x12,
        0x07,
        0x08,
        0x08,
        0x08,
        0x22,
        0x04,
        0x11,
        0x11,
        0xA9,
        0x32,
        0x18,
    )
    + cmd(0xFF, 0x77, 0x01, 0x00, 0x00, 0x11)
    + cmd(0xB0, 0x60)
    + cmd(0xB1, 0x32)
    + cmd(0xB2, 0x07)
    + cmd(0xB3, 0x80)
    + cmd(0xB5, 0x49)
    + cmd(0xB7, 0x85)
    + cmd(0xB8, 0x21)
    + cmd(0xC1, 0x78)
    + cmd(0xC2, 0x78)
    + cmd(0xE0, 0x00, 0x1B, 0x02)
    + cmd(0xE1, 0x08, 0xA0, 0x00, 0x00, 0x07, 0xA0, 0x00, 0x00, 0x00, 0x44, 0x44)
    + cmd(0xE2, 0x11, 0x11, 0x44, 0x44, 0xED, 0xA0, 0x00, 0x00, 0xEC, 0xA0, 0x00, 0x00)
    + cmd(0xE3, 0x00, 0x00, 0x11, 0x11)
    + cmd(0xE4, 0x44, 0x44)
    + cmd(
        0xE5,
        0x0A,
        0xE9,
        0xD8,
        0xA0,
        0x0C,
        0xEB,
        0xD8,
        0xA0,
        0x0E,
        0xED,
        0xD8,
        0xA0,
        0x10,
        0xEF,
        0xD8,
        0xA0,
    )
    + cmd(0xE6, 0x00, 0x00, 0x11, 0x11)
    + cmd(0xE7, 0x44, 0x44)
    + cmd(
        0xE8,
        0x09,
        0xE8,
        0xD8,
        0xA0,
        0x0B,
        0xEA,
        0xD8,
        0xA0,
        0x0D,
        0xEC,
        0xD8,
        0xA0,
        0x0F,
        0xEE,
        0xD8,
        0xA0,
    )
    + cmd(0xEB, 0x02, 0x00, 0xE4, 0xE4, 0x88, 0x00, 0x40)
    + cmd(0xEC, 0x3C, 0x00)
    + cmd(
        0xED,
        0xAB,
        0x89,
        0x76,
        0x54,
        0x02,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0x20,
        0x45,
        0x67,
        0x98,
        0xBA,
    )
    + cmd(0xFF, 0x77, 0x01, 0x00, 0x00, 0x13)
    + cmd(0xE5, 0xE4)
    + cmd(0x3A, 0x60)
)

# This is untested
ST7701S_7_INIT = (
    cmd(
        0xFF,
        0x77,
        0x01,
        0x00,
        0x00,
        0x10,
    )
    + cmd(0xC0, 0x3B, 0x00)
    + cmd(0xC1, 0x0B, 0x02)
    + cmd(0xC2, 0x07, 0x02)
    + cmd(0xCC, 0x10)
    + cmd(0xCD, 0x08)
    + cmd(
        0xB0,
        0x00,
        0x11,
        0x16,
        0x0E,
        0x11,
        0x06,
        0x05,
        0x09,
        0x08,
        0x21,
        0x06,
        0x13,
        0x10,
        0x29,
        0x31,
        0x18,
    )
    + cmd(
        0xB1,
        0x00,
        0x11,
        0x16,
        0x0E,
        0x11,
        0x07,
        0x05,
        0x09,
        0x09,
        0x21,
        0x05,
        0x13,
        0x11,
        0x2A,
        0x31,
        0x18,
    )
    + cmd(
        0xFF,
        0x77,
        0x01,
        0x00,
        0x00,
        0x11,
    )
    + cmd(0xB0, 0x6D)
    + cmd(0xB1, 0x37)
    + cmd(0xB2, 0x81)
    + cmd(0xB3, 0x80)
    + cmd(0xB5, 0x43)
    + cmd(0xB7, 0x85)
    + cmd(0xB8, 0x20)
    + cmd(0xC1, 0x78)
    + cmd(0xC2, 0x78)
    + cmd(0xD0, 0x88)
    + cmd(
        0xE0,
        3,
        0x00,
        0x00,
        0x02,
    )
    + cmd(
        0xE1,
        0x03,
        0xA0,
        0x00,
        0x00,
        0x04,
        0xA0,
        0x00,
        0x00,
        0x00,
        0x20,
        0x20,
    )
    + cmd(
        0xE2,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    )
    + cmd(
        0xE3,
        0x00,
        0x00,
        0x11,
        0x00,
    )
    + cmd(0xE4, 0x22, 0x00)
    + cmd(
        0xE5,
        0x05,
        0xEC,
        0xA0,
        0xA0,
        0x07,
        0xEE,
        0xA0,
        0xA0,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    )
    + cmd(
        0xE6,
        0x00,
        0x00,
        0x11,
        0x00,
    )
    + cmd(0xE7, 0x22, 0x00)
    + cmd(
        0xE8,
        0x06,
        0xED,
        0xA0,
        0xA0,
        0x08,
        0xEF,
        0xA0,
        0xA0,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    )
    + cmd(
        0xEB,
        0x00,
        0x00,
        0x40,
        0x40,
        0x00,
        0x00,
        0x00,
    )
    + cmd(
        0xED,
        0xFF,
        0xFF,
        0xFF,
        0xBA,
        0x0A,
        0xBF,
        0x45,
        0xFF,
        0xFF,
        0x54,
        0xFB,
        0xA0,
        0xAB,
        0xFF,
        0xFF,
        0xFF,
    )
    + cmd(
        0xEF,
        0x10,
        0x0D,
        0x04,
        0x08,
        0x3F,
        0x1F,
    )
    + cmd(
        0xFF,
        0x77,
        0x01,
        0x00,
        0x00,
        0x13,
    )
    + cmd(0xEF, 0x08)
    + cmd(
        0xFF,
        0x77,
        0x01,
        0x00,
        0x00,
        0x00,
    )
    + cmd(0x3A, 0x66)
)

ST7701S_INITS = {
    1: ST7701S_1_INIT,
    # 7: ST7701S_7_INIT,
}
