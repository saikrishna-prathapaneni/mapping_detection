from detect import get_image_coordinates
from mapping import robot_map
from trajectory import trej

import cv2
import os
import time


def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )



def capture_image():
    cam = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)


    img_counter = 0
   
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
        # ESC pressed
             print("Escape hit, closing...")
             break
        elif k%256 == 32:
        # SPACE pressed
            img_name = "data/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()






def main():
    ''' 
    main code executes capaturing of a image, mapping and trajectory

    
    '''

    path='./images_1/'
    capture_image()
    
    coord = get_image_coordinates(path+os.listdir('./images_1')[0])
    os.remove(path+os.listdir('./images_1')[0])
    while(True):    # wait till the rectangle is under workspace of the robot
        if str(input("enter 'r' to continue to the execution of the robot..."))=='r':

            break

    final_locations = robot_map(coord)  # get locations of the objects in robot perspective
    trej(final_locations)
    print('task done')

   
if __name__=='__main__':
    main()