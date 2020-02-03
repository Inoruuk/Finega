from os import listdir
import re

def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


if __name__ == "__main__":
    dict = {
        "true" : "1",
        "false" : "0",
    }
    for filename in listdir('8/'):
        with open('8/' + filename, 'r') as file:
            x = multiple_replace(dict, file.read())
            file.close()
        with open('8/' + filename, 'w+') as file:
            file.write(x)
            file.close()