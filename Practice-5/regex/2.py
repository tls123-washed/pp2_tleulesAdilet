import re

text = "abb abbb ab abbbb ac"

matches = re.findall(r"ab{2,3}", text)
print("Matches:", matches)