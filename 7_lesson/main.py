from matplotlib import pyplot as plt
import numpy as np


def unitline():
    data_arr = np.loadtxt('data.txt', dtype=int)
    lst = data_arr * volt_step
    return lst


def timeline():
    lst = np.linspace(0, tmp[2], volt_arr.size)
    return lst


with open('settings.txt', 'r') as settings:
    tmp = [float(num) for num in settings.read().split("\n")]

time_step = 1 / tmp[1]
volt_step = tmp[0]

volt_arr = unitline()
time_arr = timeline()

plt.figure(figsize=(16, 10), dpi=500)

plt.title('Исследование зарядки и разрядки конденсатора в RC-цепи', loc='center', fontsize=27)

plt.ylabel('U, В', fontsize=14)
plt.ylim(0, int(volt_arr.max() + 1))
plt.yticks(fontsize=12, rotation=30, ha='right', va='top')

plt.xlabel('t, сек', fontsize=14)
plt.xlim(0, int(time_arr.max() + 1))
plt.xticks(fontsize=12, rotation=30, ha='center', va='top')

plt.grid(color='black',
         linewidth=0.45,
         linestyle='dotted')

plt.minorticks_on()

plt.grid(which='minor',
         color='grey',
         linewidth=0.25,
         linestyle='dashed')

charge_time = volt_arr.argmax() * time_step

discharge_time = tmp[2] - charge_time

plt.text(tmp[2] * 0.74, volt_arr.max() * 0.86 + 0.2,  'Время зарядки  =  %.2f сек' % charge_time, fontsize=14)
plt.text(tmp[2] * 0.74, volt_arr.max() * 0.86,        'Время разрядки = %.2f сек' % discharge_time, fontsize=14)

# plt.scatter(time_arr, volt_arr, s=0.01, color='blue')

plt.plot(time_arr, volt_arr, 'r', linewidth=1, marker="o", markersize=8, markevery=50, label='Аппроксимирующая кривая',
         linestyle='-')

plt.legend(loc='best', fontsize=14)

plt.savefig('Graph.png')
plt.savefig('Graph.svg')
