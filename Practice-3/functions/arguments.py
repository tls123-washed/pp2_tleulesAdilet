'''
Information can be passed into functions as arguments.

Arguments are specified after the function name, inside the parentheses. 
You can add as many arguments as you want, just separate them with a comma.

The following example has a function with one argument (fname). 
When the function is called, we pass along a first name, 
which is used inside the function to print the full name:
'''
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")


'''
From a function's perspective:

A parameter is the variable listed inside the parentheses in the function definition.

An argument is the actual value that is sent to the function when it is called.
'''
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument


'''
By default, a function must be called with the correct number of arguments.

If your function expects 2 arguments, you must call it with exactly 2 arguments.
'''
#This function expects 2 arguments, and gets 2 arguments::

def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")


'''
You can assign default values to parameters. 
If the function is called without an argument, it uses the default value:
'''
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function() #Hello friend
my_function("Linus")

def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")


#You can send arguments with the key = value syntax.
def my_function21(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function21(animal = "dog", name = "Buddy")

#This way, with keyword arguments, the order of the arguments does not matter.
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")


'''
You can send any data type as an argument to a function (string, number, list, dictionary, etc.).

The data type will be preserved inside the function:
'''
#Sending a list as an argument:
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

#Sending a dictionary as an argument:
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)


#Functions can return values using the return statement:
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

#Functions can return any data type, including lists, tuples, dictionaries, and more.
#A function that returns a list:

def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

#A function that returns a tuple:

def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)


'''
You can specify that a function can have ONLY positional arguments.
To specify positional-only arguments, add , / after the arguments:
'''
def my_function(name, /):
  print("Hello", name)

my_function("Emil")

#To specify that a function can have only keyword arguments, add *, before the arguments:
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil")


'''
You can combine both argument types in the same function.
Arguments before / are positional-only, and arguments after * are keyword-only:
'''
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)