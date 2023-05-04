import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as matplt

GPIO.setmode(GPIO.BCM)

dac = (10,  9, 11,  5,  6, 13, 19, 26)
comp = 4
troyka = 17
value = 0
m_values = [0]

begin_charg = 0
end_charg   = 0
end_exp     = 0

GPIO.setup(comp, GPIO.IN) 
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

def get_number():
    while 1:
        number = input(("enter number: "))
        if number.isdecimal() == 0:
            print("Not decimal number")
            continue
        if number == 'q':
            break
        if int(number) < 0:
            print("Less then zero")
            continue
        elif int(number) > 255:
            print("More then 255")
            continue
        try: 
            x = int(number)
            return x
        except ValueError:
            print("you entered not a number")


def decimal_to_bin(x):
    string = format(x, 'b')
    tmp_list1 = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(string)):
        tmp_list1[i] = int(string[len(string) - (i + 1)])
    return tmp_list1 


def adc():
    sum = 0
    value = 0
    for k in range(7, -1, -1):
        value = 2 ** k
        sum += value
        list1 = decimal_to_bin(sum)
        GPIO.output(dac, list1)
        time.sleep(0.001)
        compVal = GPIO.input(comp)
        if compVal == 0:
            sum -= value
    print("ADC value = {:^3}, voltage = {:.2f}".format(sum, (sum / 255) * 3.3))
    return sum

try:
    value = adc()
    begin_charg = exptime = time.time()

    while value < 255:
        value = adc()
        GPIO.output(troyka, 1)
        #time.sleep(0.001)
        #exptime += 0.001
        m_values.append(value)

    end_charg = exptime
    
    while value > 10:
        value = adc()
        GPIO.output(troyka, 0)
        #time.sleep(0.001)
        #exptime += 0.001
        m_values.append(value)

    end_exp = time.time() - begin_charg
    
    m_values.append(end_exp)

    m_values_str = [str(item) for item in m_values]

    with open("data.txt", "w") as out:
        
        out.write("\n".join(m_values_str))
    matplt.plot(m_values)
    matplt.show()

    freq = len(m_values) / end_exp

    settings = [3.3/256, freq, end_exp]

    settings_str = [str(item) for item in settings]

    with open("settings.txt", "w") as out:
        
        out.write("\n".join(settings_str))


finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 1)
    GPIO.cleanup()