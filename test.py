from xml.etree import ElementTree as ET

t = ET.parse('lyric.xml')
items = t.getroot()
lyrics = items[9].text

print(lyrics)