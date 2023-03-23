import RPi.GPIO as gpio
from time import sleep, clock

def trans(a, n):
    return [int (elem) for elem in bin(a)[2:].zfill(n)]

dac=[26, 19, 13, 6, 5, 11, 9, 10]
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

try:
    a = input("Введите период, число в секундах:")
    T = float(a)
    t = T / 256 / 2
    while (True):
        for i in range(255, 0, -1):
            a = i
            gpio.output(dac, trans(a, 8))
            sleep(t)
        for i in range(255):
            a = i
            gpio.output(dac, trans(a, 8))
            sleep(t)
except ValueError:
    print("Too low period")
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    gpio.output(dac, 0)
    gpio.cleanup()