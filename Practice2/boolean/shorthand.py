#One-line if statement:
a = 5
b = 2
if a > b: print("a is greater than b")


#One-line if/else that prints a value:
a = 2
b = 330
print("A") if a > b else print("B")


#You can also use a one-line 
#if/else to choose a value and assign it to a variable:
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)


#You can chain conditional expressions, 
#but keep it short so it stays readable:
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")


#Ternary operators are particularly useful for 
#simple assignments and return statements.
#max value between two values
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)


#Setting a default value:
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)

