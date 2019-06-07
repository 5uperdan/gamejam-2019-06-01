

def get_players_grids(players):
    """ Returns a list of players' currently occupied grid refs """
    grids = []
    for player in players:
        grids.append(player.get_grid())
    return grids