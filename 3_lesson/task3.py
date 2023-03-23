import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup([2, 24], gpio.OUT, initial=0)

try:
    p = gpio.PWM(24, 50)
    p2 = gpio.PWM(2, 50)
    a = 100
    p.start(a)
    p2.start(a)
    while True:
        a = int(input("Введите коэффициент заполнения:"))
        print("Плановое напряжение:", str(3.3 / 100 * a)[:5], "Вольт")
        p.ChangeDutyCycle(a)
        p2.ChangeDutyCycle(a)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    p.stop()
    gpio.cleanup()
