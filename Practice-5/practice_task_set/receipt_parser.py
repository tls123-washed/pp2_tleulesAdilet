import re

def camel_to_snake(text):
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()

text = "CamelCaseString"
print(camel_to_snake(text))