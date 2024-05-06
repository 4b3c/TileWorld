from game_world.chunk import Chunk

import time
lasttime = time.time()
for i in range(200):
	Chunk((0, i))


print(time.time() - lasttime)