from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
#from . models import User
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import CreateView, UpdateView, FormView, DetailView, View
from . forms import RegisterForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth

User = get_user_model()

class Register(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
        #return render(request, 'accounts/register.html')

    def post(self, request, *args, **kwargs):
        # GET USER DATA
        # VALIDATE
        # create a user account    
        form = self.form_class(request.POST)    
        user = form.save() #User.objects.create_user(username=username, email=email)
       # user.set_password(password)
        user.is_active = False
        user.save()
        print(user.pk)
        email = user.email
        current_site = get_current_site(request)
        email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

        link = reverse('accounts:activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Activate your account'

        activate_url = 'http://'+current_site.domain+link
        print(activate_url)
        emails = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email]
                    
                )
        emails.send(fail_silently=False)
        messages.success(request, 'Account successfully created')
        return render(request, 'accounts/register.html')

        #return render(request, 'authentication/register.html')


# class Register(FormView):
#     form_class = RegisterForm
#     template_name = 'accounts/register.html'

#     def form_valid(self, form, request, *args, **kwargs):
#         user = form.save()
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(request)
#         email_body = {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 }
#         link = reverse('activate', kwargs={
#                                'uidb64': email_body['uid'], 'token': email_body['token']})

#         email_subject = 'Activate your account'

#         activate_url = 'http://'+current_site.domain+link

#         email = EmailMessage(
#                     email_subject,
#                     'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
#                     'noreply@semycolon.com',
#                     [email],
#                 )
#         email.send(fail_silently=False)
#         messages.success(request, 'Account successfully created')
#         return render(request, 'accounts/register.html')

#        # return HttpResponseRedirect(reverse('accounts:dashboard'))

class VerificationView(View):
    def get(self, request, uidb64, token):
        
        
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            print(id)
            User = get_user_model()

            u = User.objects.get(pk=id)
            print("kkk")

            if not account_activation_token.check_token(u, token):
                return redirect('accounts:login'+'?message='+'User already activated')

            if u.is_active:
                return redirect('accounts:login')
            u.is_active = True
            u.save()

            messages.success(request, 'Account activated successfully')
            return redirect('accounts:login')

        except Exception as ex:
            print("ss")
            pass
            

        return redirect('accounts:login')

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse('<h2> Account Not Active </h2>')

        else:
            print('Someone tried to login failed on our site.')
            return HttpResponse('<h2>Invalid login credentials applied </h2>')

    else:
        return render(request, 'accounts/login.html', {})

#def password_reset_request(request):
#	if(request.method == 'POST'):
#		email = request.POST.get('email')
#	print("HELLHOLE")
#	return render(request,'accounts/password_reset.html',{})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})


class AccountSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'location', 'phone_no', 'profile_image']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Your Account Settings were updated successfully!')
        return reverse('accounts:dashboard')


class Dashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user_object = User.objects.get(pk=request.user.id)
        return render(request, self.template_name, {'object': user_object})










