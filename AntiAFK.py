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

#Valores default
MIN_DELAY = 8.1
MAX_DELAY = 38.2
MIN_HOLD = 0.4
MAX_HOLD = 0.7
#Valores elegidos por usuario
user_MIN_DELAY = 0.0
user_MAX_DELAY = 0.0
user_MIN_HOLD = 0.0
user_MAX_HOLD = 0.0
#Single key param
selectedKey = "space"
keyWaitTime = 15
#Teclas aceptadas
wasdKeys = ["w","a","s","d"]
#------------------------------
window = ctk.CTk()
startButtonText = ctk.StringVar()
startButtonText.set("Irse AFK")
mode = ctk.StringVar(value="wasd")
AFK = False
#-----------------------------------------------

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
    key = selectedKey
    time.sleep(keyWaitTime)
    keyboard.press(key)
    time.sleep(0.8)
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
    active = "#e8890e"
    normal = "#1f6aa5"
    #Muchos IFs ¿Se podra mejorar?
    wasdButton.configure(fg_color=active if mode.get() == "wasd" else normal, hover_color=active if mode.get() == "wasd" else normal)
    mouseButton.configure(fg_color=active if mode.get() == "mouseClick" else normal, hover_color=active if mode.get() == "mouseClick" else normal)
    singlekButton.configure(fg_color=active if mode.get() == "singleKey" else normal, hover_color=active if mode.get() == "singleKey" else normal)
    minimalMoveButton.configure(fg_color=active if mode.get() == "minimalMovement" else normal, hover_color=active if mode.get() == "minimalMovement" else normal)

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
            else: time.sleep(0.1)
        else: time.sleep(0.1)    

#No entendi bien como hice esto
def set_mode(m):
    mode.set(m)
    update_mode_buttons()

#Logica boton
def irseAFK():
    global AFK
    global startButtonText
    if not AFK:
        AFK = True
        startButtonText.set("Detener")
        startButton.configure(fg_color="red", hover_color="red")
    else:
        AFK = False
        startButtonText.set("Irse AFK")
        startButton.configure(fg_color="#1f6aa5", hover_color="#1f6aa5")


#Tkinter
window.geometry("1170x630")
window.title("Anti AFK")
window.configure(bg="#121212")
window.minsize(1170, 620)

#Main Body
leftFrame = CTkFrame(window, corner_radius=0, fg_color="#292929")
rightFrame = CTkFrame(window,corner_radius=0,  fg_color="transparent")
window.columnconfigure(0, minsize=330)
window.columnconfigure(1, weight=1)
window.rowconfigure(0,weight=1)
#packFrames
leftFrame.grid(row=0, column=0, sticky="nsew")
rightFrame.grid(row=0, column=1, sticky="nsew")
leftFrame.propagate(False)


#LeftContent
nameText = CTkLabel(master=leftFrame, text="AntiAFK", font=("Segoe UI", 30))
modesFrame =CTkFrame(master=leftFrame, fg_color="transparent")
selectText= CTkLabel(master=modesFrame, text="Select a mode", font=("Segoe UI", 22))
wasdButton = CTkButton(master=modesFrame, text="Movement", command= lambda: (set_mode("wasd"), show_frame(wasd_frame)), height=30, width=330, font=("Segoe UI", 22))
mouseButton = CTkButton(master=modesFrame, text="Clicker", command= lambda: (set_mode("mouseClick"), show_frame(clicker_frame)), height=30, width=330, font=("Segoe UI", 22)) 
singlekButton = CTkButton(master=modesFrame, text="Single Key", command= lambda: (set_mode("singleKey"), show_frame(singlekey_frame)), height=30, width=330, font=("Segoe UI", 22))
minimalMoveButton = CTkButton(master=modesFrame, text="Minimal Movement", command= lambda: (set_mode("minimalMovement"), show_frame(minimal_frame)), height=30, width=330, font=("Segoe UI", 22))

