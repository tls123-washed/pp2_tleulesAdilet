import re

text = "ab abb abbb ac"

matches = re.findall(r"ab*", text)
print("Matches:", matches)