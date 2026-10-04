import re

text = "PythonRegularExpression"

parts = re.split(r"(?=[A-Z])", text)
parts = [part for part in parts if part]

print(parts)