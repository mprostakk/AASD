from math import sqrt
from typing import List

import numpy as np
from schemas import Position


def drive_positions(source: Position, destination: Position) -> List[Position]:
    length = sqrt(abs(source.x - destination.x) + abs(source.y - destination.y))
    length = int(length) * 5

    positions_x = [int(x) for x in np.linspace(source.x, destination.x, num=length)]
    positions_y = [int(y) for y in np.linspace(source.y, destination.y, num=length)]

    return [Position(x=p[0], y=p[1]) for p in zip(positions_x, positions_y)]


def is_position_on_board(position: Position):
    if 10 < position.x < 1000 and 10 < position.y < 1000:
        return True

    return False
