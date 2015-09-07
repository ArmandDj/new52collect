from django.contrib import admin
from models import Comic, Character, Review, Owns

# Register your models here.

admin.site.register(Comic)
admin.site.register(Character)
admin.site.register(Review)
admin.site.register(Owns)
