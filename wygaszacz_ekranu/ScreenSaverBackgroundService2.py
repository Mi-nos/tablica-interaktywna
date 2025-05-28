import keyboard


while True:
    if keyboard.read_key():
        print("A key has been pressed")

        f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\inactivity_time.txt', "w")
        f.write("0.0")
        f.close()
    
        

        #f = open('inactivity_time.txt', "r")
        #print(f.readline())


"""
if keyboard.read_key():
        print("A key has been pressed")
        
        #file = open('inactivity_time.txt', "w")
        #with open('inactivity_time.txt', "a") as f:
        #    f.write("0.0")

        f = open('inactivity_time.txt', "w")
        f.write("0.0")
        f.close()
"""

"""
f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\inactivity_time.txt', "w")
f.write("0.0")
f.close()
"""
