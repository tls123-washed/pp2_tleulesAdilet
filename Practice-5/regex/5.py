import re

text = "acb a123b axxxb ab a_test_b"

matches = re.findall(r"ab.*b", text)
print("Matches:", matches)