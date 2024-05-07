# from game_world.chunk import Chunk

# import time
# lasttime = time.time()
# for i in range(200):
# 	Chunk((0, i))


# print(time.time() - lasttime)


# my_dict = {
#     (0, 0): 0,
#     (0, 1): 0,
#     (0, 2): 0,
#     (1, 0): 0,
#     (1, 1): 0,
#     (1, 2): 0,
#     (2, 0): 0,
#     (2, 1): 0,
#     (2, 2): 0
# }

# keys = my_dict.keys()
# x, y = -1, 0
# keys_plus = [(key[0] + x, key[1] + y) for key in keys]
# to_add = [key for key in keys_plus if key not in keys]

# keys_minus = [(key[0] - x, key[1] - y) for key in keys]
# to_remove = [(key[0] + x, key[1] + y) for key in keys_minus if key not in keys]

# print(keys)
# print(keys_plus)
# print(to_add)
# print(to_remove)


list1 = [0, 1, 2, 3, 4, 5]

print(list1[-2:1:1])