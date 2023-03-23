import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)

gpio.setup([21, 20, 16, 12, 7, 8, 25], gpio.OUT, initial=1)

p = gpio.PWM(24, 50)
p.start(50)
input("press ret ro stop")

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