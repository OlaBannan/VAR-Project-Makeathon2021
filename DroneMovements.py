import threading
from djitellopy import tello
import cv2
from time import sleep
imgSaved = None


def getBattery():
    f = open("Battery.txt", "w")
    f.write(str(me.get_battery()))
    f.close()

    f = open("Battery.txt", "r")
    lines = f.readlines()
    print(lines)
    f.close()


me = tello.Tello()

me.connect()
getBattery()


def land():
    me.land()


def takeoff():
    me.takeoff()


def control_drone(action='l', LR=0, FB=0, UD=0, Yaw=0, SLP=2):
    if action == 'l':
        me.send_rc_control(LR // SLP, FB // SLP, UD // SLP, Yaw // SLP)
        sleep(SLP + 1)
    elif action == 'c':
        me.rotate_clockwise(LR)
        sleep(1)
    elif action == 'f':
        me.flip_back()
        sleep(SLP)
    elif action == 'lo':
        sleep(4)
        global imgSaved
        imgSaved = me.get_frame_read().frame  # individual image
        saved = cv2.imwrite("savedImage.jpg", imgSaved)

    else:
        return


def safeLand():
    control_drone('l', 0, 0, 0, 0)
    land()


def imageCapture():
    while True:
        img = me.get_frame_read().frame  # individual image
        cv2.imshow("Image", img)
        cv2.waitKey(1)  # delay shutdown


path = [('l', 0, 0, 20, 0), ('c', 43), ('l', 0, 40, 0, 0), ('lo',), ('l', 0, -40, 0, 0), ('l', 0, 0, -20, 0)]
path2 = [('lo',)]
square_path = [('l', 0, 0, 50, 0), ('c', -90), ('l', 0, 50, 0, 0), ('c', 90), ('l', 0, 50, 0, 0), ('c', 90),
               ('l', 0, 50, 0, 0), ('c', 90), ('l', 0, 50, 0, 0), ('f',), ('l', 0, 0, -50, 0)]

me.streamon()

x = threading.Thread(target=imageCapture, args=())
x.start()

takeoff()
for action in path:
    control_drone(*action)
safeLand()
x.join()



