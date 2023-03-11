import time


class LocomotiveController:
    train_sim_controller = None

    previous_error = 0

    def __init__(self, controller):
        self.train_sim_controller = controller

    def calculate_throttle(self, desired_speed, current_speed):

        gain = 0.2

        error = desired_speed - current_speed

        proportional = gain * error

        integral = gain * error * 0.1



        derivative = gain * (error - self.previous_error) / 0.1

        self.previous_error = error



        return proportional + integral + derivative
