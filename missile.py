import math
import time

class MissileGuidanceSystem:
    def __init__(self, target_position):
        self.target_position = target_position
        self.current_position = [0, 0, 0]
        self.velocity = [0, 0, 0]
        self.acceleration = [0, 0, 0] 

        # Constants and gains
        self.Kp = 0.1
        self.Ki = 0.01
        self.Kd = 0.05
        self.prev_error = [0, 0, 0]
        self.integral_error = [0, 0, 0]

        # Simulation parameters
        self.time_step = 0.1  
        self.target_reached_threshold = 1.0  

    def update_position(self):
        error = [
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1],
            self.target_position[2] - self.current_position[2]
        ]

        #PID control
        proportional = [
            self.Kp * error[0],
            self.Kp * error[1],
            self.Kp * error[2]
        ]
        self.integral_error = [
            self.integral_error[0] + error[0] * self.time_step,
            self.integral_error[1] + error[1] * self.time_step,
            self.integral_error[2] + error[2] * self.time_step
        ]
        integral = [
            self.Ki * self.integral_error[0],
            self.Ki * self.integral_error[1],
            self.Ki * self.integral_error[2]
        ]
        derivative = [
            self.Kd * (error[0] - self.prev_error[0]) / self.time_step,
            self.Kd * (error[1] - self.prev_error[1]) / self.time_step,
            self.Kd * (error[2] - self.prev_error[2]) / self.time_step
        ]

        # Calculate total adjustment
        adjustment = [
            proportional[0] + integral[0] + derivative[0],
            proportional[1] + integral[1] + derivative[1],
            proportional[2] + integral[2] + derivative[2]
        ]

        self.prev_error = error

        self.acceleration = adjustment
        self.velocity = [
            self.velocity[0] + self.acceleration[0] * self.time_step,
            self.velocity[1] + self.acceleration[1] * self.time_step,
            self.velocity[2] + self.acceleration[2] * self.time_step
        ]
        self.current_position = [
            self.current_position[0] + self.velocity[0] * self.time_step,
            self.current_position[1] + self.velocity[1] * self.time_step,
            self.current_position[2] + self.velocity[2] * self.time_step
        ]

    def distance_to_target(self):
        return math.sqrt(
            (self.target_position[0] - self.current_position[0]) ** 2 +
            (self.target_position[1] - self.current_position[1]) ** 2 +
            (self.target_position[2] - self.current_position[2]) ** 2
        )

def main():
    target = [1000, 500, 200]  # Target position
    missile = MissileGuidanceSystem(target)

    while True:
        missile.update_position()
        print("Current Position:", missile.current_position)

        distance = missile.distance_to_target()
        print(f"Distance to Target: {distance:.2f} units")

        if distance < missile.target_reached_threshold:
            print("Target hit!")
            break

        time.sleep(missile.time_step)

if __name__ == "__main__":
    main()
