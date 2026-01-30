from pynput.keyboard import Listener, Key #Me parece que gta v no lo detecta
from pynput.mouse import Button, Controller
import keyboard
import random
import time 
import sys, os
from tkinter.font import Font
import customtkinter as ctk
from customtkinter import *
import threading
from PIL import Image

window = ctk.CTk()
#Valores default
MIN_DELAY, sk_MIN_DELAY = 8.1, 5.2
MAX_DELAY, sk_MAX_DELAY = 38.2, 26.1
MIN_HOLD = 0.4
MAX_HOLD = 0.7
#Valores elegidos por usuario
user_MIN_DELAY, sk_user_MIN_DELAY = 0.0, 0.0
user_MAX_DELAY, sk_user_MAX_DELAY = 0.0, 0.0
user_MIN_HOLD = 0.0
user_MAX_HOLD = 0.0
#Single key param
recordingKey = False
selectedKey = ctk.StringVar(master=window, value="space")
text_selectedKey = ctk.StringVar(master=window, value=f"Selected key: {selectedKey.get().upper()}")
keyWaitTime = 15
#Teclas aceptadas
wasdKeys = ["w","a","s","d"]
#------------------------------
startButtonText = ctk.StringVar()
startButtonText.set("Go AFK")
mode = ctk.StringVar(value="wasd")
AFK = False
#COLORS
Fondo = "#071C2F"
Panels = "#0B2A45"
Texto = " #C7D6E5"
BotonActivo = "#1F6AE1"
BotonInactivo = "#0B2A45"
startButtonColorOFF, startButtonTextColorOFF = "#1E7F43", "#E9FFF1"
startButtonColorON, startButtonTextColorON = "#9B2C2C", "#FFECEC"
#-----------------------------------------------

#PARA EL ICONO
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
window.iconbitmap(resource_path("assets/AntiAFK_Icon.ico"))
# -

def only_float(value):
    # SI EL VALOR ES VACÍO, permitimos (esto hace que el placeholder sea visible)
    if value == "":
        return True
    
    # Permitir caracteres iniciales para poder escribir el número
    if value in ["."]:
        return True
        
    try:
        float(value)
        return True
    except ValueError:
        return False

#?
def safe_float(x, default):
    try:
        if x is None or x == "":
            return default
        return float(x)
    except Exception:
        return default

def apply_wasd_user_values():
    global new_MIN_DELAY, new_MAX_DELAY, new_MIN_HOLD, new_MAX_HOLD
    user_MIN_DELAY = wasdDelayMin.get()
    user_MAX_DELAY = wasdDelayMax.get()
    user_MIN_HOLD = wasdHoldMin.get()
    user_MAX_HOLD = wasdHoldMax.get()

    new_MIN_DELAY = safe_float(user_MIN_DELAY, MIN_DELAY)
    new_MAX_DELAY = safe_float(user_MAX_DELAY, MAX_DELAY)
    new_MIN_HOLD = safe_float(user_MIN_HOLD, MIN_HOLD)
    new_MAX_HOLD = safe_float(user_MAX_HOLD, MAX_HOLD)

    # Validaciones básicas: min <= max
    if new_MIN_DELAY > new_MAX_DELAY:
        # swap or correct: aca decido intercambiar para que tenga sentido
        new_MIN_DELAY, new_MAX_DELAY = new_MAX_DELAY, new_MIN_DELAY

    if new_MIN_HOLD > new_MAX_HOLD:
        new_MIN_HOLD, new_MAX_HOLD = new_MAX_HOLD, new_MIN_HOLD
        
def apply_singleKey_user_values():
    global sk_new_MIN_DELAY, sk_new_MAX_DELAY

    sk_user_MIN_DELAY = singleKeyDelayMin.get()
    sk_user_MAX_DELAY = singleKeyDelayMax.get()

    sk_new_MIN_DELAY = safe_float(sk_user_MIN_DELAY, sk_MIN_DELAY)
    sk_new_MAX_DELAY = safe_float(sk_user_MAX_DELAY, sk_MAX_DELAY)

    if sk_new_MIN_DELAY > sk_new_MAX_DELAY:
        sk_new_MIN_DELAY, sk_new_MAX_DELAY = sk_new_MAX_DELAY, sk_new_MIN_DELAY

       


