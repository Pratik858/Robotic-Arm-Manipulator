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


print(T04.col(-1))

A = sp.diff(T04.col(-1),t3)
print(A)



#Newton Raphson Method
#thetha(i+1) = thetha(i) - j-1(thetha)*f(thetha)n

t1, t2, t3 = (0.1, 0.1, 0.1)

p1 = [np.sin(t1)*np.sin(t3) + np.cos(t1)*np.cos(t2)*np.cos(t3) + np.cos(t1)*np.cos(t2) + np.cos(t1)]
p2 = [np.sin(t1)*np.cos(t2)*np.cos(t3) + np.sin(t1)*np.cos(t2) + np.sin(t1) - np.sin(t3)*np.cos(t1)]
p3 = [np.sin(t2)*np.cos(t3) + np.sin(t2)]

qo = sp.Matrix([0.1, 0.1, 0.1])
print(p1)
print(p2)
print(p3)

def func(dest_x, dest_y, dest_z):
  q1 =np.subtract(p1, dest_x)
  q2 =np.subtract(p2, dest_y)
  q3 =np.subtract(p3, dest_z)
  p = np.matrix([q1, q2, q3])
  return p

b = func(2, 1, 1)
#print(b)

def CalcJacobian(t1, t2, t3):
  Jacobian = np.matrix([[(np.cos(t1)*np.sin(t3) - np.sin(t1)*np.cos(t2)*np.cos(t3) - np.sin(t1)*np.cos(t2) - np.sin(t1)),      ((-1)*np.cos(t1)*np.sin(t2)*np.cos(t3) - np.cos(t1)*np.sin(t2)),    (np.sin(t1)*np.cos(t3) - np.cos(t1)*np.cos(t2)*np.sin(t3))],
                       [(np.cos(t1)*np.cos(t2)*np.cos(t3) + np.cos(t1)*np.cos(t2) + np.cos(t1) + np.sin(t3)*np.sin(t1)),       ((-1)*np.sin(t1)*np.sin(t2)*np.cos(t3) - np.sin(t1)*np.sin(t2)),    ((-1)*np.sin(t1)*np.cos(t2)*np.sin(t3) - np.cos(t3)*np.cos(t1))],
                       [0,                                                                                                     (np.cos(t2)*np.cos(t3) + np.cos(t2)),                               (-1)*np.sin(t2)*np.sin(t3)],
                       ])
  return Jacobian


#print(CalcJacobian(t1, t2, t3))
a = np.linalg.inv(CalcJacobian(0.1, 0.1, 0.1))
#print(a)
#print(b)

c = a*b
#c = a@b
print(c)

q = np.subtract(qo, c)
#print(q)

 t1 , t2, t3 = q[0,0],q[1,0],q[2,0]

 p1 = [np.sin(t1) * np.sin(t3) + np.cos(t1) * np.cos(t2)*np.cos(t3) + np.cos(t1)*np.cos(t2) + np.cos(t1)]
 p2 = [np.sin(t1)*np.cos(t2)*np.cos(t3) + np.sin(t1)*np.cos(t2) + np.sin(t1) - np.sin(t3)*np.cos(t1)]
 p3 = [np.sin(t2)*np.cos(t3) + np.sin(t2)]


 print(p1[0] - dest_x)
 print(p2[0] - dest_y)
 print(p3[0] - dest_z)
 
 t1, t2, t3 = 0.1, 0.1, 0.1
q = np.matrix([[t1],[t2],[t3]])

dest = [2, 1, 1]
def isreach(q):
  t1 , t2, t3 = q[0,0],q[1,0],q[2,0]
  p1 = [np.sin(t1)*np.sin(t3) + np.cos(t1)*np.cos(t2)*np.cos(t3) + np.cos(t1)*np.cos(t2) + np.cos(t1)]
  p2 = [np.sin(t1)*np.cos(t2)*np.cos(t3) + np.sin(t1)*np.cos(t2) + np.sin(t1) - np.sin(t3)*np.cos(t1)]
  p3 = [np.sin(t2)*np.cos(t3) + np.sin(t2)]

  x = p1[0] - dest[0]
  y = p2[0] - dest[1]
  z = p3[0] - dest[2]
  nochi = 10**(-6)
  print('hi')
  return np.absolute(x)>nochi or  np.absolute(y)>nochi  or   np.absolute(z)>nochi
#  print(p1[0] - dest_x)
# print(p2[0] - dest_y)
# print(p3[0] - dest_z)

#record = q

#while isreach(q):

for i in range(1000):
  #print('nochi')
  Jaco = np.linalg.inv(CalcJacobian(q[0,0],q[1,0],q[2,0]))
  fun1 = func(dest[0], dest[1], dest[2])
  c = Jaco @ fun1
  q = np.subtract(q, c)
  
  
t1 , t2, t3 = q[0,0],q[1,0],q[2,0]
p1 = [np.sin(t1)*np.sin(t3) + np.cos(t1)*np.cos(t2)*np.cos(t3) + np.cos(t1)*np.cos(t2) + np.cos(t1)]
p2 = [np.sin(t1)*np.cos(t2)*np.cos(t3) + np.sin(t1)*np.cos(t2) + np.sin(t1) - np.sin(t3)*np.cos(t1)]
p3 = [np.sin(t2)*np.cos(t3) + np.sin(t2)]


print(p1[0] )
print(p2[0] )
print(p3[0] )
