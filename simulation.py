import math
import os
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PROJECTILE_COLOR = (0, 255, 0)
IMPACT_COLOR = (255, 165, 0)
IMPACT_RADIUS = 50
IMPACT_DURATION_MS = 500

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projectile.png")

class ProjectileGuidanceSystem:
    def __init__(self, target_position):
        self.target_position = target_position
        self.current_position = [100, 500]  
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
        self.max_thrust = 5.0  
        self.fuel = 100.0 
        self.fuel_consumption_rate = 0.1 
        self.phase = "launch"
        self._first_step = True

    def update_position(self):
        if self.fuel <= 0 and self.phase != "descent":
            print("Out of fuel! Projectile cannot continue.")
            return

        if self.phase == "launch":
            self.acceleration = [0, -self.max_thrust]
            self.velocity = [0, self.velocity[1] + self.acceleration[1] * self.time_step]
            self.current_position = [self.current_position[0], self.current_position[1] + self.velocity[1] * self.time_step]
            if self.velocity[1] <= 0:
                self.phase = "ascent"

        elif self.phase == "ascent":
            error = [
                self.target_position[0] - self.current_position[0],
                self.target_position[1] - self.current_position[1]
            ]

            if self._first_step:  # avoid derivative kick on the first step
                self.prev_error = error
                self._first_step = False

            proportional = [self.Kp * e for e in error]
            new_integral = [self.integral_error[i] + error[i] * self.time_step for i in range(2)]
            derivative = [
                self.Kd * (error[i] - self.prev_error[i]) / self.time_step for i in range(2)
            ]
            adjustment = [proportional[i] + self.Ki * new_integral[i] + derivative[i] for i in range(2)]

            magnitude = math.sqrt(sum(a ** 2 for a in adjustment))
            if magnitude > self.max_thrust:
                # Saturated: scale thrust and skip integration (anti-windup)
                adjustment = [a / magnitude * self.max_thrust for a in adjustment]
            else:
                self.integral_error = new_integral

            self.prev_error = error

            self.acceleration = adjustment
            self.velocity = [
                self.velocity[i] + self.acceleration[i] * self.time_step for i in range(2)
            ]
            self.current_position = [
                self.current_position[i] + self.velocity[i] * self.time_step for i in range(2)
            ]

            # Fuel burn scales with the thrust actually used
            thrust_fraction = math.sqrt(sum(a ** 2 for a in self.acceleration)) / self.max_thrust
            self.fuel -= self.fuel_consumption_rate * thrust_fraction * self.time_step
            if self.fuel < 0:
                self.fuel = 0
                self.phase = "descent"

        elif self.phase == "descent":
            # Descent phase: gravity pulling down the projectile
            gravity = 9.8
            self.acceleration = [0, gravity]
            self.velocity = [
                self.velocity[i] + self.acceleration[i] * self.time_step for i in range(2)
            ]
            self.current_position = [
                self.current_position[i] + self.velocity[i] * self.time_step for i in range(2)
            ]

        distance = self.distance_to_target()
        if distance < self.target_reached_threshold:
            self.phase = "hit"

    def distance_to_target(self):
        return math.sqrt(
            sum((self.target_position[i] - self.current_position[i]) ** 2 for i in range(2))
        )

def draw_impact(screen, position):
    pygame.draw.circle(screen, IMPACT_COLOR, position, IMPACT_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Projectile Guidance System")
    projectile_image = pygame.image.load(IMAGE_PATH)
    projectile_image = pygame.transform.scale(projectile_image, (50, 20))
    target_position = [700, 100]  
    projectile = ProjectileGuidanceSystem(target_position)

    clock = pygame.time.Clock()

    running = True
    impact_start = None  # time the impact began; the window stays responsive meanwhile
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.circle(screen, RED, target_position, 10)

        if impact_start is not None:
            draw_impact(screen, projectile.current_position)
            pygame.display.flip()
            if pygame.time.get_ticks() - impact_start >= IMPACT_DURATION_MS:
                running = False
            clock.tick(60)
            continue

        projectile.update_position()

        if projectile.phase == "hit":
            impact_start = pygame.time.get_ticks()
            print("Target hit!")
            continue
        else:
            rotated_image = pygame.transform.rotate(projectile_image, -math.degrees(math.atan2(projectile.velocity[1], projectile.velocity[0])))
            rect = rotated_image.get_rect(center=(projectile.current_position[0], projectile.current_position[1]))
            screen.blit(rotated_image, rect.topleft)
        distance = projectile.distance_to_target()
        print(f"Current Position: {projectile.current_position}, Distance to Target: {distance:.2f} units, Fuel: {projectile.fuel:.2f} units, Phase: {projectile.phase}")

        if projectile.fuel <= 0 and projectile.phase != "descent":
            print("Projectile ran out of fuel!")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
