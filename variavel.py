from pathlib import Path

userPath = str(Path.home()) + '/usuario'

with open('config/filekey.key', 'r') as filekey:
    key = filekey.read()

print(key)
