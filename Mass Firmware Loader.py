#!/usr/bin/env python3

from cmath import e
import subprocess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


# Interfaz gráfica
# Ruta absoluta al archivo que se va a cargar en masa
FILE_PATH = "File to sideload"

# Variables globales
deviceList = []

# Inicialización de ventana
root = Tk()
window_title = "Mass Firmware Loader v0.1"
root.title(window_title)
root.geometry("400x500")
root.resizable(False, False)

# Frame para dispositivos
devices_frame = LabelFrame(root, text="Dispositivos")
devices_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=1, rowspan=3)
root.columnconfigure(0, weight=1)

# Frame para .zip
path_frame = LabelFrame(root, text="Cargar .zip")
path_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

path_label = Label(path_frame, borderwidth=1, text="Ruta del archivo .zip", relief="sunken", width=16, foreground="gray")
path_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Frame para botones

buttons_frame = LabelFrame(root, text="Confirmar")
buttons_frame.grid(row=2, column=1, padx=10, pady=10, columnspan=1, sticky="ew")

# Frame para filtros
filters_frame = LabelFrame(root, text="Filtros")
filters_frame.grid(row=0, column=1, padx=10, pady=10, columnspan=1, sticky="ew")

# Lógica botones
# Seleccionar todo
def select_all():
    for var in chk_var:
        var.set(1)

# Deseleccionar todo
def deselect_all():
    for var in chk_var:
        var.set(0)

# Cargar firmware
def load_firmware():
    # Cargar los archivos

    if len(deviceList) > 0:
        counter = 0
        for button in chk:
            if chk_var[counter].get() == 1:
                try:
                    subproc = subprocess.Popen(["adb", "-s", button.cget("text"), "sideload", FILE_PATH])
                    print("ID: " + button.cget("text") + " " + "\n" + FILE_PATH)
                    counter+=1
                except:
                    print("Ha ocurrido un error. Verifique que la dirección del archivo .zip esté bien escrita")
            else:
                counter+=1
                continue
    else:
        print("No se detectaron dispositivos conectados.")
        print("Conecte al menos un dispositivo, espere a que se instalen los drivers y pruebe nuevamente.")

def update_devices():
    counter = 0
    global chk_var
    global chk
    chk_var = []
    chk = []

    try:
        for element in devices_frame.winfo_children():
            element.destroy()
    except:
        return


    # Limpiar salida de "adb devices" para dejar sólo el texto 
    process = subprocess.check_output(["adb", "devices"])
    devices = str(process)
    devices = devices.replace("\\r", " ")
    devices = devices.replace("\\n", " ")
    devices = devices.replace("b", " ")
    devices = devices.replace("\\t", " ")
    devices = devices.replace("'", "")

    # Filtrar sólo los ID y guardarlos en deviceList
    bannedWords = ["List", "of", "devices", "device", "attached", "sideload", "unauthorized"]
    global deviceList
    deviceList = []

    for word in devices.split():
        if word not in bannedWords:
            deviceList.append(word)

    for device in deviceList:
        chk_var.append("var" + str(counter))
        chk_var[counter] = IntVar()

        chk.append("checkbutton" + str(counter))
        chk[counter] = Checkbutton(devices_frame, text=device, variable=chk_var[counter])
        chk[counter].grid(row=counter, column=0, padx=8,sticky="w")

        counter+=1
        
    
def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Selecciona un archivo", 
                                          filetypes = (("zip files", "*.zip*"), 
                                                        ("all files", "*.*")))
    path_label.configure(text=filename)
    global FILE_PATH
    FILE_PATH = filename

# Botones
select_all_button = Button(filters_frame, text="Seleccionar todo", command=select_all)
select_all_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

unselect_all_button = Button(filters_frame, text="Deseleccionar todo", command=deselect_all)
unselect_all_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

update_devices_button = Button(filters_frame, text="Actualizar dispositivos", command=update_devices)
update_devices_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

load_firmware_button = Button(buttons_frame, text="Cargar firmware", command=load_firmware)
load_firmware_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
buttons_frame.columnconfigure(0, weight=1)

path_label_button = Button(path_frame, text="Buscar", width=10, command=browse_files)
path_label_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
path_frame.columnconfigure(0, weight=1)

add_alias_button = Button(filters_frame, text="Añadir alias", state=DISABLED)
add_alias_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Cargar archivo zip", command=browse_files)
filemenu.add_separator()
filemenu.add_command(label="Cerrar", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Seleccionar todo", command=select_all)
editmenu.add_command(label="Deseleccionar todo", command=deselect_all)
menubar.add_cascade(label="Editar", menu=editmenu)

update_devices()

root.config(menu=menubar)

root.mainloop()