startButton = CTkButton(master=leftFrame, textvariable=startButtonText, command=irseAFK, height=45, width=330, fg_color= "#1f6aa5", hover_color="#1f6aa5",font=("Segoe UI", 22))

#rightContent
wasd_frame = CTkFrame(rightFrame, fg_color= "transparent")
clicker_frame = CTkFrame(rightFrame, fg_color= "transparent")
singlekey_frame = CTkFrame(rightFrame, fg_color= "transparent")
minimal_frame = CTkFrame(rightFrame, fg_color= "transparent")

for frame in (wasd_frame,clicker_frame,singlekey_frame,minimal_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# - PREFABS -
def create_option_frame(master, title_text, entry1PHText, entry2PHText, width=400, height=300):
    frame = CTkFrame(
        master=master,
        corner_radius=14,
        width=width,
        height=height,
        fg_color="#292929"    
    )
    frame.pack_propagate(False)
    title = CTkLabel(
        master=frame,
        text=title_text,
        font=("Segoe UI", 22)
    )
    title.pack(pady=(10,20))

    entry1 = CTkEntry(master=frame, placeholder_text= entry1PHText, corner_radius=25, text_color="#EC8B0D",placeholder_text_color="#717171", fg_color="#121212",border_color="#121212", width= 255, height= 37, font=("Segoe UI", 13))
    entry2 = CTkEntry(master=frame, placeholder_text= entry2PHText, corner_radius=25, text_color="#EC8B0D",placeholder_text_color="#717171", fg_color="#121212",border_color="#121212", width= 255, height= 37, font=("Segoe UI", 13))

    entry1.pack(pady=5)
    entry2.pack(pady=5)

    return frame, entry1, entry2

def create_slider_frame(master, title_text, width=400, height=300):
    frame =CTkFrame(
        master=master,
        corner_radius=14,
        width=width,
        height=height,
        fg_color="#292929"    
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
        command=on_slider_change
    )
    slider.set(10)
    slider.pack(pady=10)

    return frame, slider, sliderValue

# - WASD frames -
wasdDelayFrame, wasdDelayMin, wasdDelayMax = create_option_frame(
    master=wasd_frame, 
    title_text="Tiempo entre teclas", 
    entry1PHText=f"Delay mínimo — por defecto {MIN_DELAY:.2f}s", 
    entry2PHText=f"Delay máximo — por defecto {MAX_DELAY:.2f}s")

wasdHoldFrame, wasdHoldMin, wasdHoldMax = create_option_frame(
    master=wasd_frame,
    title_text="Tiempo de pulsación", 
    entry1PHText=f"Hold mínimo — por defecto {MIN_HOLD:.2f}s", 
    entry2PHText=f"Hold máximo — por defecto {MAX_HOLD:.2f}s")



# - CLICKER frames -
mouseClickFrame, mouseClickRate, sliderValue = create_slider_frame(
    master=clicker_frame,
    title_text="Click Rate"
)
# pack all option frames
wasdDelayFrame.grid(row=0, column=0, padx=10, pady=10)
wasdHoldFrame.grid(row=0, column=1, padx=10, pady=10)
mouseClickFrame.grid(row=0, column=1, padx=10, pady=10)





#Pack general things
nameText.pack(side=TOP, pady=7, padx=7)
startButton.pack(side=BOTTOM, pady=7,padx=5)
selectText.pack(pady=3)
modesFrame.pack(pady=50,padx=5)
wasdButton.pack(pady=6)
mouseButton.pack(pady=6)
singlekButton.pack(pady=6)
minimalMoveButton.pack(pady=6)

show_frame(wasd_frame) #Para que la primera TAB que aparezca sea la de WASD
update_mode_buttons() #Para que aparezca seleccionado el WASD al abrir el programa
threading.Thread(target=afk_loop, daemon=True).start() #Para que funcione todo junto, no se como funciona
window.mainloop()