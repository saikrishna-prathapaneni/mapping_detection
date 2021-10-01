
import numpy as np
import time
import random





# coordinate limits of the robot workspace
x_rob_limit = []
z_rob_limit = [10,235]   
y_rob_limit = []


#scaling and shifting constants of the system
shift_x = 0      
shift_y = 0
shift_z = 0
scale_x = 0
scale_y = 0
scale_z = 0


img_coord=[]
robot_coord=[]
img_transformation=[]





def img_map(img_coord,scale_x=0.23100748849625882,scale_y=0.240651547402833,
             shift_x=-0.0011689153455812127,shift_y=-0.0029223533830359263):
    
    '''
    img_coord is having format:
    list of (classIds[j], (x + w/2, y + h/2), (w, h))

    (classid,(center_coordinates),(width and height) )
    
    
    '''
    obj_data = img_coord
    for ob in obj_data:
        ob.to_list()
        xi=ob[1][0]
        yi=ob[1][1]
        #zi=img_coord[2]

        ob[1][0] = xi*scale_x + shift_x
        ob[1][1] = yi*scale_y + shift_y
        ob.to_tuple()
    return obj_data

def robot_map(img_coord):
    
    robot_coordinates = img_map(img_coord)



    #### robot mapping shall go here  ####




    return robot_coordinates

    





def linear_solve(first_term,second_term,const,no_of_expresults):
    '''
    function solves 1st order linear equations in 2 variables
    in the format of y= mx + c

    parameter description
 
    first term : list of x
    second term : list of coeff of c
    const:list of y
    no_of_expresults:results performed 

    return :
    solutions of linear equations considered in random

    '''
    

    second_term=np.ones(no_of_expresults)
    data_of_results=[]
    if len(first_term) != len(second_term) != no_of_expresults:
        return print("data incorrect")
    
    for i in range(no_of_expresults):

        ran_1 = random.randint(0,no_of_expresults-1)
       

        ran_2 = random.randint(0,no_of_expresults-1)
      
        
        a=np.array([[first_term[ran_1],second_term[ran_1]],[first_term[ran_2],second_term[ran_2]]])
        b=np.array([const[ran_1],const[ran_2]])
        x=np.linalg.solve(a,b)

        data_of_results.append(list(x))
    x_coeff=0
    y_coeff=0

    for i in range(len(data_of_results)):
        x_coeff=x_coeff + data_of_results[i][0]
        y_coeff=y_coeff + data_of_results[i][1] 
    return [x_coeff/len(data_of_results),y_coeff/len(data_of_results)]


def main():
    data_x=[]
    data_y=[]
    while(True):
        try:
            data_x = linear_solve([43.29,930.71,476.18,822.49,43.29] # x solutions are provided 
                                    ,[1,1,1,1,1],[10,215,110,190,10],5)
            break
        except Exception:
            pass


    while(True):
         try:
            data_y = linear_solve([41.56,41.56,207.78,290.89,332.44]  # y solutions are provided
                            ,[1,1,1,1,1],[10,10,50,70,80],5)    
            break
         except Exception:
             pass
    
    print('data in x ',data_x,'data in y ',data_y)    
    