#Logica de los diferentes modos aca
def wasd():
    apply_wasd_user_values()
    key = random.choice(wasdKeys)
    hold = random.uniform(new_MIN_HOLD,new_MAX_HOLD)  #Este hay que cambiarlo pa que el usuario pueda elegir EN PROGRESO
    intervalo = random.uniform(new_MIN_DELAY,new_MAX_DELAY) #Este lo mismo
    time.sleep(intervalo)
    print (f"Tecla {key} presionada por {hold:.2f} segundos.")
    keyboard.press(key)
    time.sleep(hold)
    keyboard.release(key)
    print(f"Esperando {intervalo:.2f} segundos para el siguiente input...")
    time.sleep(intervalo)
 
def mouse_click():
        mouse = Controller()
        time.sleep(float(sliderValue.get()))
        mouse.click(Button.left,1)
        time.sleep(0.1)


def single_key():
    apply_singleKey_user_values()
    key = selectedKey.get()
    keyWaitTime = random.uniform(sk_new_MIN_DELAY, sk_new_MAX_DELAY)
    time.sleep(keyWaitTime)
    keyboard.press(key)
    time.sleep(0.5)
    keyboard.release(key)
    

def minimal_movement():
    key = random.choice(wasdKeys)
    time.sleep(16)
    keyboard.press(key)
    time.sleep(0.6)
    keyboard.release(key)
    time.sleep(16)

#Esta funcion tan sencilla pone arriba de todo el frame seleccionado, puto el que lee btw
def show_frame(frame):
    frame.tkraise()

#Actualiza el color de los botones
def update_mode_buttons():
    active = BotonActivo
    normal = BotonInactivo
    #Muchos IFs ¿Se podra mejorar?
    wasdButton.configure(
        fg_color=active if mode.get() == "wasd" else normal,
        hover_color=active if mode.get() == "wasd" else normal,
        border_color="#3A8DFF",
        border_width=2 if mode.get() == "wasd" else 0
    )
    mouseButton.configure(
        fg_color=active if mode.get() == "mouseClick" else normal,
        hover_color=active if mode.get() == "mouseClick" else normal,
        border_color="#3A8DFF",
        border_width=2 if mode.get() == "mouseClick" else 0
    )
    singlekButton.configure(
        fg_color=active if mode.get() == "singleKey" else normal,
        hover_color=active if mode.get() == "singleKey" else normal,
        border_color="#3A8DFF",
        border_width=2 if mode.get() == "singleKey" else 0
    )
    minimalMoveButton.configure(
        fg_color=active if mode.get() == "minimalMovement" else normal,
        hover_color=active if mode.get() == "minimalMovement" else normal,
        border_color="#3A8DFF",
        border_width=2 if mode.get() == "minimalMovement" else 0
    )

#Para grabar la tecla en el modo SingleKey
def on_key_press(key):
    global recordingKey

    if key == Key.esc:
        text_selectedKey.set("Selected key: CANCELLED")
        recordingKey = False
        recordButton.configure(
           text="Click to record a key",
            fg_color="#1C3A69",
            hover_color="#255AA8",
            state="normal"
        )
        return False

    try:
        k = key.char
    except AttributeError:
        k = str(key).replace("Key.", "")

    selectedKey.set(k)
    text_selectedKey.set(f"Selected key: {k.upper()}")
    recordingKey = False
    
    recordButton.configure(
        text="Click to record a key",
        fg_color=BotonActivo,
        border_color="#3A8DFF",
        border_width=2,
        hover_color="#255AA8",
        state="normal"
    )
    return False
def recordKey():
    global recordingKey

    if recordingKey:
        
        return

    recordingKey = True
    text_selectedKey.set("Press a key...")

    recordButton.configure(
        text="Recording...",
        fg_color="#9B2C2C",
        border_color="#C74A4A",
        border_width=2,
        hover_color="#9B2C2C",
        state="disabled"
    )
    
    Listener(on_press=on_key_press).start()

