

def get_players_grid_refs(players):
    """ Returns a list of players' currently occupied grid refs """
    grid_refs = []
    for player in players:
        grid_refs.append(player.get_grid_ref())
    return grid_refs