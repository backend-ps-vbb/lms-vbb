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
		print("here")
		return render(request, 'frontend/error.html',{
			"tilte":'Unauthorized',
			"auth_error":1,
			"error_message":"Not Authorized to access this feature.",
			"redirect": "/app/approvenotice"
		})
	print("authorized")
	return render( request, "frontend/noticeboard.html", {
		"notices":None,
		"title":"Notice editing"
	})