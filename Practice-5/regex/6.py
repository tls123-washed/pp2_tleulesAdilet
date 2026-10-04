import re

text = "Python, Java. C++ Python,Java"

result = re.sub(r"[ ,.]", ":", text)
print(result)