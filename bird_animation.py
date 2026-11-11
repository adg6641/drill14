from dataclasses import dataclass

SHEET_HEIGHT = 506
COLUMN_EDGES = (0, 182, 364, 546, 728, 918)
# PNG 위쪽 기준 행 경계와 각 자세에서 측정한 눈 중심의 y 좌표.
ROWS = (
    (0, 165, (93, 92, 91, 88, 85)),
    (165, 353, (254, 253, 253, 254, 256)),
    (353, 506, (429, 431, 432, 433)),
)
BODY_ANCHOR_X = 105
BODY_ANCHOR_BELOW_EYE = 20


@dataclass(frozen=True)
class SpriteFrame:
    left: int
    bottom: int
    width: int
    height: int
    anchor_dx: float
    anchor_dy: float


def _make_frame(column, top, lower_edge, eye_y):
    left = COLUMN_EDGES[column]
    width = COLUMN_EDGES[column + 1] - left
    height = lower_edge - top
    anchor_y = eye_y + BODY_ANCHOR_BELOW_EYE
    return SpriteFrame(
        left, SHEET_HEIGHT - lower_edge, width, height,
        BODY_ANCHOR_X - width / 2, top + height / 2 - anchor_y,
    )


FRAMES = tuple(
    _make_frame(column, top, lower_edge, eye_y)
    for top, lower_edge, eye_positions in ROWS
    for column, eye_y in enumerate(eye_positions)
)
