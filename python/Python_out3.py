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

time.sleep(7)

def encode_datagram_led(datagram):
    # Split the datagram by commas
    val_list = datagram.split(',')
    # 12 CSTR   1
    # 13 WPT   2
    # 14 VOR.D   3
    # 15 NDB 4
    # 16 ARPT 5
    # 17 FD  6
    # 18 LS 7
    # Concatenate the required values and add a newline character
    return val_list[0] + val_list[1] + val_list[2] + val_list[3] + val_list[4] + '\n'

#Define data formats so it can be compared with the received information the first time (always different so it will always update on the first iteration)
old_datagram_rawS_OUT = '*,*,*,*,*'
tiempo_actual = time.time()
while True:
    try:
    # SETS CONNECTION WITH FLIGHTGEAR TO RECEIVE DATA
        # Creates a new object name Socked_OUT
        Socket_OUT = socket(AF_INET, SOCK_DGRAM)
        # Sets send buffer size to 4096 bytes
        Socket_OUT.setsockopt(SOL_SOCKET, SO_SNDBUF, 4096)
        # Binds the socket to the specified HOST and port (RECEIVES INFO FROM SIMULATOR)
        Socket_OUT.bind((HOST, PORT_OUT))

        # RECEIVE AND PROCESS DATA
        # Sets max received data to 2048 bytes and stores data and sender's address
        datagram_rawB_OUT, adrinput = Socket_OUT.recvfrom(2048)
        # Decodes the received bytes from ASCII to string and removes last character
        datagram_rawS_OUT = datagram_rawB_OUT.decode('ascii')[:-1]
        print(f"Received datagram: {datagram_rawS_OUT}")

        # CONNECTION WITH ARDUINO EFIS LEFT, SENDS LED DATA
        # Encodes information containing leds boolean values
        datagram_led = encode_datagram_led(datagram_rawS_OUT)
        print(f"Encoded datagram for LED: {datagram_led}")
        # Writes leds datagram to the buttons arduino serial connection
        arduino_EFIS_left.write(datagram_led.encode('UTF-8'))
        print(f"Data sent to Arduino:{datagram_led.encode('UTF-8')}")

         # Read response from Arduino
        while arduino_EFIS_left.in_waiting > 0:
            response = arduino_EFIS_left.readline().decode('utf-8').strip()
            print(f"Arduino response: {response}")

        # Clears the console screen
        #os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"error: {e}")
        time.sleep(1)
