import numpy as np
from scipy.integrate import tplquad

def integrand(x,y,z):
    return x**2 +y**2 + z**2

x_lower, x_upper = 
y_lower, y_upper = 
z_lower, z_upper = 

def x_lower(x,y,z):
    return
def x_upper(x,y,z):
    return
def y_lower(x,y,z):
    return 
def y_upper(x,y,z):
    return
def z_lower(x,y,z):
    return 
def z_upper(x,y,z):
    return

result,error = tplquad(integrand, x_lower, x_upper,
                       lambda x: y_lower, lambda x: y_upper, 
                       lambda x, y: z_lower, lambda x, y: z_upper)

print(f"Result: {result}")
print(f"Error (if exists): {error}")