# "Selector" de modos :)
def afk_loop():
    modos = {
         "wasd": wasd,
         "mouseClick": mouse_click,
         "singleKey": single_key,
         "minimalMovement": minimal_movement    
    }

    while True:
        if AFK:
            modo_actual = mode.get()
            if modo_actual in modos:
                modos[modo_actual]()
            else: time.sleep(0.2)
        else: time.sleep(0.2)    

#No entendi bien como hice esto
def set_mode(m):
    mode.set(m)
    update_mode_buttons()

#Logica boton
def irseAFK():
    global AFK
    global startButtonText
    global startButton
    if not AFK:
        AFK = True
        startButtonText.set("Stop")
        startButton.configure(
            fg_color=startButtonColorON,
            border_color="#FF4D4D",
            border_width=2, 
            text_color=startButtonTextColorON,
            hover_color=startButtonColorON
        )
    else:
        AFK = False
        startButtonText.set("Go AFK")
        startButton.configure(
            fg_color=startButtonColorOFF, 
            text_color=startButtonTextColorOFF,
            border_color="#269B53",
            border_width=2,
            hover_color=startButtonColorOFF
        )


#Tkinter
window.geometry("1170x630")
window.title("Anti AFK")
window.configure(bg=Fondo)
window.minsize(1170, 620)

#Main Body
leftFrame = CTkFrame(window, corner_radius=0, fg_color=Panels)
rightFrame = CTkFrame(window,corner_radius=0,  fg_color=Fondo,bg_color=Fondo)
window.columnconfigure(0, minsize=330)
window.columnconfigure(1, weight=1)
window.rowconfigure(0,weight=1)
#packFrames
leftFrame.grid(row=0, column=0, sticky="nsew")
rightFrame.grid(row=0, column=1, sticky="nsew")
leftFrame.propagate(False)


#LeftContent
nameText = CTkLabel(master=leftFrame, text="AntiAFK", font=("Segoe UI", 38))
modesFrame =CTkFrame(master=leftFrame, fg_color=Panels, bg_color=Panels)
selectText= CTkLabel(master=modesFrame, text="Select a mode", font=("Segoe UI", 22, "bold"))
wasdButton = CTkButton(master=modesFrame, text="Movement", command= lambda: (set_mode("wasd"), show_frame(wasd_frame)), height=30, width=330, font=("Segoe UI", 22), fg_color="#1C3A69", bg_color="transparent")
mouseButton = CTkButton(master=modesFrame, text="Clicker", command= lambda: (set_mode("mouseClick"), show_frame(clicker_frame)), height=30, width=330, font=("Segoe UI", 22), fg_color="#1C3A69", bg_color="transparent") 
singlekButton = CTkButton(master=modesFrame, text="Single Key", command= lambda: (set_mode("singleKey"), show_frame(singlekey_frame)), height=30, width=330, font=("Segoe UI", 22), fg_color="#1C3A69", bg_color="transparent")
minimalMoveButton = CTkButton(master=modesFrame, text="Minimal Movement", command= lambda: (set_mode("minimalMovement"), show_frame(minimal_frame)), height=30, width=330, font=("Segoe UI", 22), fg_color="#1C3A69", bg_color="transparent")

startButton = CTkButton(master=leftFrame, textvariable=startButtonText, command=irseAFK, height=45, width=330, fg_color=startButtonColorOFF, hover_color=startButtonColorOFF,border_color="#269B53",border_width=2,font=("Segoe UI", 22))

#rightContent
wasd_frame = CTkFrame(rightFrame, fg_color= "transparent", bg_color="transparent")
clicker_frame = CTkFrame(rightFrame, fg_color= "transparent", bg_color="transparent")
singlekey_frame = CTkFrame(rightFrame, fg_color= "transparent", bg_color="transparent")
minimal_frame = CTkFrame(rightFrame, fg_color= "transparent", bg_color="transparent")

