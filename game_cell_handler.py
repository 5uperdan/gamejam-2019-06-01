from gameobjects import Capitalist_Cell, Capturable_Cell, Socialist_Cell, Neutral_Cell


def capitalise_cell(cells, target_grid_ref):
    """ capitalisation player has actioned cell """
    cell = cells.get(target_grid_ref, None)
    if cell is None:
        return

    if type(cell) is Capitalist_Cell:
        return
    if type(cell) is Neutral_Cell:
        cells[target_grid_ref] = Capitalist_Cell(target_grid_ref)
    if type(cell) is Socialist_Cell:
        cell.is_hindered = True


def socialise_cell(cells, target_grid_ref):
    """ capitalisation player has actioned cell """
    cell = cells.get(target_grid_ref, None)
    if cell is None:
        return

    if type(cell) is Socialist_Cell:
        return
    if type(cell) is Neutral_Cell:
        cells[target_grid_ref] = Socialist_Cell(target_grid_ref)
    if type(cell) is Capitalist_Cell:
        cell.is_hindered = True