import re
import pathlib

def split_by_case(line):
    match = re.match(r'^([A-Z\s/-]+)\s(.+)', line)
    if match:
        capital_words = match.group(1).strip().lower().capitalize()
        rest_of_text = match.group(2).strip()
        if not rest_of_text.endswith("."):
           rest_of_text += "."
        return capital_words, rest_of_text

lines = pathlib.Path("lamarle.txt").read_text().split("\n")

for line in lines:
  try:
     capital_words, rest_of_text = split_by_case(line)
     print(capital_words, ": ", rest_of_text, sep="")
     #print(f"Capital Words: {capital_words}")
     #print(f"Rest of Text: {rest_of_text}")
  except TypeError:
     print("Cannot split:", line)
