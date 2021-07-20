from django.db.models import query
from django.http import request
from api.models import *
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from datetime import date, datetime, timedelta

def is_librarian(user):
	return (user.is_superuser )

@login_required
def Index(request):
	print("home")
	copies = BookInstance.objects.filter(is_available=False).filter(student=request.user)
	for copy in copies:
		print(copy)
	return render(request, 'home.html',{
		"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
	})

#BOOKS
@login_required
def BookListView(request):
	book_list = Book.objects.all()
	# MODELNAME.objects.all() is used to get all objects i.e. tuples from database
	return render(request, 'frontend/book_list.html', locals())

@login_required
def BookDetailView(request, pk):
	book = get_object_or_404(Book, code=pk)
	copies = BookInstance.objects.filter(book=book).filter(is_available=True)
	copy = BookInstance.objects.filter(is_available=False).filter(student=request.user).filter(book=book)
	if(len(copy)!=0):
		print( request.user ) 
		print( copy )
		return render(request, 'frontend/book_detail.html', {
			"book":book,
			"available_copies": 0,
			"copy":copy[0]
		})	
	return render(request, 'frontend/book_detail.html', {
		"book":book,
		"available_copies": len(copies),
	})

@login_required
@user_passes_test(is_librarian) # add seializer func
def BookCreate(request):
	form = BookForm()
	if request.method == 'POST':
		form = BookForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			#generate book instances
			copies = (form.cleaned_data['instances'])
			print('copies:')
			print(copies)
			book_model = form.save()
			for i in range(int(copies)):
				instance = BookInstance(
				book=book_model,
				due_back=None,
				student=None,
				is_available=True,)
				instance.save()

			return render(request, 'frontend/form.html', {
			"form":BookForm(),
			"success":True,
			"message":str(book_model) + " added"
			})
	
	return render(request, 'frontend/form.html', locals())

@login_required
def BookIssue(request, pk):
	# http://127.0.0.1:8000/app/book/16/issue example url
	print('trying to issue')
	try:
		book_model = Book.objects.get(pk=pk)
	except:
		return render(request, 'frontend/book_list.html',{
			"book_list":Book.objects.all(),
			"error":True,
			"message":"This book doesn't exist!"
		})
	issued = BookInstance.objects.filter(book=book_model).filter(is_available=False).filter(student=request.user) # all issued copies.
	
	if(len(issued)!=0): # cant issue another copy
		print('issued')
		return render(request, 'frontend/book_detail.html',{
			"book":book_model,
			"error":True,
			"message":"You've already issued this book!"
		})

	copies = BookInstance.objects.filter(book=book_model).filter(is_available=True)
	
	if(len(copies)!=0):
		copy = copies[0]
		print(copy)
		copy.is_available = False
		copy.student = request.user
		copy.due_back = datetime.now() + timedelta(days=7)
		copy.save()
		record = History(
				book=book_model,
				instance=copy,
				issuer=request.user,
				issued_on = datetime.now(),
				due_on = copy.due_back,
				returned=False,
			)
		record.save()
		# successfuly issued,
		return render(request, 'home.html',{
			"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
			"success":True,
			"message":"Sucessfuly issued a copy of: " + str(book_model)
		})
	else:# no available copies!
		return render(request, 'frontend/book_detail.html',{
			"book":book_model,
			"error":True,
			"message":"Sorry, no copies of this book are available at the moment! "
		})

@login_required
def BookReturn(request, pk):
	# http://127.0.0.1:8000/app/book/16/retrun example url
	print('tryying to return')
	try:
		book_model = Book.objects.get(pk=pk)
	except:
		return render(request, 'home.html',{
			"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
			"error":True,
			"message":"This book doesn't exist!"
		})
	issued = BookInstance.objects.filter(book=book_model).filter(is_available=False).filter(student=request.user) # all issued copies.
	
	if(len(issued)==0): # havent issued
		print('not issued')
		return render(request, 'home.html',{
			"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
			"error":True,
			"message":"You haven't issued the book you're trying to return!"
		}) # with error msg that not issued

	# if here issued conrains the required book copy.
	copy = issued[0]
	if(copy):
		print(copy)
		try:
			record = History.objects.filter(instance=copy).filter(issuer=request.user).filter(returned=False)[0]
			copy.is_available = True
			copy.student = None
			copy.due_back = None
			copy.save()
			print(record)
		except:
			return render(request, 'home.html',{
						"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
						"error":True,
						"message":"There is no record of you issuing this book!" 
					})
		record.returned_on = datetime.now()
		record.returned = True
		record.save()
		return render(request, 'home.html',{
						"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
						"success":True,
						"message":"Successfully returned: " + str(copy) 
					})
	else:
		return render(request, 'home.html',{
			"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
			"error":True,
			"message":"You haven't issued the book you're trying to return!"
		})

##############################################################################

# authors
@login_required
@user_passes_test(is_librarian) 
def AuthorCreate(request):
	form = AuthorForm()
	if request.method == 'POST':
		form = AuthorForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			#generate book instances
			author = form.save()
		return render(request, 'frontend/form.html', {
			"form":AuthorForm(),
			"success":True,
			"message":str(author) + " added"
		})		
	return render(request, 'frontend/form.html', locals())

