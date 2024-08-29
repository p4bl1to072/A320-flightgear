import sys
from socket import *

import sys
import psutil
import serial
from serial.tools import list_ports
import time
import os
nombre_proceso = "fgfs.exe"

time.sleep(25)
HOST = "127.0.0.1"  # Local HOST
PORT_IN = 8000  # Puerto entrada
PORT_OUT = 8040 # Puerto salida

if os.path.isfile("numero_serie.txt"):
    # Abre el archivo en modo lectura
    with open('numero_serie.txt', 'r') as archivo:
        # Lee todas las líneas del archivo en una lista
        lineas = archivo.readlines()

    # Verifica si hay al menos tres líneas en el archivo
    if len(lineas) >= 3:
        # Extrae el número de la segunda y tercera línea y lo guarda como una cadena (string)
        serial_number_scr = lineas[1].strip()  # strip() elimina espacios en blanco y caracteres de nueva línea
        print(serial_number_scr)
        serial_number_bot = lineas[2].strip()
        print(serial_number_bot)
    else:
        print("Configurar los puertos de ambos arduinos")
else:
    print("Configurar los puertos del arduino usando la interfaz")


ports = serial.tools.list_ports.comports()
for port in ports:
    if port.serial_number == serial_number_bot:
        puerto_bot = port.device
        arduino_bot = serial.Serial(port=puerto_bot, baudrate=1000000, timeout=0.1)
    if port.serial_number == serial_number_scr:
        puerto_scr = port.device
        arduino_scr = serial.Serial(port=puerto_scr, baudrate=115200, timeout=0.1)
print("Encendiendo pantallas")
time.sleep(7) #no tocar
state_conmute = [0, 0, 0, 0, 0]
rot_counter = [0, 0, 0, 0]


def encode_datagram_OUT(n_datagram, o_datagram):
    # ofset_time en segundos
    # codifica y envia
    # En primera prueba solo vamos a sacar la cadena de caracteres para pantalla luego se añadiran leds
    # 0  Kts o Mach
    # 1  Managed Speed
    # 2  Kts
    # 3  Mach

    # 4  HDG o Track
    # * Manage LAT
    # 5  Managed HDG
    # 6  HDG

    # 7  Managed Alt
    # 8  Alt Value

    # 9  Managed FPA/VS
    # 10 FPA
    # 11 VS

    # 12 LOC   1
    # 13 AP1   2
    # 14 AP2   3
    # 15 A/THR 4
    # 16 EXPED 5
    # 17 APPR  6
    # format data = "0 0 000 0 0 0 000 0 00000 0 +0000"

    # Val_VS_FPA si es angulo va de -9.9 a +9.9 si no -6000 a +6000 de 500 en 500
    val_list = n_datagram.split(',')
    o_val_list = o_datagram.split(',')
    # encontrar los cambios
    if val_list[0:4] != o_val_list[0:4]:
        s1 = '1'
    else:
        s1 = '0'
    if val_list[4:7] != o_val_list[4:7]:
        s2 = '1'
    else:
        s2 = '0'
    if val_list[4] != o_val_list[4]:
        s3 = '1'
    else:
        s3 = '0'
    if val_list[7:9] != o_val_list[7:9]:
        s4 = '1'
    else:
        s4 = '0'
    if val_list[9:12] != o_val_list[9:12] or val_list[4] != o_val_list[4]:
        s5 = '1'
    else:
        s5 = '0'
    ss = s1 + s2 + s3 + s4 + s5

    # va_spd

    datagram_out = val_list[0] + val_list[1]
    if val_list[0] == '0':
        datagram_out = datagram_out + val_list[2]
    else:
        datagram_out = datagram_out + val_list[3][2:5]

    datagram_out = datagram_out + val_list[4] + '0' + val_list[5] + val_list[6] + val_list[7] + val_list[8] + val_list[
        9]

    if val_list[4] == '0':
        datagram_out = datagram_out + val_list[11]
    else:
        datagram_out = datagram_out + val_list[10]

    datagram_out = datagram_out + ss + '\n'
    return datagram_out

