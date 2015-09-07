from django.db import models

# Create your models here.

class Character(models.Model):
	name = models.TextField()

	def __unicode__(self):
		return self.name

class Comic(models.Model):
	series = models.TextField()
	issue_num = models.IntegerField()
	title = models.TextField()
	writer = models.TextField()
	penciller = models.TextField()
	cover = models.TextField(null = True)
	rating = models.FloatField()
	characters = models.ManyToManyField(Character)
	cover_price = models.FloatField()

	def __unicode__(self):
		return self.series + " #" + str(self.issue_num)

class Review(models.Model):
	comic = models.ForeignKey(Comic)
	author = models.TextField()
	content = models.TextField()
	date = models.DateField()

class Owns(models.Model):
	user = models.TextField()
	comic = models.ForeignKey(Comic)
	read = models.BooleanField(default = False)
	wish = models.BooleanField(default = False)
	rating = models.IntegerField(null = True)
	priority = models.IntegerField(null = True)