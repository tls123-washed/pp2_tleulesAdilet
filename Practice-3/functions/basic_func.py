def my_function():
  print("Hello from a function")

my_function()


#farenheit to celsius function
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77)) #25.0
print(fahrenheit_to_celsius(95)) #35.0
print(fahrenheit_to_celsius(50)) #10.0


'''
Functions can send data back to the code that called them using the return statement.

When a function reaches a return statement, it stops executing and sends the result back:
'''
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#We can return value directly
def get_greeting():
  return "Hello from a function"

print(get_greeting())


#If a function doesn't have a return statement, it returns None by default.
'''
Function definitions cannot be empty.
If you need to create a function placeholder without any code, use the pass statement:'''
def my_function1():
  pass