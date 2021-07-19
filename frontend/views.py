from django.http import request
from api.models import *
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from datetime import datetime, timedelta

def is_librarian(user):
	return (user.is_superuser )

@login_required
def Index(request):
	print("home")
	copies = BookInstance.objects.filter(is_available=False).filter(student=request.user)
	for copy in copies:
		print(copy)
	# MODELNAME.objects.all() is used to get all objects i.e. tuples from database
	return render(request, 'home.html',{
		"copies":BookInstance.objects.filter(is_available=False).filter(student=request.user),
	})

@login_required
def BookListView(request):
	book_list = Book.objects.all()
	# MODELNAME.objects.all() is used to get all objects i.e. tuples from database
	return render(request, 'frontend/book_list.html', locals())

@login_required
def BookDetailView(request, pk):
	book = get_object_or_404(Book, code=pk)
	copies=BookInstance.objects.filter(book=book).filter(is_available=True)
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

			return redirect('home')
	
	return render(request, 'frontend/form.html', locals())

@login_required
def BookIssue(request, pk):
	# http://127.0.0.1:8000/app/book/16/issue example url
	print('tryying to issue')
	try:
		book_model = Book.objects.get(pk=pk)
	except:
		return redirect('home') # change this to book detail
	issued = BookInstance.objects.filter(book=book_model).filter(is_available=False).filter(student=request.user) # all issued copies.
	
	if(len(issued)!=0): # cant issue another copy
		print('issued')
		return redirect('home')

	copy = BookInstance.objects.filter(book=book_model).filter(is_available=True)[0]
	
	if(copy):
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
		return redirect('home')
	else:
		return redirect('home')

# authors
@login_required
@user_passes_test(is_librarian) # add seializer func
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