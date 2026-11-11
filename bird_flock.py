from math import cos, pi

ROUND_TRIP_SECONDS = 12.0


def patrol_x(elapsed, left, right):
    half_trip = ROUND_TRIP_SECONDS / 2
    cycle_time = elapsed % ROUND_TRIP_SECONDS
    progress = (1 - cos(pi * cycle_time / half_trip)) / 2
    facing = 1 if cycle_time < half_trip else -1
    return left + (right - left) * progress, facing
