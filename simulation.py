import pygame
import math
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
MISSILE_COLOR = (0, 255, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Missile Guidance System")
missile_image = pygame.image.load("missile.png")
missile_image = pygame.transform.scale(missile_image, (50, 20))

class MissileGuidanceSystem:
    def __init__(self, target_position):
        self.target_position = target_position
        self.current_position = [100, 100]  # Starting position
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.integral_error = [0, 0]

        self.Kp = 0.1
        self.Ki = 0.01
        self.Kd = 0.05
        self.prev_error = [0, 0]

        self.time_step = 0.1 
        self.target_reached_threshold = 10.0 

        # Fuel and thrust parameters
        self.max_thrust = 5.0  # Maximum thrust of the missile in units per second^2 
        self.fuel = 100.0  # Initial amount of fuel in units
        self.fuel_consumption_rate = 0.1  # Fuel consumption rate per time step (units per second)

    def update_position(self):
        if self.fuel <= 0:
            print("Out of fuel! Missile cannot continue.")
            return

        error = [
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1]
        ]
        proportional = [self.Kp * e for e in error]
        self.integral_error = [self.integral_error[i] + error[i] * self.time_step for i in range(2)]
        integral = [self.Ki * ie for ie in self.integral_error]
        derivative = [
            self.Kd * (error[i] - self.prev_error[i]) / self.time_step for i in range(2)
        ]

        adjustment = [proportional[i] + integral[i] + derivative[i] for i in range(2)]

        # Limit the acceleration to the available thrust
        total_adjustment_magnitude = math.sqrt(sum(a ** 2 for a in adjustment))
        if total_adjustment_magnitude > self.max_thrust:
            adjustment = [a / total_adjustment_magnitude * self.max_thrust for a in adjustment]

        self.prev_error = error

        self.acceleration = adjustment
        self.velocity = [
            self.velocity[i] + self.acceleration[i] * self.time_step for i in range(2)
        ]
        self.current_position = [
            self.current_position[i] + self.velocity[i] * self.time_step for i in range(2)
        ]

        # fuel consumption
        self.fuel -= self.fuel_consumption_rate * self.time_step
        if self.fuel < 0:
            self.fuel = 0

    def distance_to_target(self):
        return math.sqrt(
            sum((self.target_position[i] - self.current_position[i]) ** 2 for i in range(2))
        )

def main():
    target_position = [700, 500]  
    missile = MissileGuidanceSystem(target_position)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        missile.update_position()

        pygame.draw.circle(screen, RED, target_position, 10)


        rotated_image = pygame.transform.rotate(missile_image, -math.degrees(math.atan2(missile.velocity[1], missile.velocity[0])))
        rect = rotated_image.get_rect(center=(missile.current_position[0], missile.current_position[1]))
        screen.blit(rotated_image, rect.topleft)

  
        distance = missile.distance_to_target()
        print(f"Current Position: {missile.current_position}, Distance to Target: {distance:.2f} units, Fuel: {missile.fuel:.2f} units")

        if distance < missile.target_reached_threshold:
            print("Target hit!")
            running = False

        if missile.fuel <= 0:
            print("Missile ran out of fuel!")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
