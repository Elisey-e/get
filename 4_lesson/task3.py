import RPi.GPIO as gpio
from time import sleep, clock, time
from math import log2, ceil
import matplotlib.pyplot as matplt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2 ** bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4
m_values = [0]

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT, initial=gpio.LOW)
gpio.setup(troykaModule, gpio.OUT, initial=gpio.LOW)
gpio.setup(comparator, gpio.IN)
gpio.setup(leds, gpio.OUT)

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
    leds_c = min(round(value / 32), 8)
    list_t = list(map(int, list("0" * (8 - leds_c) + "1" * leds_c)))
    print(list_t)
    gpio.output(leds, list_t)
    return value

try:
    value = adc()
    begin_charg = exptime = time()

    while value < 220:
        value = adc()
        gpio.output(troykaModule, 0)
        #time.sleep(0.001)
        #exptime += 0.001
        m_values.append(value)
    
    m_values.pop()

    while value > 75:
        value = adc()
        gpio.output(troykaModule, 1)
        #time.sleep(0.001)
        #exptime += 0.001
        m_values.append(value)

    end_charg = exptime
    
    end_exp = time() - begin_charg
    
    matplt.plot(m_values)
    matplt.show()

    m_values_str = [str(item) for item in m_values]

    with open("data.txt", "w") as out:
        out.write("\n".join(m_values_str))

    freq = len(m_values) / end_exp

    settings = [3.3/256, freq, end_exp]

    settings_str = [str(item) for item in settings]

    with open("settings.txt", "w") as out:
        
        out.write("\n".join(settings_str))
except KeyboardInterrupt:
    print("Stopped by user")
else:
    print("NOEXCEPTIONS")
finally:
    gpio.output(dac, gpio.LOW)
    gpio.cleanup()
