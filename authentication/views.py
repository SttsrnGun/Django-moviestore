from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm


def loginView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('movies:getList'))
        else:
            template = loader.get_template('authentication/login.html')
            form_class = AuthenticationForm
            context = {
                'authenticated_user': request.user,
                'is_authenticated': request.user.is_authenticated,
                'auth_form': form_class,
                'next': request.GET.get('next','/')
            }
            return HttpResponse(template.render(context, request))
        
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            form_class = AuthenticationForm(data=request.POST)

            if form_class.is_valid():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(request.POST.get('next','/'))
                
            template = loader.get_template('authentication/login.html')
            context = {
                'auth_form': form_class,
            }
                
            return HttpResponse(template.render(context, request))

def registerView(request):
    if request.method == 'GET':
    
        form = UserCreationForm()
            
        context ={
            'form': form,
            'next': request.GET.get('next','/'),
        }
        template = loader.get_template('authentication/register.html')
        return HttpResponse(template.render(context, request))
    
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password2']
            user = authenticate(request, username=username, password=password)
            print('user')
            print(user)
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next','/'))
            
        template = loader.get_template('authentication/register.html')
        context ={
            'form': form,
            'next': request.GET.get('next','/'),
        }
            
        return HttpResponse(template.render(context, request))