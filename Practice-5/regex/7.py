import re

def snake_to_camel(text):
    return re.sub(r"_([a-zA-Z])", lambda m: m.group(1).upper(), text)

text = "hello_world_python_regex"
print(snake_to_camel(text))