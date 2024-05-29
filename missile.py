import math
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MissileGuidanceSystem:
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
            print("Out of fuel! Missile cannot continue.")
            return


        error = [
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1],
            self.target_position[2] - self.current_position[2]
        ]

        proportional = [self.Kp * e for e in error]
        self.integral_error = [self.integral_error[i] + error[i] * self.time_step for i in range(3)]
        integral = [self.Ki * ie for ie in self.integral_error]
        derivative = [
            self.Kd * (error[i] - self.prev_error[i]) / self.time_step for i in range(3)
        ]

        adjustment = [proportional[i] + integral[i] + derivative[i] for i in range(3)]

        total_adjustment_magnitude = math.sqrt(sum(a ** 2 for a in adjustment))
        if total_adjustment_magnitude > self.max_thrust:
            adjustment = [a / total_adjustment_magnitude * self.max_thrust for a in adjustment]

        self.prev_error = error

        self.acceleration = adjustment
        self.velocity = [
            self.velocity[i] + self.acceleration[i] * self.time_step for i in range(3)
        ]
        self.velocity = [
            self.velocity[i] + self.wind_velocity[i] * self.time_step for i in range(3)
        ]
        self.current_position = [
            self.current_position[i] + self.velocity[i] * self.time_step for i in range(3)
        ]

        self.fuel -= self.fuel_consumption_rate * self.time_step
        if self.fuel < 0:
            self.fuel = 0
        self.positions.append(self.current_position.copy())

    def distance_to_target(self):
        return math.sqrt(
            sum((self.target_position[i] - self.current_position[i]) ** 2 for i in range(3))
        )

    def visualize(self):
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
    missile = MissileGuidanceSystem(target)

    while True:
        missile.update_position()
        missile.visualize()

        distance = missile.distance_to_target()
        print(f"Current Position: {missile.current_position}, Distance to Target: {distance:.2f} units, Fuel: {missile.fuel:.2f} units")

        if distance < missile.target_reached_threshold:
            print("Target hit!")
            break

        if missile.fuel <= 0:
            print("Missile ran out of fuel!")
            break

        time.sleep(missile.time_step)

    plt.show()

if __name__ == "__main__":
    main()
