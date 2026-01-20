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
#Mouse click param
clickWaitTime = 15
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

#Logica de los diferentes modos aca
def wasd():
    key = random.choice(wasdKeys)
    hold = random.uniform(MIN_HOLD,MAX_HOLD)  #Este hay que cambiarlo pa que el usuario pueda elegir
    intervalo = random.uniform(MIN_DELAY,MAX_DELAY) #Este lo mismo
    time.sleep(intervalo)
    print (f"Tecla {key} presionada por {hold:.2f} segundos.")
    keyboard.press(key)
    time.sleep(hold)
    keyboard.release(key)
    print(f"Esperando {intervalo:.2f} segundos para el siguiente input...")
    time.sleep(intervalo)
 
def mouse_click():
        mouse = Controller()
        time.sleep(clickWaitTime)
        mouse.click(Button.left,1)
        print("Click hecho")
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

def show_frame(frame):
    frame.tkraise()

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
        print("AFK")
    else:
        AFK = False
        startButtonText.set("Irse AFK")
        startButton.configure(fg_color="#1f6aa5", hover_color="#1f6aa5")
        print("Chau AFK")


#Tkinter
window.geometry("790x600")
window.title("Anti AFK")
window.configure(bg="#121212")
window.minsize(740, 520)

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

frame1 = CTkFrame(master=wasd_frame, corner_radius=14,height=200, width=300, fg_color="#292929")
frame2 = CTkFrame(master=wasd_frame, corner_radius=14, fg_color="#292929")


#Pack
nameText.pack(side=TOP, pady=7, padx=7)
startButton.pack(side=BOTTOM, pady=7,padx=5)
frame1.grid(row=0,column=0, padx=10, pady=10)
frame2.grid(row=0,column=1, padx=10, pady=10)
selectText.pack(pady=3)
modesFrame.pack(pady=50,padx=5)
wasdButton.pack(pady=6)
mouseButton.pack(pady=6)
singlekButton.pack(pady=6)
minimalMoveButton.pack(pady=6)

 
update_mode_buttons() #Para que aparezca seleccionado el WASD al abrir el programa
threading.Thread(target=afk_loop, daemon=True).start() #Para que funcione todo junto, no se como funciona
window.mainloop()