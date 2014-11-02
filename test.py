import re

inputs = 'Scary Monsters And Nice Sprites (Zedd Remix)'
output = re.search('\(', inputs)
print(inputs[:re.search('\(', inputs).start()])
