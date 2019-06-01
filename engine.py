class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        cells = {}
        for x, y in zip(range(10), range(10)):
            cells.append(x, y) = None