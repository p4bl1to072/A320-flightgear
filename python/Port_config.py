import tkinter as tk
from tkinter import messagebox  # Importar el módulo messagebox
from serial.tools import list_ports
import os
import sys
num_disp = 1
def mostrar_advertencia():
    if os.path.isfile("numero_serie.txt"):
        with open("numero_serie.txt", "r") as archivo:
            contenido = archivo.read()
            if contenido.strip():  # Verificar si el contenido no está vacío
                respuesta = messagebox.askyesno("Advertencia", "El archivo 'numero_serie.txt' ya tiene contenido. ¿Deseas sobrescribirlo?")
                if not respuesta:
                    sys.exit()
                else:
                    # Borrar el contenido del archivo si el usuario confirma
                    with open("numero_serie.txt", "w") as archivo:
                        archivo.write("")
    return True



def inicializar_programa():
    mostrar_advertencia()


def guardar_numero_serie():
    global num_disp
    selected_port = port_listbox.get(port_listbox.curselection()) # Obtiene el puerto seleccionado

    try:
        # Obtener información sobre el puerto COM seleccionado
        for port in list_ports.comports():
            if port.description == selected_port:
                serial_number = port.serial_number or "No disponible"
        if num_disp == 1:
            respuesta = messagebox.askyesno("Advertencia"," Este puerto debe ser el Arduino conectado a las pantallas. ¿Es correcto?")
        else:
            respuesta = messagebox.askyesno("Advertencia",
                                            " Este puerto debe ser el Arduino conectado a los botones. ¿Es correcto?")

        if not respuesta:
            resultado_label.config(text="Dispositivo erróneo seleccionado cambie de Arduino")
        else:
            # Leer el contenido actual del archivo
            with open("numero_serie.txt", "r") as archivo:
                contenido_actual = archivo.read()

            # Agregar el nuevo número de serie debajo del contenido actual
            nuevo_contenido = contenido_actual + "\n" + serial_number

            # Guardar el contenido actualizado en el archivo
            with open("numero_serie.txt", "w") as archivo:
                archivo.write(nuevo_contenido)
                num_disp +=1
                resultado_label.config(text="Número de serie guardado con éxito, desconectar arduino")
                puertos_label_device.config(text="Conectar Arduino Botones")
                if num_disp ==3:
                    ventana.quit()
    except Exception as e:
        resultado_label.config(text="Error al obtener el número de serie: " + str(e))


def actualizar_lista_puertos():
    # Obtener la lista de puertos COM disponibles
    ports = [port.description for port in list_ports.comports()]

    # Limpiar la lista actual
    port_listbox.delete(0, tk.END)

    # Llenar la lista con los puertos actualizados
    for port in ports:
        port_listbox.insert(tk.END, port)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Seleccionar Dispositivo COM")


# Configurar la geometría de la ventana
ventana.grid_rowconfigure(1, weight=1)
ventana.columnconfigure(0, weight=1)

# Etiqueta para la lista de puertos
puertos_label_device = tk.Label(ventana, text="Conectar Arduino Pantallas")
puertos_label_device.grid(row=0, column=0, padx=10, pady=10)

# Etiqueta para la lista de puertos
puertos_label = tk.Label(ventana, text="Puertos COM disponibles:")
puertos_label.grid(row=1, column=0, padx=10, pady=10)

# Crear una barra de desplazamiento vertical
scrollbar = tk.Scrollbar(ventana, orient="vertical")

# Obtener la lista de puertos COM disponibles
ports = [port.description for port in list_ports.comports()]

# Crear una lista de puertos con Scrollbar
port_listbox = tk.Listbox(ventana, yscrollcommand=scrollbar.set, selectmode="single")
scrollbar.config(command=port_listbox.yview)

for port in ports:
    port_listbox.insert(tk.END, port)

port_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
scrollbar.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ns")
# Botón para actualizar la lista de puertos
actualizar_boton = tk.Button(ventana, text="Actualizar Puertos", command=actualizar_lista_puertos)
actualizar_boton.grid(row=3, column=0, padx=10, pady=10)

# Botón para guardar el número de serie
guardar_boton = tk.Button(ventana, text="Guardar Número de Serie", command=guardar_numero_serie)
guardar_boton.grid(row=4, column=0, padx=10, pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="")
resultado_label.grid(row=5, column=0, padx=10, pady=10)


inicializar_programa()
ventana.mainloop()