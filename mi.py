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

    def update_position(self):
        # Calculate error in position
        error = [
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1],
            self.target_position[2] - self.current_position[2]
        ]

        # Proportional, Integral, Derivative (PID) control
        proportional = [
            self.Kp * error[0],
            self.Kp * error[1],
            self.Kp * error[2]
        ]
        integral = [
            self.Ki * sum(error),
            self.Ki * sum(error),
            self.Ki * sum(error)
        ]
        derivative = [
            self.Kd * (error[0] - self.prev_error[0]),
            self.Kd * (error[1] - self.prev_error[1]),
            self.Kd * (error[2] - self.prev_error[2])
        ]

        # Calculate total adjustment
        adjustment = [
            proportional[0] + integral[0] + derivative[0],
            proportional[1] + integral[1] + derivative[1],
            proportional[2] + integral[2] + derivative[2]
        ]

        # Update previous error
        self.prev_error = error

        # Update acceleration, velocity, and position
        self.acceleration = adjustment
        self.velocity = [
            self.velocity[0] + self.acceleration[0],
            self.velocity[1] + self.acceleration[1],
            self.velocity[2] + self.acceleration[2]
        ]
        self.current_position = [
            self.current_position[0] + self.velocity[0],
            self.current_position[1] + self.velocity[1],
            self.current_position[2] + self.velocity[2]
        ]


target = [1000, 500, 200]  # Target position
missile = MissileGuidanceSystem(target)


for _ in range(10):
    missile.update_position()
    print("Current Position:", missile.current_position)
