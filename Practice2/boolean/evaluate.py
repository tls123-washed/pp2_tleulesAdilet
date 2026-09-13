print(bool("Hello"))
print(bool(15))


x = "Hello"
y = 15

print(bool(x))
print(bool(y))


bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#all values are true if they contain content


#but if content is equals to zero it will return false
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})