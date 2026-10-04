import re

text = "Hello World Python Regex apple TEST Kazakhstan"

matches = re.findall(r"\b[A-Z][a-z]+\b", text)
print("Matches:", matches)