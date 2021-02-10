import numpy as np
import sympy as sp
import math as m

dest_x, dest_y, dest_z = (2, 1 , 1)


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
T12 = Transformation.Parameters(1,sp.pi/2,0,t2)
T23 = Transformation.Parameters(1,sp.pi/2,0,t3)
T34 = Transformation.Parameters(1,0,0,0)


#Whole Transformation
T02 = T01*T12 
T03 = T02*T23 
T04 = T03*T34 


position_end_effector = T04[:3,3]
position_joint_3 = T03[:3,3]
position_joint_2 = T02[:3,3]
position_joint_1 = T01[:3,3]

# print(T04.col(-1))

# A = sp.diff(T04.col(-1),t3)


xdes ,ydes,zdes = -2,-1,-1

f1 = T04[0,-1] -xdes
f2 = T04[1,-1] - ydes
f3 = T04[2,-1] - zdes
def inv_jaco(q):
  values = [ (t1,q[0,0]),(t2,q[1,0]),(t3,q[2,0])]
  jacobian = np.matrix([
                      [sp.diff(f1,t1).subs(values) , sp.diff(f1,t2).subs(values) ,sp.diff(f1,t3).subs(values)],
                      [sp.diff(f2,t1).subs(values),sp.diff(f2,t2).subs(values),sp.diff(f2,t3).subs(values)],
                      [sp.diff(f3,t1).subs(values),sp.diff(f3,t2).subs(values),sp.diff(f3,t3).subs(values)]
                    ], dtype='float')
  return np.linalg.inv(jacobian)

def function_value(q):
    values = [ (t1,q[0,0]),(t2,q[1,0]),(t3,q[2,0])]
    func = np.matrix([
                      [f1.subs(values)],
                      [f2.subs(values)],
                      [f3.subs(values)]
    ], dtype = 'float')
    return func


def isreach(q):
  values = [ (t1,q[0,0]),(t2,q[1,0]),(t3,q[2,0])]
  current = [f1.subs(values),f2.subs(values),f3.subs(values)]
  error = pow(10,-6)
  return abs(current[0]) < error and abs(current[1]) < error and abs(current[2]) < error

x_data ,y_data ,z_data = [] , [] ,[]
q = np.matrix([[0.1],[0.1],[1.1]])
i = 0
while not isreach(q) :
    values = [ (t1,q[0,0]),(t2,q[1,0]),(t3,q[2,0])]
    i += 1
    jaco  = inv_jaco(q)
    func = function_value(q)
    q = np.subtract(q , np.dot(jaco,func))
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
# anim.plot_3D_gif("Inv")
