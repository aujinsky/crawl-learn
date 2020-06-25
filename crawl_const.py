PLAYER_NAME = "learn2crawl"
SCR_COL = 80
SCR_ROW = 40
SCR_MSG = 21
class key():
    UP = '\x1b[A'.encode()
    DOWN = '\x1b[B'.encode()
    RIGHT = '\x1b[C'.encode()
    LEFT = '\x1b[D'.encode()
    CTRLX = '\x18'.encode()
    CTRLS = '\x13'.encode()
    TAB = '\t'.encode()
    ESC = '\x1b'.encode()
# like a enum
PLACE = {"outside" : 0, "dungeon" : 1, "temple" : 2, "sewer" : 3, "ossuary" : 4,
        "lair" : 5, "orc" : 6, "bazaar" : 7, "bailey" : 8, "gauntlet" : 9, "volcano" : 10,
        "icecv" : 11, "swamp" : 12, "spider" : 13, "snake" : 14, "shoals" : 15, "elf" : 16,
        "vaults" : 17, "depths" : 18, "desolation" : 19, "wizlab" : 20, "zot" : 21, "abyss" : 22}
PEACE = 0
BATTLE = 1
GATHERINFO = 2


class MobInfo():
    HP = 0
    AC = 1
    EV = 2
    SH = 3
    MR = 4
    RFIRE = 5
    RCOLD = 6
    RNEG = 7
    RPOIS = 8
    RELEC = 9
    RCORR = 10
    SPD = 11
    ATTACK1 = 12
    COUNT1 = 13
    EGO1 = 14
    ATTACK2 = 15
    COUNT2 = 16
    EGO2 = 17
    ATTACK3 = 18
    COUNT3 = 19
    EGO3 = 20
    ABILITY = 21
    MOB_INFO_SIZE = 22
class ResMap():
    def __init__(self, res_str):
        if res_str == "MR_RES_FIRE":
            return MobInfo.RFIRE
        elif res_str == "MR_RES_COLD":
            return MobInfo.RCOLD
        elif res_str == "MR_RES_NEG":
            return MobInfo.RNEG
        elif res_str == "MR_RES_POISON":
            return MobInfo.RPOIS
        elif res_str == "MR_RES_ELEC":
            return MobInfo.RELEC
        elif res_str == "MR_RES_ACID":
            return MobInfo.RCORR
        else:
            return -1
