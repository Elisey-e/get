import RPi.GPIO as gpio
from time import sleep, clock

dac=[26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2 ** bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT, initial=gpio.LOW)
gpio.setup(troykaModule, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comparator, gpio.IN)

def decimal2binary(decimal):
    return [int (elem) for elem in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    gpio.output(dac, signal)
    return signal

def adc():
    value = 128
    delta = 64
    for i in range(bits - 1):
        signal = num2dac(value)
        sleep(0.01)
        voltage = value / levels * maxVoltage
        comparatorvalue = gpio.input(comparator)
        if comparatorvalue == 0:
            value -= delta
        else:
            value += delta
        delta //= 2
    print("ADC value = {:^3} -> {}, input voltage = {:2f}".format(value, signal, voltage))

try:
    while (True):
        adc()
except KeyboardInterrupt:
    print("Stopped by user")
else:
    print("NOEXCEPTIONS")
finally:
    gpio.output(dac, gpio.LOW)
    gpio.cleanup()
