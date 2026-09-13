class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

#len is 0, that means myclass() is 0 too, and that means myobj false too

def myFunction() :
  return True

print(myFunction())


def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")
  
  

#returns true if value fit the data type  
x = 120
print(isinstance(x, int))