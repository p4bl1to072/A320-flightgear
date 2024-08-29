import sys
from socket import *
import psutil
import serial
from serial.tools import list_ports
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("flightgear_arduino.log"),
    logging.StreamHandler()
])

nombre_proceso = "fgfs.exe"

time.sleep(25)
HOST = "127.0.0.1"  # Local HOST
PORT_OUT = 8040 # Puerto salida
PORT_IN = 8000  # Puerto entrada

if os.path.isfile("numero_serie.txt"):
    with open('numero_serie.txt', 'r') as archivo:
        lineas = archivo.readlines()
    if len(lineas) >= 2:
        serial_number_buttons_EFIS_left = lineas[1].strip()
        logging.info(f"Arduino Serial Number: {serial_number_buttons_EFIS_left}")
    else:
        logging.error("Configurar el puerto del arduino del EFIS")
        sys.exit(1)
else:
    logging.error("Configurar los puertos del arduino usando la interfaz")
    sys.exit(1)

# List of used serial ports (in no particular order)
ports = serial.tools.list_ports.comports()
arduino_EFIS_left = None

for port in ports:
    logging.info(f"Checking port: {port.device} with serial number {port.serial_number}")
    if port.serial_number == serial_number_buttons_EFIS_left:
        puerto_button_EFIS_left = port.device
        try:
            arduino_EFIS_left = serial.Serial(port=puerto_button_EFIS_left, baudrate=1000000, timeout=0.1)
            logging.info(f"Connected to Arduino on port: {puerto_button_EFIS_left}")
        except Exception as e:
            logging.error(f"Failed to connect to Arduino: {e}")
            sys.exit(1)

if arduino_EFIS_left is None:
    logging.error("Could not find the Arduino with the specified serial number.")
    sys.exit(1)

time.sleep(7)

def encode_datagram_led(datagram):
    val_list = datagram.split(',')
    return val_list[0] + val_list[1] + val_list[2] + val_list[3] + val_list[4] + '\n'

def transform_serial_info_EFIS(response_EFIS):
    stripped_response = response_EFIS.strip('{}')
    logging.info(f"After strip: {stripped_response}")
    split_response = stripped_response.split(',')
    logging.info(f"After split: {split_response}")
    button_names = ["CSTR", "WPT", "VORD", "NDB", "ARPT"]
    for i, state in enumerate(split_response[1:6]):
        if state == '1':
            logging.info(f"Button pressed: {button_names[i]}")
            return button_names[i] + '\n'
    return "OFF"

old_datagram_rawS_OUT = '*,*,*,*,*'
tiempo_actual = time.time()

Socket_OUT = socket(AF_INET, SOCK_DGRAM)
Socket_OUT.setsockopt(SOL_SOCKET, SO_SNDBUF, 4096)
Socket_OUT.bind((HOST, PORT_OUT))

Socket_IN = socket(AF_INET, SOCK_DGRAM)
Socket_IN.setsockopt(SOL_SOCKET, SO_SNDBUF, 4096)
Socket_IN.connect((HOST, PORT_IN))

while True:
    try:
        datagram_rawB_OUT, adrinput = Socket_OUT.recvfrom(2048)
        datagram_rawS_OUT = datagram_rawB_OUT.decode('ascii')[:-1]
        logging.info(f"Received datagram from FlightGear: {datagram_rawS_OUT}")

        datagram_led = encode_datagram_led(datagram_rawS_OUT)
        logging.info(f"Encoded datagram for LED: {datagram_led}")
        arduino_EFIS_left.write(datagram_led.encode('UTF-8'))
        logging.info(f"Data sent to Arduino (LED): {datagram_led.encode('UTF-8')}")

        while arduino_EFIS_left.in_waiting > 0:
            try:
                response_EFIS_left = arduino_EFIS_left.readline().decode('utf-8').strip()
                logging.info(f"Arduino response: {response_EFIS_left}")
                button_pressed = transform_serial_info_EFIS(response_EFIS_left)
                Socket_IN.send(button_pressed.encode('utf-8'))
                logging.info(f"Data sent to FlightGear: {button_pressed}")
            except Exception as e:
                logging.error(f"Error reading from Arduino: {e}")

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        time.sleep(1)
