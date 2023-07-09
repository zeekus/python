import random
def space_themed_words():
    return [
        "sky",
        "moon",
        "star",
        "comet",
        "orbit",
        "lunar",
        "solar",
        "mars",
        "venus",
        "jupit",
        "pluto",
        "nebul",
        "cosmic",
        "meteor",
        "orbits",
        "comets",
        "saturn",
        "uranus",
        "neptune",
        "jupiter",
        "nebula",
        "planets",
        "galaxy",
        "cosmos",
        "bigbang",
        "gravity",
        "stellar",
        "quasars",
        "pulsars",
        "astronomy",
        "telescope",
        "blackhole",
    ]

def random_space_word():
    words = space_themed_words()
    return random.choice(words)

if __name__ == "__main__":
    word = random_space_word()
    print(word)
