
WINDOWSIZE = (1600, 900)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
BOUNDSX = (WINDOWSIZE[0] / 4, WINDOWSIZE[0] * 3 / 4)
BOUNDSY = (WINDOWSIZE[1] / 3, WINDOWSIZE[1] * 2 / 3)
CHUNKSIZE = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
TILESIZE = 50
MAXSPEED = 2
FRICTION = 0.008

SEED = 2763492

COLORS = {
    "light_green": (100, 230, 140),
    "dark_green": (70, 180, 110),
    "light_blue": (100, 170, 230)
}

CHUNKSHIFT = {
	-1: range(-1, 3, 1),
    0: range(-1, 3, 1),
	1: range(2, -2, -1)
}


def muliply(list1, list2):
    return([list1[0] * list2[0], list1[1] * list2[1]])

def add(list1, list2):
    return([list1[0] + list2[0], list1[1] + list2[1]])

def subtract(list1, list2):
    return([list1[0] - list2[0], list1[1] - list2[1]])

