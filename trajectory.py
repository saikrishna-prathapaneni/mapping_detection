from serial.tools import list_ports
from math import sqrt
from pydobot import Dobot


                    
  # z locations of the object
z= {0:'',1:'',2:'',3:'',4:''}

bin_location = ( (0,0),(0,0))     # location of bins

port = list_ports.comports()[0].device
device = Dobot(port=port, verbose=True)     #Establish Connection with the bot

print(device._get_arm_orientation())   #AA AA:3:50:0:00:206 here 00 means Left and 01:205 means right
#device._set_arm_orientation('L')     #L is left and R is right arm orientation


device.speed(8000,5000)     #Set overall movement speed of the bot. Highest values for both 10000

def trej(obj_coord):
    obj_coord = obj_coord.sort(key=lambda x:x[1])
    for obj in obj_coord:
        obj_class=obj[0]
        obj_x = obj[1]
        obj_y = obj[2]
        obj_z=z[obj_class]


        if obj_class==0:
            device._set_arm_orientation('L')
            device.grip(1)      #Turn ON air pump
            device.suck(0)      # 0 for sucking in air, 1 for blowing out air

                                 #device.move_to(159.7595, 14.5572, 233.5419, 71.5233, wait=True)     #decent initial position, move_to() uses shortest time path
            device.move_to_jump(obj_x, obj_y, obj_z, -24.8673, wait= True)  #parameters: x, y, z, r
                                 #device._set_ptp_jump_params(20.0000, 200.000) #change these params to change height and limit values of jump. These are defalt values
            device.move_to_jump(bin_location[0][0], bin_location[0][1], bin_location[0][2], 128.9536, wait=True)

            device.grip(0)      #Turn OFF air pump
        
        elif obj_class==2:
            device._set_arm_orientation('R')
            device.grip(1)     
            device.suck(0)      

                                
            device.move_to_jump(obj_x, obj_y, obj_z, -24.8673, wait= True)  
                                
            device.move_to_jump(bin_location[1][0], bin_location[1][1], bin_location[1][2], 128.9536, wait=True)

            device.grip(0)
        else:
            pass


    device.close()


def find_distance(initial_Coord,final_coord):
    
    return (sqrt((intial_coord[0]-final_coord[0])**2 + (intial_coord[1]-final_coord[1])**2
                       + (intial_coord[2]-final_coord[2]**2)))