def encode_datagram_led(datagram):
    val_list = datagram.split(',')
    return val_list[12] + val_list[13] + val_list[14] + val_list[15] + val_list[16] + val_list[17] + '\n'

def encode_datagram_in(datagram):
    # ORDEN VARIABLES []
    # Encoder
    incremento = [0, 0, 0, 0]
    val_list = datagram.split(',')
    val_list = list(map(int, val_list))
    scale_rot = 1
    for i in range(4):
        if abs(val_list[i] - rot_counter[i]) > 200:
            incremento = -(val_list[i] - rot_counter[i] - 255)
        else:
            incremento[i] = -(val_list[i] - rot_counter[i])
        rot_counter[i] = val_list[i]
    # Botones no se hace nada son 9 botones index [4-11]
    # Conmutadores hay que separar entre los 5 casos index [12-16] PULL "1" 1000 "1"
    val_conmute = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # SPD
    if val_list[12] != state_conmute[0]:
        if val_list[12] == 1:
            val_conmute[1] = 1
        else:
            val_conmute[0] = 1

    # HDG
    if val_list[13] != state_conmute[1]:
        if val_list[13] == 1:
            val_conmute[3] = 1
        else:
            val_conmute[2] = 1

    # ALT
    if val_list[14] != state_conmute[2]:
        if val_list[14] == 1:
            val_conmute[5] = 1
        else:
            val_conmute[4] = 1

    # dial_mode
    val_conmute[6] = val_list[15]

    # V/S
    if val_list[16] != state_conmute[4]:
        if val_list[16] == 1:
            val_conmute[8] = 1
        else:
            val_conmute[7] = 1

    state_conmute[:] = val_list[12:17]
    datagram_pos = ",".join(list(map(str, val_list[4:12])) + list(map(str, val_conmute)) + list(
        map(str, incremento))) + ',1\n'  # +1 final es el update
    return datagram_pos

old_datagram_rawS_OUT = '*,*,***,*.***,*,*,***,*,*****,*,+**.*,+****,*,*,*,*,*,*'
tiempo_actual = time.time()
while True:
    try:

        Socket_OUT = socket(AF_INET, SOCK_DGRAM)
        Socket_OUT.setsockopt(SOL_SOCKET, SO_SNDBUF, 4096)
        Socket_OUT.bind((HOST, PORT_OUT))

        datagram_rawB_OUT, adrinput = Socket_OUT.recvfrom(2048)
        datagram_rawS_OUT = datagram_rawB_OUT.decode('ascii')[:-1]
        datagram_OUT = encode_datagram_OUT(datagram_rawS_OUT, old_datagram_rawS_OUT)
        #print(datagram_OUT)
        test1 = datagram_OUT.encode('UTF-8')
        test = arduino_scr.readline()
        arduino_scr.write(datagram_OUT.encode('UTF-8'))
        old_datagram_rawS_OUT = datagram_rawS_OUT[:]

        datagram_led = encode_datagram_led(datagram_rawS_OUT)

        # Read datagram from arduino
        datagram_rawB_IN = arduino_bot.readline()
        arduino_bot.write(datagram_led.encode('UTF-8'))
        datagram_rawS_IN = datagram_rawB_IN.decode('UTF-8')
        #print(datagram_rawS_IN)
        if "}" in datagram_rawS_IN and datagram_rawS_IN.index("{") == 0:
            # Delete unnecessary characters

            datagram_rawS_IN = datagram_rawS_IN[1:datagram_rawS_IN.index("}")]
            datagram_posS_IN = encode_datagram_in(datagram_rawS_IN)
            #print(datagram_posS_IN)

        # string_s = '1\n'
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect((HOST, PORT_IN))
        s.send(datagram_posS_IN.encode('ascii'))

        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        print(datagram_posS_IN.encode('ascii'))
        print(datagram_OUT)






    except:
        print("error")
        var = 0