##############################################################################

# add student
@login_required
@user_passes_test(is_librarian) 
def StudentCreate(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			#generate book instances
			student = form.save()
		return render(request, 'frontend/form.html', {
			"form":CustomUserCreationForm(),
			"success":True,
			"message":str(student) + " added"
		})		
	return render(request, 'frontend/form.html', locals())

##############################################################################

#NOTICES
@login_required
# form for notice.
def NoticeCreate(request):
	form = NoticeForm()
	print(request.path)
	if request.method == 'POST':
		form = NoticeForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			#generate notice
			notice = form.save()
			print(notice)
			notice.posted_on = datetime.now()
			notice.posted_by = request.user
			if request.user.is_superuser:
				notice.is_approved = True
			notice.save()
			notices = []
			for notice in Notice.objects.all():
				if(notice.is_approved):
					notices.append(notice)
					print(notice)
			return render( request, "frontend/noticeboard.html", {
				"notices":notices,
				"title":"noticeboard",
				"success":True,
				"message":"Notice Submitted successfuly"
			})
	return render(request, 'frontend/form.html', locals())

@login_required
def notice_board(request):
	notices = []
	for notice in Notice.objects.all():
		if(notice.is_approved):
			notices.append(notice)
	return render( request, "frontend/noticeboard.html", {
		"notices":notices,
		"title":"noticeboard"
	})

@login_required
# @user_passes_test(is_librarian)
def approve_notice(request):
	if (not (request.user.is_superuser)):
		# unauthorized accesss
		return render(request, 'frontend/error.html',{
			"tilte":'Unauthorized',
			"auth_error":1,
			"error":1,
			"message":"Not Authorized to access this feature.",
			"redirect": request.path
		})
	# print("authorized")
	
	notices = []
	for notice in Notice.objects.all():
		if(not notice.is_approved):
			notices.append(notice)

	if(request.method == 'POST'):
		try:
			action = request.POST['action']
		except:
			return render( request, "frontend/approvenotice.html", {
			"notices":notices,
			"error":True,
			"message":"No Action specified!",
			"title":"Approve Notices"
		})

		#action is present
		if( (not(action == "approve")) and (not(action == "delete")) ):
			print(action + " : is invalid")
			return render( request, "frontend/approvenotice.html", {
				"notices":notices,
				"error":True,
				"message":"Incorrect Action specified!",
				"title":"Approve Notices"
			})

		#Correct action is present
		to_modify = []
		valid = True
		for field in request.POST:
			# Dev note - need to modify if more form fields are added
			# print(field, request.POST[field])
			if(field=="csrfmiddlewaretoken"):
				continue
			elif(field=="action"):
				continue
			else:
				if(Notice.objects.filter(pk=int(field)).exists()):
					obj = Notice.objects.get(pk=int(field))
					if(obj.is_approved):
						valid = False
						break
					# print(field, obj)
					to_modify.append(obj)
				else:
					valid = False
					break
		if(not to_modify):
			print("invalid")
			valid = False
		if (valid):
			print("valid")
			# update notices here. Data is validated here.
			if(action=="approve"):
				for notice in to_modify:
					notice.is_approved = True
					notice.save()
					print("approved: ")
					print(notice)
			else:
				for notice in to_modify:
					print("yeeting: ")
					print(notice)
					notice.delete()
			notices = []
			for notice in Notice.objects.all():
				if(not notice.is_approved):
					notices.append(notice)
			return render( request, "frontend/approvenotice.html", {
			"notices":notices,
			"success":True,
			"message":"Great Success",
			"title":"Approve Notices"
			})
		else:
			print("invalid")
			return render( request, "frontend/approvenotice.html", {
			"notices":notices,
			"error":True,
			"message":"Incorrect or No Notice IDs selected!",
			"title":"Approve Notices"
			})

	# GET request - return the form.
	return render( request, "frontend/approvenotice.html", {
		"notices":notices,
		"title":"Approve Notices"
	})

##############################################################################

#SEARCH
@login_required
def Search(request):
	try:
		query = request.GET['q']
	except:
		return render(request, 'frontend/book_list.html', {
			"book_list":None,
			"error":True,
			"message":"No serach query provided! "
		})	
	
	# have a search query
	print('query: ' + query)
	
	#search books
	books = Book.objects.filter(bookname__contains=query)
	results=set()
	for book in books:
		results.add(book)
	#search authors
	books = Book.objects.filter(author__first_name__contains=query)
	for book in books:
		results.add(book)
	books = Book.objects.filter(author__last_name__contains=query)
	for book in books:
		results.add(book)

	#search for full name
	# books = Book.objects.all()
	# for book in books:
	# 	if((book.author.full_name()))

	if results:
		return render(request, 'frontend/book_list.html', {
			"book_list":results,
			"success":True,
			"message":"Serach results for the query: " + str(query)
		})	
	else:
		return render(request, 'frontend/book_list.html', {
			"book_list":None,
			"error":True,
			"message":"Sorry, no Serach results for the query: " + str(query)
		})