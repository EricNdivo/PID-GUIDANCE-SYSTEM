import unittest
import math
from missile import MissileGuidanceSystem

class TestMissileGuidanceSystem(unittest.TestCase):
    def test_initialization(self):
        target_position = [1000, 500, 200]
        missile = MissileGuidanceSystem(target_position)
        self.assertEqual(missile.target_position, target_position)
        self.assertEqual(missile.current_position, [0, 0, 0])
        self.assertEqual(missile.velocity, [0, 0, 0])
        self.assertEqual(missile.acceleration, [0, 0, 0])
        self.assertEqual(missile.integral_error, [0, 0, 0])
        self.assertEqual(missile.prev_error, [0, 0, 0])
        self.assertEqual(missile.time_step, 0.1)
        self.assertEqual(missile.target_reached_threshold, 1.0)
        self.assertEqual(missile.wind_velocity, [5, -3, 0])
        self.assertEqual(missile.max_thrust, 10.0)
        self.assertEqual(missile.fuel, 100.0)
        self.assertEqual(missile.fuel_consumption_rate, 0.1)
        self.assertIsInstance(missile.positions, list)

    def test_update_position(self):
        target_position = [1000, 500, 200]
        missile = MissileGuidanceSystem(target_position)
        initial_position = missile.current_position.copy()
        missile.update_position()
        self.assertNotEqual(missile.current_position, initial_position)
        
    def test_distance_to_target(self):
        target_position = [1000, 500, 200]
        missile = MissileGuidanceSystem(target_position)
        distance = missile.distance_to_target()
        expected_distance = math.sqrt(sum((target_position[i] - missile.current_position[i]) ** 2 for i in range(3)))
        self.assertAlmostEqual(distance, expected_distance)


    def test_fuel_consumption(self):
        target_position = [1000, 500, 200]
        missile = MissileGuidanceSystem(target_position)
        initial_fuel = missile.fuel
        missile.update_position()
        self.assertLess(missile.fuel, initial_fuel)

    def test_engine_thrust(self):
        target_position = [1000, 500, 200]
        missile = MissileGuidanceSystem(target_position)
        missile.acceleration = [20, 20, 20]  # Exceed maximum thrust
        missile.update_position()
        self.assertAlmostEqual(math.sqrt(sum(a ** 2 for a in missile.acceleration)), missile.max_thrust)

if __name__ == '__main__':
    unittest.main()
