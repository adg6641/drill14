import unittest
from unittest.mock import Mock, patch

import bird_flock
from bird import Bird, DRAW_SCALE, FLAPS_PER_SECOND
from bird_animation import FRAMES
from bird_flock import BirdFlock, ROUND_TRIP_SECONDS, patrol_x


class SpriteTests(unittest.TestCase):
    def test_poses_are_read_in_row_order_without_the_empty_cell(self):
        self.assertEqual(len(FRAMES), 14)
        self.assertEqual([frame.bottom for frame in FRAMES], [341] * 5 + [153] * 5 + [0] * 4)
        self.assertEqual(FRAMES[-1].left, 546)
        self.assertEqual(FRAMES[4].left + FRAMES[4].width, 918)

    def test_wing_cycle_reaches_every_pose_and_wraps_to_first(self):
        bird = Bird(Mock())
        cycle_seconds = 1 / FLAPS_PER_SECOND
        for pose in range(len(FRAMES)):
            bird.update(cycle_seconds * (pose + 0.5) / len(FRAMES))
            self.assertEqual(bird.frame_index, pose)
        bird.update(cycle_seconds)
        self.assertEqual(bird.frame_index, 0)

    def test_flipped_sprite_keeps_the_same_body_anchor(self):
        image = Mock()
        bird = Bird(image)
        frame = FRAMES[0]
        for direction in (1, -1):
            bird.draw(200, 300, direction)
            _, _, _, _, _, flip, center_x, center_y, _, _ = image.clip_composite_draw.call_args.args
            self.assertEqual(flip, 'h' if direction < 0 else '')
            self.assertAlmostEqual(center_x + direction * frame.anchor_dx * DRAW_SCALE, 200)
            self.assertAlmostEqual(center_y + frame.anchor_dy * DRAW_SCALE, 300)


class FlockTests(unittest.TestCase):
    def test_patrol_turns_at_both_ends_and_repeats(self):
        left, right = 235, 1365
        half_trip = ROUND_TRIP_SECONDS / 2
        self.assertEqual(patrol_x(0, left, right), (left, 1))
        self.assertEqual(patrol_x(half_trip, left, right), (right, -1))
        self.assertEqual(patrol_x(ROUND_TRIP_SECONDS, left, right), (left, 1))
        self.assertAlmostEqual(patrol_x(half_trip - 0.01, left, right)[0],
                               patrol_x(half_trip + 0.01, left, right)[0])

    def test_all_ten_birds_stay_in_view_on_both_legs(self):
        image = Mock()
        with (patch.object(bird_flock, 'load_image', return_value=image) as load_image,
              patch.object(bird_flock, 'get_canvas_width', return_value=1600),
              patch.object(bird_flock, 'get_canvas_height', return_value=600)):
            flock = BirdFlock()
        load_image.assert_called_once()
        self.assertEqual(len(flock.birds), 10)
        self.assertEqual(len({bird.frame_index for bird in flock.birds}), 10)

        with patch.object(bird_flock.game_framework, 'frame_time', 0.125):
            for step in range(193):
                image.reset_mock()
                flock.draw()
                calls = image.clip_composite_draw.call_args_list
                self.assertEqual(len(calls), 10)
                expected_flip = 'h' if step % 96 >= 48 else ''
                for call in calls:
                    _, _, _, _, _, flip, x, y, width, height = call.args
                    self.assertEqual(flip, expected_flip)
                    self.assertGreaterEqual(x - width / 2, 0)
                    self.assertLessEqual(x + width / 2, 1600)
                    self.assertGreaterEqual(y - height / 2, 0)
                    self.assertLessEqual(y + height / 2, 600)
                flock.update()


if __name__ == '__main__':
    unittest.main()
