from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from content.models import Comic, Character, Review, Owns
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# homepage
def index(request):
	context = {
	}
	return render(request, 'content/index.html', context)

# default browse page, no category selected
def browse(request):
	context = {
	}
	return render(request, 'content/browse.html', context)

# browse page, category selected
def browse_by(request, browse_by):
	series_list = None
	if browse_by == "series":
		series_list = Comic.objects.all().order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(series=x).order_by('issue_num')), series_list)
	elif browse_by == "character":
		series_list = Character.objects.all().order_by('name').values_list('name', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(characters__name=x).order_by('series')), series_list)
	elif browse_by == "writer":
		series_list = Comic.objects.all().order_by('writer').values_list('writer', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(writer=x).order_by('series')), series_list)
	elif browse_by == "artist":
		series_list = Comic.objects.all().order_by('penciller').values_list('penciller', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(penciller=x).order_by('series')), series_list)
	context = {
		'browse_by': browse_by,
		'series_list': series_list,
	}
	return render(request, 'content/browse.html', context)

# handles search queries
def search(request, search_by):
	if search_by == 'series':
		series_list = Comic.objects.filter(series__icontains=request.POST['content']).order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(series=x).order_by('issue_num')), series_list)
	elif search_by == 'character':
		series_list = Character.objects.filter(name__icontains=request.POST['content']).order_by('name').values_list('name', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(characters__name=x).order_by('series')), series_list)
	elif search_by == 'writer':
		series_list = Comic.objects.filter(writer__icontains=request.POST['content']).order_by('writer').values_list('writer', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(writer=x).order_by('series')), series_list)
	elif search_by == 'artist':
		series_list = Comic.objects.filter(penciller__icontains=request.POST['content']).order_by('penciller').values_list('penciller', flat=True).distinct()
		series_list = map(lambda x:(x, Comic.objects.filter(penciller=x).order_by('series')), series_list)
	context = {
		'browse_by': search_by,
		'series_list': series_list,
	}
	return render(request, 'content/browse.html', context)

# displays information for specific comic book
def comic(request, series, issue):
	comic = Comic.objects.filter(series=series, issue_num=issue)[0]
	reviews = Review.objects.filter(comic_id=comic.id)
	ownership = Owns.objects.filter(user=request.user.username, comic=comic)
	if len(ownership) > 0:
		ownership = ownership[0]
		if ownership.wish:
			ownership = 'wish'
		else:
			ownership = 'owned'
		rating = Owns.objects.get(user=request.user.username, comic=comic).rating
	else:
		ownership = False
		rating = None
	ratings = Owns.objects.filter(comic=comic).values_list('rating', flat=True)
	ratings = [float(rating) for rating in ratings if rating is not None]
	if len(ratings) > 0:
		avg = sum(ratings) / len(ratings)
	else:
		avg = 0.0
	comic.rating = round(avg, 1);
	comic.save()
	context = {
		'comic': comic,
		'characters': comic.characters.all(),
		'review_list': reviews,
		'ownership': ownership,
		'rating': rating,
	}
	return render(request, 'content/comic.html', context)

# handles review submissions
def review(request, series, issue, id):
	if id == '-1':
		comic = Comic.objects.get(series=series, issue_num=issue)
		author = request.user.username
		review = Review(comic=comic, author=author, content=request.POST['content'], date=datetime.date.today())
		review.save()
		return HttpResponseRedirect(reverse('content:comic', args=(series, issue,)))
	else:
		review = Review.objects.get(id = id)
		review.delete();
		return HttpResponseRedirect(reverse('content:comic', args=(series, issue,)))

# login page
def login_view(request, error = 0, message = 0):
	context = {
		'error': error,
		'message': message,
	}
	return render(request, 'content/login.html', context)

# registration page
def register(request, error = 0):
	context = {
		'error': error,
	}
	return render(request, 'content/register.html', context)

# handles account operations (login, register, logout)
def account_request(request, type):
	if type == 'logout':
		logout(request)
		return HttpResponseRedirect(reverse('content:login', args=(0, 2,)))

	username = request.POST['username']
	password = request.POST['password']
	
	if type == 'login':
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if('content/login' in request.META.get('HTTP_REFERER')):
					return HttpResponseRedirect("/content")
				else:
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		return HttpResponseRedirect(reverse('content:login', args=(1, 0,)))
	elif type == 'register':
		user = User.objects.filter(username=username);
		if len(user) > 0:
			return HttpResponseRedirect(reverse('content:register', args=(1,)))
		elif password != request.POST['confirm']:
			return HttpResponseRedirect(reverse('content:register', args=(2,)))
		else:
			user = User.objects.create_user(username=username, password=password)
			user.save()
			return HttpResponseRedirect(reverse('content:login', args=(0, 1,)))

