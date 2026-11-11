from bird_animation import FRAMES

DRAW_SCALE = 0.5
FLAPS_PER_SECOND = 2.4
MAX_HORIZONTAL_EXTENT = max(
    (frame.width / 2 + abs(frame.anchor_dx)) * DRAW_SCALE
    for frame in FRAMES
)


class Bird:
    def __init__(self, image, flap_phase=0.0):
        self.image = image
        self.flap_phase = flap_phase
        self.frame_index = 0
        self.update(0.0)

    def update(self, elapsed):
        wing_cycle = (elapsed * FLAPS_PER_SECOND + self.flap_phase) % 1.0
        self.frame_index = int(wing_cycle * len(FRAMES))

    def draw(self, x, y, facing):
        frame = FRAMES[self.frame_index]
        # 뒤집을 때 몸통 기준점의 가로 보정 방향도 함께 바꾼다.
        self.image.clip_composite_draw(
            frame.left, frame.bottom, frame.width, frame.height,
            0, 'h' if facing < 0 else '',
            x - facing * frame.anchor_dx * DRAW_SCALE,
            y - frame.anchor_dy * DRAW_SCALE,
            frame.width * DRAW_SCALE, frame.height * DRAW_SCALE,
        )
