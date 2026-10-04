import re

text = "hello_world test_case Python_regex bad-case"

matches = re.findall(r"\b[a-z]+_[a-z]+\b", text)
print("Matches:", matches)