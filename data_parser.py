import json
from content.models import Comic, Character
import urllib


with open('crawler/data.json', 'r+') as f:
	Comic.objects.all().delete()
	Character.objects.all().delete()

	data = json.load(f)
	for comic in data:
		c = Comic()
		c.series = comic['series']
		c.issue_num = comic['issue_num']
		c.title = comic['title']
		c.writer = comic['writer']
		c.penciller = comic['penciller']
		c.rating = 0
		c.cover_price = comic['cover_price']

		c.save()

		urllib.urlretrieve('http://comicbookdb.com/' + comic['cover'].replace('thumb', 'large'), 'content/static/images/' + str(c.id) + '.jpg')
		c.cover = str(c.id) + '.jpg'

		for character in comic['characters']:
			char = Character.objects.filter(name=character)
			if len(char) == 0:
				char = Character(name=character)
				char.save()
			else:
				char = char[0]
			c.characters.add(char)

		c.save()