for frame in (wasd_frame,clicker_frame,singlekey_frame,minimal_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

info_icon = ctk.CTkImage(Image.open(resource_path("assets/info_icon.png")),size=(20,20))

# - PREFABS -
def create_info_frame(master, text):
    frame =CTkFrame(
        master=master,
        corner_radius=14,
        fg_color=Panels,
        bg_color="transparent"
    )
    frame.pack_propagate(True)
    
    iconLabel =CTkLabel(
        master=frame,
        text="",
        image=info_icon,
        width=5,
        
    )
    iconLabel.pack(side="left",padx=(20,0), pady=(15), anchor="n")
    
    infoText = CTkLabel(
        master=frame,
        text=text,
        wraplength=780,
        justify="left",
        anchor="w",           
        font=("Segoe UI", 18)
    )
    infoText.pack(pady=15, fill="x",padx=(10,20))
    return frame

def create_option_frame(master, title_text, entry1PHText, entry2PHText, width=400, height=300):
    frame = CTkFrame(
        master=master,
        corner_radius=14,
        width=width,
        height=height,
        fg_color=Panels,
        bg_color="transparent"    
    )
    frame.pack_propagate(False)
    title = CTkLabel(
        master=frame,
        text=title_text,
        font=("Segoe UI", 22)
    )
    title.pack(pady=(10,20))

    vcmd = (window.register(only_float), "%P")
    
    entry1 = CTkEntry(master=frame, placeholder_text= entry1PHText, corner_radius=25, text_color="#E6F1FF",placeholder_text_color="#8FA8BF", fg_color="#0E3557",border_color="#1A3E5F", width= 255, height= 37, font=("Segoe UI", 13))
    entry2 = CTkEntry(master=frame, placeholder_text= entry2PHText, corner_radius=25, text_color="#E6F1FF",placeholder_text_color="#8FA8BF", fg_color="#0E3557",border_color="#1A3E5F", width= 255, height= 37, font=("Segoe UI", 13))
    entry1.configure(validate="key", validatecommand=vcmd)
    entry2.configure(validate="key", validatecommand=vcmd)
    
    entry1.pack(pady=5)
    entry2.pack(pady=5)

    return frame, entry1, entry2

def create_slider_frame(master, title_text, width=400, height=300):
    frame =CTkFrame(
        master=master,
        corner_radius=14,
        width=width,
        height=height,
        fg_color=Panels    
    )
    frame.pack_propagate(False)

    title =CTkLabel(
        master = frame,
        text= title_text,
        font=("Segoe UI", 22)
    )
    title.pack(pady=(10,20))

    sliderValue = StringVar(value= 10)

    sliderText =CTkLabel(
        master = frame,
        textvariable = sliderValue,    # HAY QUE INDICAR QUE SON SEGUNDOS!
        font=("Segoe UI", 19)
    )
    sliderText.pack(pady=5)
    
    def on_slider_change(v):
        sliderValue.set(f"{float(v):.2f}")


    slider = CTkSlider(
        master = frame,
        from_= 0.5,
        to = 60,
        width= 250,
        height = 30,
        button_color=BotonActivo,
        command=on_slider_change
    )
    slider.set(10)
    slider.pack(pady=10)

    return frame, slider, sliderValue

def create_recordKey_Frame(master, title_text, comando, width=400, height=300):
    frame =CTkFrame(
        master=master,
        corner_radius=14,
        width=width,
        height=height,
        fg_color=Panels    
    )
    frame.pack_propagate(False)
    
    title = CTkLabel(
        master = frame,
        text= title_text,
        font=("Segoe UI", 22)
    )
    title.pack(pady=(10,20))
    
    recordButton = CTkButton(
        master= frame,
        text="Click to record a key",
        fg_color=BotonActivo,
        border_color="#3A8DFF",
        border_width=2,
        hover_color="#255AA8",
        width= 280,
        height = 100,
        command= comando
    )
    recordButton.pack(pady=(40,20))
    
    actualKeyText = CTkLabel(
        master=frame,
        textvariable = text_selectedKey
    )
    actualKeyText.pack()
    return frame, recordButton
    

# - WASD frames -
wasdInfoText = create_info_frame(
    master=wasd_frame,
    text="This mode press WASD keys randomly to move the character.\nYou can modify the delay from key to key and how much time that key is gonna be pressed."
)
wasdDelayFrame, wasdDelayMin, wasdDelayMax = create_option_frame(
    master=wasd_frame, 
    title_text="Time between keys", 
    entry1PHText=f"Minimum delay — by default: {MIN_DELAY:.2f}s", 
    entry2PHText=f"Maximum delay — by default: {MAX_DELAY:.2f}s")
wasdHoldFrame, wasdHoldMin, wasdHoldMax = create_option_frame(
    master=wasd_frame,
    title_text="Time between pulsations", 
    entry1PHText=f"Minimun hold — by default: {MIN_HOLD:.2f}s", 
    entry2PHText=f"Maximum hold — by default: {MAX_HOLD:.2f}s")

# - CLICKER frames -
clickerInfoText = create_info_frame(
    master=clicker_frame,
    text="This mode automatically clicks the left mouse button.\nYou can configure the time between clicks with the slider."
)
mouseClickFrame, mouseClickRate, sliderValue = create_slider_frame(
    master=clicker_frame,
    title_text="Click Rate"
)
# - SingleKey frames -
singleKeyInfoText = create_info_frame(
    master=singlekey_frame,
    text="This mode repeatedly presses a single key selected by the user.\nYou can configure the delay between presses.\n\nUseful for actions that require repeated input."
)
recordKeyFrame, recordButton = create_recordKey_Frame(
    master=singlekey_frame,
    title_text= "Key selection",
    comando= recordKey
    )
singleKeyOptionFrame, singleKeyDelayMin, singleKeyDelayMax= create_option_frame(
    master=singlekey_frame,
    title_text="Time between keys",
    entry1PHText=f"Minimum delay — by default: {sk_MIN_DELAY:.2f}s", 
    entry2PHText=f"Maximum delay — by default: {sk_MAX_DELAY:.2f}s"
)
# - MinimalMovement frames -
minimalMovementInfoText = create_info_frame(
    master=minimal_frame,
    text="This mode performs minimal and subtle movements to prevent AFK detection.\nIt is designed to be less noticeable while keeping the session active.\n\nIdeal for situations where minimal input is required to stay active."
)
warningText = create_info_frame(master=minimal_frame, text="There is no configuration available at the moment.")

# pack all option frames
#-
wasdInfoText.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
wasdDelayFrame.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
wasdHoldFrame.grid(row=1, column=1, sticky="nw", padx=10, pady=10)
wasd_frame.columnconfigure(0, weight=0)
wasd_frame.columnconfigure(1, weight=1)
#-
clickerInfoText.grid(row=0, column=0,columnspan=2, sticky="ew", padx=10, pady=10)
mouseClickFrame.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
clicker_frame.columnconfigure(0,weight=0)
clicker_frame.columnconfigure(1, weight=1)
#-
singleKeyInfoText.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
recordKeyFrame.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
singleKeyOptionFrame.grid(row=1, column=1, sticky="nw", padx=10, pady=10)
singlekey_frame.columnconfigure(0, weight=0)
singlekey_frame.columnconfigure(1, weight=1)
#-
minimalMovementInfoText.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
warningText.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
minimal_frame.columnconfigure(0,weight=0)
minimal_frame.columnconfigure(1, weight=1)



#Pack general things
nameText.pack(side=TOP, pady=(20,1), padx=7)
startButton.pack(side=BOTTOM, pady=7,padx=5)
selectText.pack(pady=(1,3))
modesFrame.pack(pady=50,padx=5)
wasdButton.pack(pady=6)
mouseButton.pack(pady=6)
singlekButton.pack(pady=6)
minimalMoveButton.pack(pady=6)

show_frame(wasd_frame) #Para que la primera TAB que aparezca sea la de WASD
update_mode_buttons() #Para que aparezca seleccionado el WASD al abrir el programa
threading.Thread(target=afk_loop, daemon=True).start() #Para que funcione todo junto, no se como funciona
window.mainloop()