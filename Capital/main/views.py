from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from .models import *
from django.views import generic
from django.urls import reverse_lazy
from django.forms.utils import ErrorList
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.http import HttpResponse

# Create your views here.

#API

class WelcomeView(TemplateView):
    template_name = 'indexa.html'

class About(TemplateView):
    template_name = 'About.html'
 
class History(TemplateView):
    template_name = 'History.html'

class Ourteam(TemplateView):
    template_name = 'Ourteam.html'
        
class Profile(TemplateView):
    template_name = 'dashboard.html'

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        #print(uid)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')

        return redirect('profile')

    else:
        return HttpResponse('Activation link is invalid!')

class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_messages = 'Please confirm your email address to complete the registration, activation link has been sent to your email, also check your email spam folder'
    
    def abc(self):
        ref = ""
        if "referal" in self.request.session:
            ref = (self.request.session["referal"])

        return ref

    def get_context_data(self, **kwargs):

        context = super(SignUp, self).get_context_data(**kwargs)
        context['referal_user'] = self.abc()

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        username = object.username
        email = object.email
        object.is_active = False
        user = object

        if CustomUser.objects.filter(username__iexact=object.username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This username has been taken'])
            return self.form_invalid(form)

        elif CustomUser.objects.filter(email__iexact=object.email).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This email has been taken'])
            return self.form_invalid(form)
        elif CustomUser.objects.filter(Phone__iexact=object.Phone).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This Phone has been taken'])
            return self.form_invalid(form)
        
        elif object.referer_username:
            if CustomUser.objects.filter(username__iexact=object.referer_username).exists():
                referal_user = CustomUser.objects.get(
                    username__iexact=object.referer_username)

            else:
                object.referer_username = None

        form.save()

        try:

                current_site = get_current_site(self.request)
                mail_subject = 'Activate your Dsubplug account.'
                message =  {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                message = get_template('acc_active_email.html').render(message)
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email] )
                email.content_subtype = "html"
                email.send()

        except:
            pass
        try:
            Referal_list.objects.create(user=referal_user, username=username)
        except:
            pass
        try:

            messages.success( self.request, 'Please confirm your email address to complete the registration,activation link has been sent to your email,, also check your email spam folder')

            send_mail("Welcome to Dsubplug.com", "Welcome to Dsubplug.com ,We offer instant recharge of Airtime, Databundle, CableTV (DStv, GOtv & Startimes), Electricity Bill Payment and Airtime to Cash.", email, username)

        except:
            pass
        try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                "accountReference": create_id(),
                "accountName": username,
                "currencyCode": "USD",
                "customerEmail": email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {}
            }

        except:
            pass
        return super(SignUp, self).form_valid(form)