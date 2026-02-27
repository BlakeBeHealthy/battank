from led import Led
from motor import tankMotor
from servo import Servo
from infrared import Infrared
from ultrasonic import Ultrasonic
from camera import Camera
import time

#written by Blake Trott, Dante Littlejohn, Trenton Lewis
def prelim_check(led, motor, servo, infrared, ultrasonic, camera):
    try:
        print("Testing motor...")
        # Test Motor
        motor.setMotorModel(2000, 2000)  # Move forward
        time.sleep(0.25)
        motor.setMotorModel(-2000, -2000)  # Move backward
        time.sleep(0.25)
        motor.setMotorModel(-2000, 2000)  # Turn left
        time.sleep(0.25)
        motor.setMotorModel(2000, -2000)  # Turn right
        time.sleep(0.25)
        motor.setMotorModel(0, 0)  # Stop the tank
        led.ledIndex(0x01, 0, 255, 0)
        print("Motor check complete")
        time.sleep(1)

        # Test Claw
        print("Testing servo/claw")
        for i in range(90, 150, 1):
            servo.setServoAngle("0", i)
            time.sleep(0.01)
        for i in range(140, 90, -1):
            servo.setServoAngle("1", i)
            time.sleep(0.01)
        for i in range(90, 140, 1):
            servo.setServoAngle("1", i)
            time.sleep(0.01)
        for i in range(140, 90, -1):
            servo.setServoAngle("0", i)
            time.sleep(0.01)
        led.ledIndex(0x02, 0, 255, 0)
        print("Servo/Claw check complete")
        time.sleep(1)

        # Test Line Tracking Position
        print("Testing Line Tracking Position")
        while True:
            if (
                infrared.read_one_infrared(1) == 0
                and infrared.read_one_infrared(2) == 1
                and infrared.read_one_infrared(3) == 0
            ) or (
                infrared.read_one_infrared(1) == 1
                and infrared.read_one_infrared(2) == 0
                and infrared.read_one_infrared(3) == 1
            ):
                led.ledIndex(
                    0x04, 0, 255, 0
                )  # Green means tape is aligned in the middle
                break
            else:
                led.ledIndex(0x04, 255, 0, 0)  # Red means tape is misaligned
        print("Line Tracking Position check complete")
        time.sleep(1)

        # Test ultrasonic sensor
        print("Testing ultrasonic sensor")
        while True:
            distance_from_object = ultrasonic.get_distance()
            if distance_from_object <= 25:
                led.ledIndex(0x04, 255, 0, 0)  # Object is too close
            else:
                break
        led.ledIndex(0x08, 0, 255, 0)
        print("Ultrasonic sensor check complete")

        print("Preliminary checks complete")

    except KeyboardInterrupt:
        print("BatTank shutting down")
        servo.setServoAngle("0", 90)
        servo.setServoAngle("1", 140)


def is_tape_centered(infrared):
    if (
        infrared.read_one_infrared(1) == 0
        and infrared.read_one_infrared(2) == 1
        and infrared.read_one_infrared(3) == 0
    ) or (
        infrared.read_one_infrared(1) == 1
        and infrared.read_one_infrared(2) == 0
        and infrared.read_one_infrared(3) == 1
    ):
        return True
    else:
        False


def is_path_clear(ultrasonic):
    distance_from_object = ultrasonic.get_distance()
    return True if distance_from_object > 25 else False


def line_track(infrared, ultrasonic, motor, servo, led):
    while is_tape_centered(infrared):
        if is_path_clear(ultrasonic) is False:
            motor.setMotorModel(0, 0)
            # TODO: Remove obstacle from path if movable with claw
        else:
            motor.setMotorModel(
                2000, 2000
            )  # Move forward as long as there isn't anything in the way


def run():
    print("BatTank starting...")
    led = Led()
    motor = tankMotor()
    servo = Servo()
    infrared = Infrared()
    ultrasonic = Ultrasonic()
    camera = Camera()

    # Preliminary check of all functions
    prelim_check(led, motor, servo, infrared, ultrasonic, camera)
    print("BatTank ready to roll")
    # First feature, line tracking
    line_track(infrared, ultrasonic, motor, servo, led)
