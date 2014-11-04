import re
 #
inputs = 'Scary Monsters And Nice Sprites(Zedd Remix)'
print(re.search('\(', inputs))
if re.search('\(', inputs) is not None:
    output = re.search
    print(inputs[:re.search('\(', inputs).start()])
else:
    print(inputs)
