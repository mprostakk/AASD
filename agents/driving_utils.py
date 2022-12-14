from math import sqrt
from typing import List

import numpy as np
from schemas import Position
from zones_const import STAFF_ZONE, PUBLIC_ZONE, SAFE_ZONE


def drive_positions(source: Position, destination: Position) -> List[Position]:
    length = sqrt(abs(source.x - destination.x) + abs(source.y - destination.y))
    length = int(length) * 7

    positions_x = [int(x) for x in np.linspace(source.x, destination.x, num=length)]
    positions_y = [int(y) for y in np.linspace(source.y, destination.y, num=length)]

    return [Position(x=p[0], y=p[1]) for p in zip(positions_x, positions_y)]


def is_allowed_position(position: Position, allowed_zones: List[str]) -> bool:
    if 30 < position.x < 1200 and 30 < position.y < 1170:
        return PUBLIC_ZONE in allowed_zones
    elif 1200 < position.x < 2170 and 30 < position.y < 700:
        return STAFF_ZONE in allowed_zones
    elif 1200 < position.x < 2170 and 700 < position.y < 1170:
        return SAFE_ZONE in allowed_zones

    return False
