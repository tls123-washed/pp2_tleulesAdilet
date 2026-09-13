print("Hello")
print('Hello') #same

print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = """Lorem ipsum dolor sit amet,blabla
consectetur adipiscing elit, bla
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a, "absolutely no difference")
print(len(a))

a = "Hello, World!"
print(a[1])

for x in "RONALDO SIUUUUU":
    print(x)
    
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")
  
txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")