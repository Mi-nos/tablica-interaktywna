import pyautogui
import time
from pynput import mouse
import multiprocessing
import keyboard
import os

total_time = 0.0
max_time = 10.0

shared_float = total_time

# Funkcja procesu potomnego
def child_process(shared_float):
    """
    for i in range(5):
        with shared_float.get_lock():  # Użyj wbudowanej blokady
            shared_float.value += 1.5
        time.sleep(0.5)
    """
    if keyboard.read_key():
            print("A keyboard key has been pressed")
            total_time = 0.0
            shared_float = 0.0

def monitor_float(shared_float):
    while True:
        print("Aktualna wartość:", shared_float.value)
        time.sleep(0.1)

#pid = os.fork()

if __name__ == "__main__":
    #shared_float = multiprocessing.Value('d', 0.0)

    """
    while(True):
        ########################################################################################
        ##MOUSE MOVEMENT CAPTURE################################################################
        ########################################################################################
        start = time.time()
        # Get the initial position of the mouse
        initial_position = pyautogui.position()

        # Wait for a short period
        time.sleep(0.01)

        # Get the new position of the mouse
        new_position = pyautogui.position()

        # Calculate the movement
        movement = (new_position.x - initial_position.x, new_position.y - initial_position.y)
        #print(movement)
        end = time.time()
        mouse_elapsed_time = end - start
        #print(mouse_elapsed_time)
        if(movement == (0,0)):
            total_time += mouse_elapsed_time
        else:
            total_time = 0.0
        print(total_time)

        if(total_time >= max_time):
            print(f"Brak aktywnosci przez {total_time} sekund.")
            print(f"Maksymalny dopuszczalny czas nieaktywnosci: {max_time} sekund.")
            exit(0)
    """

    #wersja z plikiem tekstowym - wip
    while(True):
        #################
        f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\config.txt', "r")
        line = f.readline()
        line2 = f.readline().strip()
        f.close()
        #print('line:')
        #print(line)
        #print('line2:')
        #print(line2)
        max_time = float(line2)
        #max_time = 25

        #################

        ########################################################################################
        ##MOUSE MOVEMENT CAPTURE################################################################
        ########################################################################################
        start = time.time()
        # Get the initial position of the mouse
        initial_position = pyautogui.position()

        # Wait for a short period
        time.sleep(0.01)

        # Get the new position of the mouse
        new_position = pyautogui.position()

        # Calculate the movement
        movement = (new_position.x - initial_position.x, new_position.y - initial_position.y)
        #print(movement)
        end = time.time()
        mouse_elapsed_time = end - start
        #print(mouse_elapsed_time)
        if(movement == (0,0)):
            total_time += mouse_elapsed_time
        else:
            total_time = 0.0
        print(total_time)

        f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\inactivity_time.txt', "w")
        f.write(str(total_time))
        f.close()

        #if(total_time >= max_time):
        if(total_time >= max_time):
            print(f"Brak aktywnosci przez {total_time} sekund.")
            print(f"Maksymalny dopuszczalny czas nieaktywnosci: {max_time} sekund.")
            #exit(0)
            total_time = 0.0
            os.system('python C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\ScreenSaverPlayVideo.py')

            #time.sleep(20)