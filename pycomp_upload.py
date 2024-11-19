import os
path = "./img/"
files = [f for f in os.listdir(path)]
for item in files:
    os.system(f'feh "{path}{item}" & python upload.py "{path}{item}"')
