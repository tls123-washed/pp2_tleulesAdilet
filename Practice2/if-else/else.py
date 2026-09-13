a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
  
'''
The else statement provides a default action when none of the previous conditions are true. 
Think of it as a "catch-all" for any scenario not covered by your if and elif statements.
'''

number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")
  
#You can combine if, elif, and else
#to create a comprehensive decision-making structure  
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")
  
  
