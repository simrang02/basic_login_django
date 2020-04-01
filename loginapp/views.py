from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout,login,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserForm,UserProfileInfoForm

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

@login_required
def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    # user_form = forms.UserForm()
    # profile_form = forms.UserProfileInfoForm()
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return user_login(request)
        else:
            print('Hi')
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'login.html',{'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            HttpResponse("Wrong credentials! Go back!")
    else:
        return render(request, 'index.html')