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
    # Se verifica si hay 3 porque siempre deja una línea en blanco al final
    # Se ha modificado para que sean 7 líneas
    if len(lineas) >= 2:
        # Extrae el número de la segunda y tercera línea y lo guarda como una cadena (string)
        # Añadidos las 3 nuevas placas de arduino
        serial_number_buttons_EFIS_left = lineas[1].strip()
        print(serial_number_buttons_EFIS_left)
    else:
        print("Configurar el puerto del arduino del EFIS")
else:
    print("Configurar los puertos del arduino usando la interfaz")

# List of used serial ports (in no particular order)
ports = serial.tools.list_ports.comports()
# Corresponding serial ports assigned to each arduino
for port in ports:
    if port.serial_number == serial_number_buttons_EFIS_left:
        puerto_button_EFIS_left = port.device
        arduino_EFIS_left = serial.Serial(port=puerto_button_EFIS_left, baudrate=1000000, timeout=0.1)

print("Encendiendo pantallas")
time.sleep(7)
state_conmute = [0, 0]
rot_counter = [0]

""" COMENTADO EN LA PRUEBA DE ENVIO LEDS
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
    # format data = "0 0 000 0 0 0 000 0 00000 0 +0000" + LEDS

    # Val_VS_FPA si es angulo va de -9.9 a +9.9 si no -6000 a +6000 de 500 en 500
    val_list = n_datagram.split(',')
    o_val_list = o_datagram.split(',')
    # encontrar los cambios en las pantallas
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
    #concatenación de cadenas usando los valores correctos
    datagram_out = val_list[0] + val_list[1]
    if val_list[0] == '0':
        datagram_out = datagram_out + val_list[2] #kts
    else:
        datagram_out = datagram_out + val_list[3][2:5] #decimales de Mach

    datagram_out = datagram_out + val_list[4] + '0' + val_list[5] + val_list[6] + val_list[7] + val_list[8] + val_list[
        9]

    if val_list[4] == '0':
        datagram_out = datagram_out + val_list[11] #VS
    else:
        datagram_out = datagram_out + val_list[10] #FPA
        
    #añade una variable que indica si se han producido cambios en las pantallas
    datagram_out = datagram_out + ss + '\n'
    return datagram_out
"""

def encode_datagram_led(datagram):
    #USAR VALORES DERECHA SI SACO SOLO LEDS
    val_list = datagram.split(',')
    # 12 CSTR   1
    # 13 WPT   2
    # 14 VOR.D   3
    # 15 NDB 4
    # 16 ARPT 5
    # 17 FD  6
    # 18 LS 7
    return val_list[1] + val_list[2] + val_list[3] + val_list[4] + val_list[5] + '\n'
"""
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
"""
#Define data formats so it can be compared with the received information the first time (always different so it will always update on the first iteration)
old_datagram_rawS_OUT = '*,*,***,*.***,*,*,***,*,*****,*,+**.*,+****,*,*,*,*,*,*'
tiempo_actual = time.time()
while True:
    try:
        #SETS CONNECTION WITH FLIGHTGEAR TO RECEIVE DATA
        #Creates a new object name Socked_OUT
        Socket_OUT = socket(AF_INET, SOCK_DGRAM)
        #Sets send buffer size to 4096 bytes
        Socket_OUT.setsockopt(SOL_SOCKET, SO_SNDBUF, 4096)
        #Binds the socket to the specified HOST and port (RECEIVES INFO FROM SIMULATOR)
        Socket_OUT.bind((HOST, PORT_OUT))

        #RECEIVE AND PROCESS DATA
        #Sets max received data to 2048 bytes and stores data and sender's address
        datagram_rawB_OUT, adrinput = Socket_OUT.recvfrom(2048)
        #Decodes the received bytes from ASCII to string and removes last character
        datagram_rawS_OUT = datagram_rawB_OUT.decode('ascii')[:-1]
        print(datagram_rawS_OUT)
        """ COMENTADO PARA LA PRUEBA
        #Checks if the values from the simulator have changed and changes are required in screens arduino
        datagram_OUT = encode_datagram_OUT(datagram_rawS_OUT, old_datagram_rawS_OUT)
        #print(datagram_OUT)
        #Encodes result of encode_datagram_OUT
        test1 = datagram_OUT.encode('UTF-8')
        """
        """
        #CONNECTION WITH ARDUINO SCREENS, SENDS DATA
        #Reads one line from arduino_scr serial connection
        test = arduino_scr.readline()
        #Sends datagram to screens arduino
        arduino_scr.write(datagram_OUT.encode('UTF-8'))
        #Updates the old datagram with current one so it is always comparing the one received with the previous one
        old_datagram_rawS_OUT = datagram_rawS_OUT[:]
        """
        #CONNECTION WITH ARDUINO EFIS LEFT, SENDS LED DATA
        #Encodes information containing leds boolean values
        datagram_led = encode_datagram_led(datagram_rawS_OUT)
        print(datagram_led)
        print(datagram_led.encode('UTF-8'))
        # Reads information from buttons arduino
        #datagram_rawB_IN = arduino_EFIS_left.readline()
        # Writes leds datagram to the buttons arduino serial connection
        arduino_EFIS_left.write(datagram_led.encode('UTF-8'))
        print("-----------------------------")
        """
        #CONNECTION WITH ARDUINO EFIS LEFT, RECEIVES INPUTS DATA
        # Decodes the information from buttons arduino
        datagram_rawS_IN = datagram_rawB_IN.decode('UTF-8')
        #print(datagram_rawS_IN)
        if "}" in datagram_rawS_IN and datagram_rawS_IN.index("{") == 0:
            # Delete unnecessary characters: {a,b,c,d,...,z}  -->  a,b,c,d,...,z 
            datagram_rawS_IN = datagram_rawS_IN[1:datagram_rawS_IN.index("}")]
            datagram_posS_IN = encode_datagram_in(datagram_rawS_IN)
            #print(datagram_posS_IN)
        """
        """
        #CONNECTION WITH FLIGHTGEAR TO SEND DATA FROM ARDUINO BUTTONS
        # string_s = '1\n'
        # Creates a new object called s
        s = socket(AF_INET, SOCK_DGRAM)
        # Connects socket to specified HOST and port (SENDS INFO TO SIMULATOR)
        s.connect((HOST, PORT_IN))
        # Sends information to the simulator
        s.send(datagram_posS_IN.encode('ascii'))
        """
        # Clears the console screen
        os.system('cls' if os.name == 'nt' else 'clear')
        """print(datagram_posS_IN.encode('ascii'))
        print(datagram_OUT)"""
        print(datagram_rawS_OUT)







    except:
        print("error")
        var = 0


