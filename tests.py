import unittest

class TestMissileGuidanceSystem(unittest.TestCase):
    def test_initialization(self):
        target = [1000, 500, 200]
        missile = MissileGuidanceSystem(target)

        self.assertEqual(missile.target_position, target)
        self.assertEqual(missile.current_position, [0, 0, 0])
        self.assertEqual(missile.velocity, [0, 0, 0])
        self.assertEqual(missile.acceleration, [0, 0, 0])
        self.assertEqual(missile.Kp, 0.1)
        self.assertEqual(missile.Ki, 0.01)
        self.assertEqual(missile.Kd, 0.05)
        self.assertEqual(missile.prev_error, [0, 0, 0])

    def test_update_position(self):
        target = [1000, 500, 200]
        missile = MissileGuidanceSystem(target)
        initial_position = missile.current_position.copy()

        missile.update_position()
        new_position = missile.current_position

        # Assert that position has changed from the initial position
        self.assertNotEqual(new_position, initial_position)

        # Add more assertions based on expected behavior

if __name__ == '__main__':
    unittest.main()