# handles changes in ownership status
def ownership(request, series, issue, action):
	comic = Comic.objects.get(series=series, issue_num=issue)
	ownership = Owns.objects.filter(user=request.user.username, comic=comic)
	if len(ownership) > 0:
		ownership = ownership[0]
		if action == 'add' and ownership.wish == True:
			ownership.wish = False
			ownership.save()
		elif action == 'remove':
			ownership.delete()
		elif action == 'toggleread':
			ownership.read = not ownership.read
			ownership.save()
		elif action == 'readingadd':
			ownership.priority = len(Owns.objects.filter(user=request.user.username, wish=False, read=False, priority__isnull=False)) + 1
			ownership.save()
		elif action == 'readingremove':
			next_items = Owns.objects.filter(priority__gt=ownership.priority)
			for item in next_items:
				item.priority -= 1
				item.save()
			ownership.priority = None
			ownership.save()
		elif action == 'readingtoggleread':
			next_items = Owns.objects.filter(priority__gt=ownership.priority)
			for item in next_items:
				item.priority -= 1
				item.save()
			ownership.read = not ownership.read
			ownership.priority = None
			ownership.save()
		elif action == 'incrementpriority':
			next_item = Owns.objects.get(priority=ownership.priority + 1)
			next_item.priority -= 1
			ownership.priority += 1
			next_item.save()
			ownership.save()
		elif action == 'decrementpriority':
			prev_item = Owns.objects.get(priority=ownership.priority - 1)
			prev_item.priority += 1
			ownership.priority -= 1
			prev_item.save()
			ownership.save()
	else:
		if action == 'add':
			add = Owns(user=request.user.username, comic=comic, wish=False)
		elif action == 'wish':
			add = Owns(user=request.user.username, comic=comic, wish=True)
		add.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# collection page
def collection(request):
	collection = Owns.objects.filter(user=request.user.username, wish=False)
	collection = map(lambda x:x.comic.id, collection)
	series_list = Comic.objects.filter(id__in=collection).order_by('series').values_list('series', flat=True).distinct()
	series_list = map(lambda x:[x, Comic.objects.filter(series=x, id__in=collection).order_by('issue_num')], series_list)
	for series in series_list:
		series[1] = map(lambda x:[x, Owns.objects.get(user=request.user.username, comic=x).read, Owns.objects.get(user=request.user.username, comic=x).priority], series[1])
	context = {
		'series_list': series_list
	}
	return render(request, 'content/collection.html', context)

# other lists is collection page (e.g. wishlist)
def collection_other(request, listing):
	series_list = None
	if listing == "wishlist":
		collection = Owns.objects.filter(user=request.user.username, wish=True)
		collection = map(lambda x:x.comic.id, collection)
		series_list = Comic.objects.filter(id__in=collection).order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:[x, Comic.objects.filter(series=x, id__in=collection).order_by('issue_num')], series_list)
		read = False
	elif listing == "incomplete":
		collection = Owns.objects.filter(user=request.user.username, wish=False)
		collection = map(lambda x:x.comic.id, collection)
		series_list = Comic.objects.filter(id__in=collection).order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:[x, Comic.objects.filter(series=x).exclude(id__in=collection).order_by('issue_num')], series_list)
		read = False
	elif listing == "read":
		collection = Owns.objects.filter(user=request.user.username, read=True)
		collection = map(lambda x:x.comic.id, collection)
		series_list = Comic.objects.filter(id__in=collection).order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:[x, Comic.objects.filter(series=x, id__in=collection).order_by('issue_num')], series_list)
		read = True
	elif listing == "unread":
		collection = Owns.objects.filter(user=request.user.username, read=False)
		collection = map(lambda x:x.comic.id, collection)
		series_list = Comic.objects.filter(id__in=collection).order_by('series').values_list('series', flat=True).distinct()
		series_list = map(lambda x:[x, Comic.objects.filter(series=x, id__in=collection).order_by('issue_num')], series_list)
		read = False
	for series in series_list:
		series[1] = map(lambda x:[x, read, Owns.objects.get(user=request.user.username, comic=x).priority], series[1])
	context = {
		'listing': listing,
		'series_list': series_list,
	}
	return render(request, 'content/collection.html', context)

# handles rating
def rating(request, series, issue):
	rating = request.POST['rating']
	comic = Comic.objects.get(series=series, issue_num=issue)
	data = Owns.objects.get(user=request.user.username, comic=comic)
	data.rating = rating
	data.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# reading list page
def reading(request):
	reading_list = Owns.objects.filter(user=request.user.username, wish=False, read=False, priority__isnull=False).order_by('priority')
	reading_list = map(lambda x:x.comic, reading_list)
	context = {
		'reading_list': reading_list,
		'length': len(reading_list),
	}
	return render(request, 'content/reading.html', context)