from django.http import request
from api.models import Notice
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_librarian(user):
    return (user.is_superuser )

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
			"error_message":"Not Authorized to access this feature.",
			"redirect": "/app/approvenotice"
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