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
    if len(lineas) >= 3:  # Ensure at least 3 lines for two Arduino devices
        serial_number_buttons_EFIS_left = lineas[1].strip()
        serial_number_screen = lineas[2].strip()  # Serial number for the screen Arduino
        logging.info(f"Arduino Serial Number (EFIS): {serial_number_buttons_EFIS_left}")
        logging.info(f"Arduino Serial Number (Screen): {serial_number_screen}")
    else:
        logging.error("Configurar el puerto del arduino del EFIS y de la pantalla")
        sys.exit(1)
else:
    logging.error("Configurar los puertos del arduino usando la interfaz")
    sys.exit(1)

# List of used serial ports (in no particular order)
ports = serial.tools.list_ports.comports()
arduino_EFIS_left = None
arduino_screen = None  # New variable for the screen Arduino

for port in ports:
    logging.info(f"Checking port: {port.device} with serial number {port.serial_number}")
    if port.serial_number == serial_number_buttons_EFIS_left:
        puerto_button_EFIS_left = port.device
        try:
            arduino_EFIS_left = serial.Serial(port=puerto_button_EFIS_left, baudrate=1000000, timeout=0.1)
            logging.info(f"Connected to Arduino on port: {puerto_button_EFIS_left}")
        except Exception as e:
            logging.error(f"Failed to connect to Arduino (EFIS): {e}")
            sys.exit(1)
    elif port.serial_number == serial_number_screen:  # Check for screen Arduino
        puerto_screen = port.device
        try:
            arduino_screen = serial.Serial(port=puerto_screen, baudrate=115200, timeout=0.1)  # Adjust baud rate as needed
            logging.info(f"Connected to Screen Arduino on port: {puerto_screen}")
        except Exception as e:
            logging.error(f"Failed to connect to Arduino (Screen): {e}")
            sys.exit(1)

if arduino_EFIS_left is None or arduino_screen is None:  # Check if both Arduinos are connected
    logging.error("Could not find one or both Arduinos with the specified serial numbers.")
    sys.exit(1)

time.sleep(7)

def encode_datagram_led_EFIS(datagram):
    val_list = datagram.split(',')
    return val_list[4] + val_list[5] + val_list[6] + val_list[7] + val_list[8] +val_list[9] + val_list [10] + '\n'

def encode_datagram_screen(new_datagram, old_datagram):
    # This function compares the new datagram with the previous one
    # and determines if there are any changes that need to be reflected on the screen.

    # Splitting the datagrams into lists
    val_list = new_datagram.split(',')
    o_val_list = old_datagram.split(',')

    # Checking for changes in the relevant fields (0 to 3)
    if val_list[0:4] != o_val_list[0:4]:
        s1 = '1'
    else:
        s1 = '0'

    # Constructing the datagram to send to the Arduino
    datagram_out = val_list[0] + val_list[1] + val_list[2] + val_list[3] + s1 + '\n'

    return datagram_out

def encode_datagram_led_WARNINGS(datagram):
    val_list = datagram.split(',')
    return val_list[11] + val_list[12] + val_list[13] + val_list[14] + '\n'

def transform_serial_info_EFIS(response_EFIS):
    stripped_response = response_EFIS.strip('{}')
    logging.info(f"After strip: {stripped_response}")
    split_response = stripped_response.split(',')
    logging.info(f"After split: {split_response}")
    
    # Create a string for the first 5 button states
    transformed_response = ','.join(split_response) +'\n'

    logging.info(f"Transformed response from EFIS: {transformed_response}")
    
    return transformed_response

old_datagram_rawS_OUT = '*,*,****,*****,*'
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

        datagram_led = encode_datagram_led_EFIS(datagram_rawS_OUT)
        datagram_screen = encode_datagram_screen(datagram_rawS_OUT,old_datagram_rawS_OUT)
        datagram_warnings = encode_datagram_led_WARNINGS(datagram_rawS_OUT)
        logging.info(f"Encoded datagram for LED EFIS: {datagram_led}")
        logging.info(f"Encoded datagram for screen: {datagram_screen}")
        logging.info(f"Encoded datagram for LED WARNINGS: {datagram_warnings}")

        arduino_EFIS_left.write(datagram_led.encode('UTF-8'))
        logging.info(f"Data sent to Arduino (LED): {datagram_led.encode('UTF-8')}")

        arduino_screen.write(datagram_screen.encode('UTF-8'))  # Send data to the screen Arduino
        logging.info(f"Data sent to Screen Arduino: {datagram_screen.encode('UTF-8')}")

        while arduino_EFIS_left.in_waiting > 0:
            try:
                response_EFIS_left = arduino_EFIS_left.readline().decode('utf-8').strip()
                logging.info(f"Arduino response: {response_EFIS_left}")
                button_states = transform_serial_info_EFIS(response_EFIS_left)
                Socket_IN.send(button_states.encode('ascii'))
                logging.info(f"Data sent to FlightGear: {button_states}")
            except Exception as e:
                logging.error(f"Error reading from Arduino: {e}")

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        time.sleep(1)
