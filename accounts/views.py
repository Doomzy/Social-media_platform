from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm
from .forms import UserProfileForm
from django.contrib.auth import login, logout
from django.views import View

from .models import UserProfile

class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homePage:home')
        return render(request, 'login.html')
    
    def post(self, request):
        loginData= AuthenticationForm(data= request.POST)
        if loginData.is_valid():
            login(request, loginData.get_user())
            return redirect('homePage:home')
        form= AuthenticationForm()
        msg="Wrong login info"
        return render(request, 'login.html', {'form': form, 'msg':msg})

class Signup(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homePage:home')
        return render(request, 'signup.html')

    def post(self, request):
        userForm = UserCreationForm(request.POST)    
        profilForm = UserProfileForm(request.POST, request.FILES)
        if userForm.is_valid():
            myUser=userForm.save(commit=False)
            myForm= profilForm.save(commit=False)
            myForm.fullName= myForm.f_name +" "+ myForm.l_name
            myForm.user= myUser
            if profilForm.is_valid():
                myUser.save()
                myForm.save()
                login(request, myUser)
            return redirect('homePage:home')
        else:
            msg="Wrong login info"
            return render(request, 'signup.html',{'msg':msg})

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('accounts:login')

class UserSearch(View):
    def get(self, request):
        html=[]
        searchKey= request.GET.get('searchKey')
        allProfiles= UserProfile.objects.filter(fullName__icontains=searchKey)
        for p in allProfiles:
            html.append('''
                <div class="row mt-4 m-auto">
                    <img class="smImg col-4" src="'''+p.pfp.url+'''" alt="">
                    <h5 class="col-8" style="place-self: center;">
                    <a class="profileLink" href="/u/'''+p.user.username+'''"> ''' +p.fullName+''' </a>
                    </h5>
                </div>
            ''')
        data={
           'html':html
        }
        return JsonResponse(data)

