from django.shortcuts import redirect, render
from django.views import View
from .models import Friend
from django.contrib.auth.models import User
from accounts.models import UserProfile
from posts.models import Post

class Profile(View):

    def getUserProfile(self, user):
        myUser=  UserProfile.objects.get(user= user.id)
        return myUser

    def get(self, request, user):
        myUser= self.request.user
        myUserInfo= self.getUserProfile(myUser)
        myFriends= Friend.friendList(myUser)
        theUser= User.objects.get(username= user)
        theUserProfile= self.getUserProfile(theUser)
        userFriends=  Friend.friendList(theUser)
        userFriendReq=  Friend.friendRequestsList(myUser)
        sentUserFriendReq=  Friend.sentFriendRequests(myUser)
        userPosts= list(Post.allUserPosts(theUser))
        content={
            'userProfile':myUserInfo,
            'profileInfo':theUserProfile,
            'myFriendList':myFriends,
            'userFriendList':userFriends,
            'friendRequests':userFriendReq,
            'sentFriendRequests':sentUserFriendReq,
            'allPosts':userPosts
            }
        return render(request, 'profile.html',content )

    def post(self, request, user):
        myUser= self.request.user
        enteredPass= request.POST.get('userPassword')
        if myUser.check_password(enteredPass):
            myUserInfo= self.getUserProfile(myUser)

            myUserInfo.f_name= request.POST.get('f_name')
            myUserInfo.l_name= request.POST.get('l_name')
            myUserInfo.fullName= myUserInfo.f_name +" "+ myUserInfo.l_name

            myUserInfo.email= request.POST.get('email')
            myUserInfo.gender= request.POST.get('gender')

            myUserInfo.save()
        return redirect ("userProfile:Profile", myUser)
    
class FriendsCTRL(View):

    def post(self, request, user):
        method= request.POST.get("_method")
        if method == "add":          
            myuser1=  User.objects.get(username= self.request.user)
            myuser2=  User.objects.get(username= user)
            if request.POST.get('status') == 'B':
                Newfriends= Friend() 
                Newfriends.user1= myuser1
                Newfriends.user2= myuser2
                Newfriends.status= 'B'
                Newfriends.save()
            if request.POST.get('status') == 'F':
                Newfriends= Friend.objects.filter(user2=myuser1, user1=myuser2).update(status='F')
        elif method == "delete":
            myuser1=  self.request.user
            myuser2=  User.objects.get(username= user)
            friendShip= (Friend.objects.filter(user1=myuser1, user2=myuser2)) | (Friend.objects.filter(user1=myuser2 ,user2=myuser1))
            friendShip.delete()
        if request.POST.get('next'):
            return redirect (request.POST.get('next'))
        return redirect ("userProfile:Profile", user)

