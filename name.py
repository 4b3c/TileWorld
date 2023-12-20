import random

vowels = ["a", "e", "i", "o", "u"]
consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

def random_name(name_length=random.randint(3, 6)):
	name = ""
	start = random.choice(("v", "c"))
	for i in range(name_length):
		if start == "v":
			name += random.choice(vowels)
			start = "c"
		elif start == "c":
			pick = random.choice(consonants)
			name += pick
			if pick == "c" or pick == "s" or pick == "t":
				start == random.choice(("v", "h"))
			else:
				start = random.choice(("v", "v", "v", "r"))
		elif start == "r":
			name += name[-1]
			start = "v"
		elif start == "h":
			name += "h"
			start = "v"

	if name[-1] in consonants:
		if random.randint(1, 5) == 1:
			name += "e"

	return name
