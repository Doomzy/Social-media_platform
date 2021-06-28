from django.shortcuts import  render
from django.views import View
from posts.forms import PostForm
from posts.models import Post
from userProfile.models import Friend
from accounts.models import UserProfile

class HomePage(View):

    def get(self, requset):
        myUser= self.request.user
        myUserInfo= UserProfile.objects.get(user= myUser.id)
        userFriends=  Friend.friendList(myUser)
        userFriendReq=  Friend.friendRequestsList(myUser)
        friendsId= list()
        try:
            for f in userFriends:
                friendsId.append(f.id)
            allPosts= list(Post.allUserPosts(myUser) | Post.objects.filter(author_id__in=friendsId))
        except:
            allPosts= list(Post.allUserPosts(myUser))
        form= PostForm()
        content={'userProfile':myUserInfo,
        'myFriendList':userFriends,
        'friendRequests':userFriendReq,
        'form':form,
        'allPosts':allPosts
        }
        return render(requset, 'homePage.html', content)

