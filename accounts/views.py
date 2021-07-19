from django.db.models.fields import EmailField
from accounts.models import CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from .models import CustomUser
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
   # send_mail( 
   # 'Welcome to VBB!',# subject
   # 'Hey,thanks for registering!',# message
   # '',#sender mail address
   # [CustomUser.email,],#recepient list,
   #  fail_silently=False
   #  )
