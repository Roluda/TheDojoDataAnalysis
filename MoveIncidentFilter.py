
def totalMovesFiltered(self):
    """sum of each individual move in the filtered data.

    return a dictionary"""

    dict = {}
    for move in self.movesFiltered:
        if move.get("name") not in dict.keys():
            dict[move.get("name")] = 1
        else:
            dict[move.get("name")] += 1

    return dict




