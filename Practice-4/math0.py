import math
import random

#Exercise 1: degree -> radian
degree = float(input("Input degree: "))
radian = math.radians(degree)
print("Output radian:", round(radian, 6))

#Exercise 2: area of a trapezoid
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
print("Expected Output:", (base1 + base2) / 2 * height)

#Exercise 3: area of a regular polygon
sides = int(input("Input number of sides: "))
length = float(input("Input the length of a side: "))
area = sides * length ** 2 / (4 * math.tan(math.pi / sides))
print("The area of the polygon is:", round(area))

#Exercise 4: area of a parallelogram
base = float(input("Length of base: "))
h = float(input("Height of parallelogram: "))
print("Expected Output:", base * h)

