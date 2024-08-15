# Functions for:
# - Digital output
# - Digital input
# - Delay
# - Button
# - HC-SR04 Ultrasonic distance sensor
# - DHT11 Temperature and Humidity sensor
# - OLED display


import os
import time
import pwmio
import board
import digitalio
import subprocess
# from adafruit_motor import servo
import adafruit_dht
import adafruit_motor.motor as motor
import adafruit_hcsr04

cwd = os.getcwd()


# ------------- Digital output ------------- #
def digitalWrite(pin_no: str, val: float):
    if not hasattr(board, pin_no):
        return  # + send a message
    pin = digitalio.DigitalInOut(getattr(board, pin_no))
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = int(val)


# ------------- Digital input ------------- #
def digitalRead(pin_no: str):
    if not hasattr(board, pin_no):
        return
    pin = digitalio.DigitalInOut(getattr(board, pin_no))
    pin.direction = digitalio.Direction.INPUT
    return bool(pin.value)


# ------------- Delay ------------- #
def delay(ms: int):
    time.sleep(ms / 1000)


# ------------- Button ------------- #
def button(pin: str):
    button = 0
    try:
        button = digitalio.DigitalInOut(getattr(board, pin))
        button.direction = digitalio.Direction.INPUT
    except Exception:
        None
    button.pull = digitalio.Pull.UP
    return not button.value


# ------------- HC-SR04 Ultrasonic distance sensor  ------------- #
class _dist:
    def def_dist(self, trigger: str, echo: str):
        try:
            self.sonar = adafruit_hcsr04.HCSR04(
                trigger_pin=getattr(board, trigger),
                echo_pin=getattr(board, echo))
        except Exception:
            return

    def dst(self):
        try:
            s = 0.0
            for i in range(20):
                if self.sonar.distance < 1:
                    i = i - 1
                    continue
                s += self.sonar.distance
            return round(s / 20, 1)
        except Exception:
            return 0.0


dist = _dist()


# ------------- DHT Temperature and Humidity sensor ------------- #
class _dht:
    def def_dht(self, pin: str):
        try:
            self.dhtDevice = adafruit_dht.DHT11(getattr(board, pin))
        except Exception:
            return

    def temp(self):
        try:
            return self.dhtDevice.temperature
        except Exception:
            return 0.0

    def hum(self):
        try:
            return self.dhtDevice.humidity
        except Exception:
            return 0.0


dht = _dht()


# ------------- OLED display ------------- #
class _oled:
    def define(self, _height, _width, _text_color):
        self.width = int(_width)
        self.height = int(_height)
        self.text_color = int(_text_color)

    def print(self, text):
        subprocess.Popen(
            "python3 "
            + cwd
            + "/plugins/rpi/sensors/oled_display.py "
            + str(self.height)
            + " "
            + str(self.width)
            + " "
            + str(self.text_color)
            + " '"
            + str(text)
            + "'",
            shell=True,
        )


oled = _oled()


# ------------- PIR sensor ------------- #
def pir_motion(pin: str) -> bool:
    try:
        pir = digitalio.DigitalInOut(getattr(board, pin))
        pir.direction = digitalio.Direction.INPUT
        return bool(pir.value)
    except Exception:
        return False


# ------------- SERVO motor ------------- #
# *need to make usability easy and more controlable
# def servo_motor(pin: str, times, pulse_ms: int, frequency=50):
#     pwm = pwmio.PWMOut(getattr(board, pin), duty_cycle=2**15, frequency=50)
#     servo_m = servo.Servo(pwm)
#     duty_cycle = int(pulse_ms / (period_ms / 65535.0))

#     for i in range(0, times):
#         for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 Degree steps
#             servo.angle = angle
#             time.sleep(0.05)
#         for angle in range(180, 0, -5):  # 180 - 0 degrees, 5 Degree steps
#             servo.angle = angle
#             time.sleep(0.05)


# ------------- PWM led ------------- #
def pwm_led(pin: str, duty_cycle: int):
    led = pwmio.PWMOut(getattr(board, pin), frequency=5000, duty_cycle=0)
    led.duty_cycle = int(duty_cycle / 100 * 65535)
    if duty_cycle == 0:
        led.deinit()

# # Example usage
# pwm_led('D14', 50)  # Set to 50% brightness or duty cycle
# sleep(1)     # Keep the LED on for 1 second


# ------------- DC Motor (not tested yet) ------------- #
def run_dc_motor(pin1, pin2, duration: float):
    pwm_a = pwmio.PWMOut(getattr(board, pin1), frequency=5000)
    pwm_b = pwmio.PWMOut(getattr(board, pin2), frequency=5000)

    m = motor.DCMotor(pwm_a, pwm_b)
    m.decay_mode = 0
    m.throttle = 1.0

    time.sleep(duration)
    m.throttle = 0

# Example usage of the function
# run_dc_motor('D14', 'D15', 2)  # Run the motor for 2 seconds
