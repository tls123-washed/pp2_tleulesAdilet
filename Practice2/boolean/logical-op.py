"""
Logical operators are used to combine conditional statements. Python has three logical operators:

and - Returns True if both statements are true
or - Returns True if one of the statements is true
not - Reverses the result, returns False if the result is true
"""
#and is used when we need both our conditions be true
#Test if a is greater than b, AND if c is greater than a:
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")
  
  
#Test if a is greater than b, OR if a is greater than c:
#or uses whe youneed at least one correct value
a = 200
b = 33
c = 500
if a > b or a > c:
  print("At least one of the conditions is True")
  

#Test if a is NOT greater than b:
a = 33
b = 200
if not a > b:
  print("a is NOT greater than b")
  
  
#Combined
age = 25
is_student = False
has_discount_code = True

if (age < 18 or age > 65) and not is_student or has_discount_code:
  print("Discount applies!")



'''
When combining multiple logical operators, use parentheses
to make your intentions clear and control the order of evaluation.
'''
temperature = 25
is_raining = False
is_weekend = True

if (temperature > 20 and not is_raining) or is_weekend:
    print("Great day to go out")



#User authentication check:

username = "Tobias"
password = "secret123"
is_verified = True

if username and password and is_verified:
  print("Login successful")
else:
  print("Login failed")
  
  
#Range checking with logical operators:

score = 85

if score >= 0 and score <= 100:
  print("Valid score")
else:
  print("Invalid score")