import math
import time
import matplotlib.pyplot as plt

class ProjectileGuidanceSystem:
    def __init__(self, target_position):
        self.target_position = target_position
        self.current_position = [0, 0, 0]
        self.velocity = [0, 0, 0]
        self.acceleration = [0, 0, 0]
        self.integral_error = [0, 0, 0]

        self.Kp = 0.1
        self.Ki = 0.01
        self.Kd = 0.05
        self.prev_error = [0, 0, 0]
        self.time_step = 0.1  
        self.target_reached_threshold = 1.0  

        self.wind_velocity = [5, -3, 0]
        self.gravity = 3.0  # downward acceleration along z (up axis)
        self.wind_drag = 0.1  # how strongly the air drags the projectile toward the wind speed
        self._first_step = True

        self.max_thrust = 10.0 
        self.fuel = 100.0  
        self.fuel_consumption_rate = 0.1 

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([0, 1200])
        self.ax.set_ylim([0, 1200])
        self.ax.set_zlim([0, 300])
        self.positions = []

    def update_position(self):
        if self.fuel <= 0:
            print("Out of fuel! Projectile cannot continue.")
            return


        error = [
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1],
            self.target_position[2] - self.current_position[2]
        ]

        # Derivative kick fix: no derivative term on the very first step
        if self._first_step:
            self.prev_error = error
            self._first_step = False

        proportional = [self.Kp * e for e in error]
        new_integral = [self.integral_error[i] + error[i] * self.time_step for i in range(3)]
        derivative = [
            self.Kd * (error[i] - self.prev_error[i]) / self.time_step for i in range(3)
        ]
        adjustment = [
            proportional[i] + self.Ki * new_integral[i] + derivative[i] for i in range(3)
        ]

        magnitude = math.sqrt(sum(a ** 2 for a in adjustment))
        if magnitude > self.max_thrust:
            # Saturated: scale thrust and do not accumulate the integral (anti-windup)
            adjustment = [a / magnitude * self.max_thrust for a in adjustment]
        else:
            self.integral_error = new_integral

        self.prev_error = error

        self.acceleration = adjustment
        # Wind acts as drag toward the wind speed instead of a constant acceleration
        self.velocity = [
            self.velocity[i]
            + (self.acceleration[i]
               + self.wind_drag * (self.wind_velocity[i] - self.velocity[i])
               + (-self.gravity if i == 2 else 0.0)) * self.time_step
            for i in range(3)
        ]
        self.current_position = [
            self.current_position[i] + self.velocity[i] * self.time_step for i in range(3)
        ]

        # Fuel burn scales with the thrust actually used
        thrust_fraction = math.sqrt(sum(a ** 2 for a in self.acceleration)) / self.max_thrust
        self.fuel -= self.fuel_consumption_rate * thrust_fraction * self.time_step
        if self.fuel < 0:
            self.fuel = 0
        self.positions.append(self.current_position.copy())

    def distance_to_target(self):
        return math.sqrt(
            sum((self.target_position[i] - self.current_position[i]) ** 2 for i in range(3))
        )

    def visualize(self):
        if not self.positions:
            return
        self.ax.clear()
        self.ax.set_xlim([0, 1200])
        self.ax.set_ylim([0, 1200])
        self.ax.set_zlim([0, 300])
        xs, ys, zs = zip(*self.positions)
        self.ax.plot(xs, ys, zs)
        self.ax.scatter(*self.target_position, color='red')
        plt.draw()
        plt.pause(0.01)

def main():
    target = [1000, 500, 200]  
    projectile = ProjectileGuidanceSystem(target)

    while True:
        projectile.update_position()
        projectile.visualize()

        distance = projectile.distance_to_target()
        print(f"Current Position: {projectile.current_position}, Distance to Target: {distance:.2f} units, Fuel: {projectile.fuel:.2f} units")

        if distance < projectile.target_reached_threshold:
            print("Target hit!")
            break

        if projectile.fuel <= 0:
            print("Projectile ran out of fuel!")
            break

        time.sleep(projectile.time_step)

    plt.show()

if __name__ == "__main__":
    main()
