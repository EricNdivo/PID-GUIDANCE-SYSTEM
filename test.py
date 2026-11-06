import unittest
import math
from projectile import ProjectileGuidanceSystem

class TestProjectileGuidanceSystem(unittest.TestCase):
    def test_initialization(self):
        target_position = [1000, 500, 200]
        projectile = ProjectileGuidanceSystem(target_position)
        self.assertEqual(projectile.target_position, target_position)
        self.assertEqual(projectile.current_position, [0, 0, 0])
        self.assertEqual(projectile.velocity, [0, 0, 0])
        self.assertEqual(projectile.acceleration, [0, 0, 0])
        self.assertEqual(projectile.integral_error, [0, 0, 0])
        self.assertEqual(projectile.prev_error, [0, 0, 0])
        self.assertEqual(projectile.time_step, 0.1)
        self.assertEqual(projectile.target_reached_threshold, 1.0)
        self.assertEqual(projectile.wind_velocity, [5, -3, 0])
        self.assertEqual(projectile.max_thrust, 10.0)
        self.assertEqual(projectile.fuel, 100.0)
        self.assertEqual(projectile.fuel_consumption_rate, 0.1)
        self.assertIsInstance(projectile.positions, list)

    def test_update_position(self):
        target_position = [1000, 500, 200]
        projectile = ProjectileGuidanceSystem(target_position)
        initial_position = projectile.current_position.copy()
        projectile.update_position()
        self.assertNotEqual(projectile.current_position, initial_position)
        
    def test_distance_to_target(self):
        target_position = [1000, 500, 200]
        projectile = ProjectileGuidanceSystem(target_position)
        distance = projectile.distance_to_target()
        expected_distance = math.sqrt(sum((target_position[i] - projectile.current_position[i]) ** 2 for i in range(3)))
        self.assertAlmostEqual(distance, expected_distance)


    def test_fuel_consumption(self):
        target_position = [1000, 500, 200]
        projectile = ProjectileGuidanceSystem(target_position)
        initial_fuel = projectile.fuel
        projectile.update_position()
        self.assertLess(projectile.fuel, initial_fuel)

    def test_engine_thrust(self):
        target_position = [1000, 500, 200]
        projectile = ProjectileGuidanceSystem(target_position)
        projectile.acceleration = [20, 20, 20]  # Exceed maximum thrust
        projectile.update_position()
        self.assertAlmostEqual(math.sqrt(sum(a ** 2 for a in projectile.acceleration)), projectile.max_thrust)

if __name__ == '__main__':
    unittest.main()
