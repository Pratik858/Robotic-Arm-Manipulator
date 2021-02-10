import numpy as np 
import sympy as sp 
import matplotlib.pyplot as plt 

class Transformation():
    def Parameters(a,alpha,d,t):
        Trans = sp.Matrix([ [ sp.cos(t)              , -1*sp.sin(t)         ,      0           ,    a              ],
                        [ sp.sin(t)*sp.cos(alpha) , sp.cos(t)*sp.cos(alpha) , -1*sp.sin(alpha) , -1*sp.sin(alpha)*d ],
                        [ sp.sin(t)*sp.sin(alpha) , sp.cos(t)*sp.sin(alpha) ,    sp.cos(alpha) ,    sp.cos(alpha)*d ],
                        [ 0                       , 0                       ,    0             ,  1              ],
                          ])
        return Trans 
    
    
#Length of links is 1 
#Angle thetha
t1 = sp.Symbol('t1')
t2 = sp.Symbol('t2')
t3 = sp.Symbol('t3')


#Transformations
T01 = Transformation.Parameters(0,0,0,t1)
T02 = Transformation.Parameters(1,sp.pi/2,0,t2)
T03 = Transformation.Parameters(1,sp.pi/2,0,-1*t3)
T04 = Transformation.Parameters(1,0,0,0)


#Whole Transformation
T02 = T01*T02 
T03 = T02*T03 
T04 = T03*T04 

# calculating the positions of endeffector and joint
position_end_effector = T04[:3,3]
position_joint_3 = T03[:3,3]
position_joint_2 = T02[:3,3]
position_joint_1 = T01[:3,3]

#for animation
x_data ,y_data ,z_data = [] , [] ,[]
values = { t1:0,t2:0,t3:0 }
destination = [sp.pi/2 , sp.pi/2 , sp.pi/2 ]
i = 0
for j in range(3):
    i = 0
    while(i < destination[j]):
        if j ==0 :
            values[t1] = i
        elif j ==1 :
            values[t2] = i
        else :
            values[t3] = i
        i += 0.1
        x3 = position_end_effector.subs(values)[0]
        y3 = position_end_effector.subs(values)[1]
        z3 = position_end_effector.subs(values)[2]
        x2 = position_joint_3.subs(values)[0]
        y2 = position_joint_3.subs(values)[1]
        z2 = position_joint_3.subs(values)[2]
        x1 = position_joint_2.subs(values)[0]
        y1 = position_joint_2.subs(values)[1]
        z1 = position_joint_2.subs(values)[2]
        x_data.append([x1,x2,x3])
        y_data.append([y1,y2,y3])
        z_data.append([z1,z2,z3])
    


from ploting import animation
anim = animation(x_data, y_data, z_data)
anim.plot_3D()
anim.plot_3D_gif()
