import subprocess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


# Interfaz gráfica
# Ruta absoluta al archivo que se va a cargar en masa
FILE_PATH = "File to sideload"

# Inicialización de ventana
top = Tk()
window_title = "Mass Firmware Loader v0.1"
top.title(window_title)
top.geometry("400x500")
top.resizable(False, False)

# Frame para dispositivos
devices_frame = LabelFrame(top, text="Dispositivos")
devices_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=1, rowspan=3)
top.columnconfigure(0, weight=1)

# Frame para .zip
path_frame = LabelFrame(top, text="Cargar .zip")
path_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

path_label = Label(path_frame, borderwidth=1, text="Ruta del archivo .zip", relief="sunken", width=16, foreground="gray")
path_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Frame para botones

buttons_frame = LabelFrame(top, text="Confirmar")
buttons_frame.grid(row=2, column=1, padx=10, pady=10, columnspan=1, sticky="ew")

# Frame para filtros
filters_frame = LabelFrame(top, text="Filtros")
filters_frame.grid(row=0, column=1, padx=10, pady=10, columnspan=1, sticky="ew")

# Limpiar salida de "adb devices" para dejar sólo el texto 
process = subprocess.check_output("adb devices")
devices = str(process)
devices = devices.replace("\\r", " ")
devices = devices.replace("\\n", " ")
devices = devices.replace("b", " ")
devices = devices.replace("\\t", " ")
devices = devices.replace("'", "")

# Filtrar sólo los ID y guardarlos en deviceList
bannedWords = ["List", "of", "devices", "device", "attached", "sideload", "unauthorized"]
deviceList = []

for word in devices.split():
    if word not in bannedWords:
        deviceList.append(word)

# Lista dispositivos guardados en deviceList en forma de Checkboxes y les asigna su respectiva variable
counter = 0
chk_var = []
chk = []
for device in deviceList:
    chk_var.append("var" + str(counter))
    chk_var[counter] = IntVar()

    chk.append("checkbutton" + str(counter))
    chk[counter] = Checkbutton(devices_frame, text=device, variable=chk_var[counter])
    chk[counter].grid(row=counter, column=0, padx=8,sticky="w")

    counter+=1

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
                    subproc = subprocess.Popen(["adb", "-s", button.cget("text"), "sideload", FILE_PATH], stdout=subprocess.PIPE)
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

    for element in devices_frame.winfo_children():
        element.destroy()

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
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Cargar archivo zip", command=browse_files)
filemenu.add_separator()
filemenu.add_command(label="Cerrar", command=top.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Seleccionar todo", command=select_all)
editmenu.add_command(label="Deseleccionar todo", command=deselect_all)
menubar.add_cascade(label="Editar", menu=editmenu)


top.config(menu=menubar)

if "unauthorized" in devices:
    messagebox.askokcancel(message="Uno o más dispositivos requieren autorización para continuar. \nAutorice e intente de nuevo")

top.mainloop()