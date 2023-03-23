import RPi.GPIO as gpio

def trans(a, n):
    return [int (elem) for elem in bin(a)[2:].zfill(n)]

dac=[26, 19, 13, 6, 5, 11, 9, 10]
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

try:
    while (True):
        a = input('num:')
        if a == 'q':
            raise KeyboardInterrupt
        elif a.count('.') > 0:
            print("not N")
        elif not a.isdigit():
            print("string")
        elif int(a) < 0:
            print("below zero")
        elif int(a) > 255:
            print("too big")
        else:
            b = int(a)
            gpio.output(dac, trans(int(a), 8))
            print("voltage:{:.4f}".format(int(a) / 256 * 3.3))
except ValueError:
    print("input num not in range")
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    gpio.output(dac, 0)
    gpio.cleanup()