from gameobjects import Capitalist_Cell, Capturable_Cell, Socialist_Cell


def capitalise_cell(cells, target_grid_ref):
    """ capitalisation player has actioned cell,
    returns True if energy was spent """
    cell = cells.get(target_grid_ref, None)
    if cell is None:
        return False

    if type(cell) is Capitalist_Cell:
        return False
    if type(cell) is Capturable_Cell:
        cells[target_grid_ref] = Capitalist_Cell(target_grid_ref)
        return True
    if type(cell) is Socialist_Cell:
        cell.is_hindered = True
        return True


def socialise_cell(cells, target_grid_ref):
    """ capitalisation player has actioned cell,
    returns True if energy was spent """
    cell = cells.get(target_grid_ref, None)
    if cell is None:
        return False

    if type(cell) is Socialist_Cell:
        return False
    if type(cell) is Capturable_Cell:
        cells[target_grid_ref] = Socialist_Cell(target_grid_ref)
        return True
    if type(cell) is Capitalist_Cell:
        cell.is_hindered = True
        return True