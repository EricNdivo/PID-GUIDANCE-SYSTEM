from vpython import *
import math

scene = canvas(title='Missile Guidance System', width=800, height=600, center=vector(0, 5, 0), background=color.cyan)
ground = box(pos=vector(0, 0, 0), size=vector(20, 0.2, 20), color=color.green)
building = box(pos=vector(5, 1, 0), size=vector(2, 2, 2), color=color.red)
missile = cone(pos=vector(-5, 10, 0), axis=vector(0.5, -1, 0), radius=0.5, color=color.yellow)
missile.velocity = vector(0, -1, 0)
missile.acceleration = vector(0, 0, 0)
target_position = building.pos

Kp = 0.2
Ki = 0.01
Kd = 0.1
prev_error = vector(0, 0, 0)
integral_error = vector(0, 0, 0)


dt = 0.01
def pid_control(current_position, target_position, prev_error, integral_error, dt):
    error = target_position - current_position
    proportional = Kp * error
    integral_error += error * dt
    integral = Ki * integral_error
    derivative = Kd * (error - prev_error) / dt
    prev_error = error
    return proportional + integral + derivative, prev_error, integral_error

# Run the simulation
while True:
    rate(100) 

    distance_to_target = mag(missile.pos - target_position)

    if distance_to_target < 1.0:
        explosion = sphere(pos=missile.pos, radius=2, color=color.orange, emissive=True)
        explosion_life = 0.5  

        while explosion_life > 0:
            rate(50)
            explosion_life -= dt
            explosion.radius *= 1.05
            explosion.color = color.red if explosion.color == color.orange else color.orange

        explosion.visible = False
        print("Target hit!")
        break

    control_signal, prev_error, integral_error = pid_control(missile.pos, target_position, prev_error, integral_error, dt)
    missile.acceleration = control_signal
    missile.velocity += missile.acceleration * dt
    missile.pos += missile.velocity * dt

    if mag(missile.velocity) != 0:
        missile.axis = norm(missile.velocity) * 1.5
