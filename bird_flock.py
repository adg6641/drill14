from math import cos, pi, sin, tau

from pathlib import Path

from pico2d import get_canvas_height, get_canvas_width, load_image

import game_framework
from bird import Bird, MAX_HORIZONTAL_EXTENT

ROUND_TRIP_SECONDS = 12.0
EDGE_MARGIN = 24
# 위에서 아래로 3·4·3마리. 왕복할 때도 각 새의 상대적인 좌우 위치를 유지한다.
FORMATION = (
    (-106, 82), (0, 86), (106, 82),
    (-159, -2), (-53, 4), (53, 4), (159, -2),
    (-106, -86), (0, -82), (106, -86),
)


def patrol_x(elapsed, left, right):
    half_trip = ROUND_TRIP_SECONDS / 2
    cycle_time = elapsed % ROUND_TRIP_SECONDS
    progress = (1 - cos(pi * cycle_time / half_trip)) / 2
    facing = 1 if cycle_time < half_trip else -1
    return left + (right - left) * progress, facing


def flight_altitude(elapsed, cruising_height, phase):
    flock_rise = 14 * sin(tau * elapsed / 6.0)
    individual_rise = 5 * sin(tau * (elapsed / 2.1 + phase))
    return cruising_height + flock_rise + individual_rise


class BirdFlock:
    def __init__(self):
        sheet_path = Path(__file__).with_name('bird_animation.png')
        image = load_image(str(sheet_path))
        self.birds = [
            Bird(image, flap_phase=index / len(FORMATION))
            for index in range(len(FORMATION))
        ]
        half_width = max(abs(dx) for dx, _ in FORMATION) + MAX_HORIZONTAL_EXTENT
        self.left = EDGE_MARGIN + half_width
        self.right = get_canvas_width() - self.left
        self.cruising_height = get_canvas_height() * 0.64
        self.elapsed = 0.0

    def update(self):
        self.elapsed += game_framework.frame_time
        for bird in self.birds:
            bird.update(self.elapsed)

    def draw(self):
        center_x, facing = patrol_x(self.elapsed, self.left, self.right)
        for bird, (dx, dy) in zip(self.birds, FORMATION):
            y = flight_altitude(self.elapsed, self.cruising_height + dy, bird.flap_phase)
            bird.draw(center_x + dx, y, facing)
