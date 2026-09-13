"""
if statements cannot be empty,
but if you for some reason have an if statement with no content,
put in the pass statement to avoid getting an error.
    """
    
a = 33
b = 200

if b > a:
  pass

#The pass statement is a null operation - nothing happens when it executes. 
# It serves as a placeholder.


#Placeholder for future implementation:

age = 20

if age < 18:
  pass # TODO: Add underage logic later
else:
  print("Access granted")
  
  
"""
This will cause an error (empty code block):

score = 85

if score > 90:
  # This is excellent
# This will raise an IndentationError
"""


#This works correctly with pass:

score = 85

if score > 90:
  pass # This is excellent
print("Score processed")


#Using pass in different branches:

value = 50

if value < 0:
  print("Negative value")
elif value == 0:
  pass # Zero case - no action needed
else:
  print("Positive value")
  
  
#Using pass with functions:

def calculate_discount(price):
  pass # TODO: Implement discount logic

# Function exists but doesn't do anything yet