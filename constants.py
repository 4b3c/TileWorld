import random

WINDOWSIZE = (1600, 900)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
CHUNKSIZE = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
TILESIZE = 50
MAXSPEED = 2
FRICTION = 0.008

SEED = 2763492
SAVEFOLDER = "worlds/"

COLORS = {
    "light_green": (100, 230, 140),
    "dark_green": (70, 180, 110),
    "light_blue": (100, 170, 230),
    "light_grey": (40, 40, 40)
}

CHUNKSHIFT = {
	-1: range(2, -2, -1),
    0: range(-1, 3, 1),
	1: range(-1, 3, 1)
}


def muliply(list1, list2):
    return([list1[0] * list2[0], list1[1] * list2[1]])

def add(list1, list2):
    return([list1[0] + list2[0], list1[1] + list2[1]])

def subtract(list1, list2):
    return([list1[0] - list2[0], list1[1] - list2[1]])

def strtup(string: str):
    try:
        return int(string[1:string.index(",")]), int(string[string.index(" "):-1])
    except:
        print(string)
        quit()
