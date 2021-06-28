from django.shortcuts import redirect
from django.http import JsonResponse
from .forms import PostForm
from.models import *
from accounts.models import UserProfile
from django.views import View


class PostView(View):

    def getPost(self, request):
        postId= request.POST.get('postId')
        myPost= Post.objects.get(id= postId)
        return myPost

    def post(self, request):
        method= request.POST.get('method')
        myUser= request.user
        if method == 'add':
            postForm= PostForm(request.POST, request.FILES)
            postForm.instance.author = UserProfile.objects.get(user=myUser)
            if postForm.is_valid():
                postForm.save()
            if request.POST.get('next'):
                return redirect (next)
        elif method == 'edit':
            myPost= self.getPost(request)
            thepost= myPost
            thepost.content= request.POST.get('content')
            if request.POST.get('noMedia'):
                thepost.media= None
            data={
                'postId':thepost.id,
                'content':thepost.content
            }
            thepost.save()
        elif method == 'delete':
            myPost= self.getPost(request)
            thepost= myPost
            data={
                'postId':thepost.id
            }
            thepost.delete()
        return JsonResponse(data)

class PostCtrlsView(View):

    def post(self, request):
        method= request.POST.get('method')
        myUser= UserProfile.objects.get(user=request.user)
        try:
            myPost= Post.objects.get(id= request.POST.get('postId'))
        except: None
        
        if method == 'like':
            liked= Like()
            liked.user= myUser
            liked.post= myPost
            liked.save()
            data={
                'post':myPost.id,
                'status':'liked'
            }        
        elif method == 'unlike':
            liked= Like.objects.filter(user= myUser, post= myPost)
            liked.delete()
            data={
                'post':myPost.id,
                'status':'unliked'
            }

        elif method == 'add':
            myPost= Post.objects.get(id= request.POST.get('postId'))
            commented= Comment()
            commented.user= myUser
            commented.post= myPost
            commented.content= request.POST.get('contnet')
            commented.save()
            data={
                'imgUrl':myUser.pfp.url,
                'username':myUser.user.username,
                'fullname':myUser.fullName,
                'commId':commented.id,
                'post':commented.post.id,
            }
        elif method == 'delete':
            commented= Comment.objects.get(id= request.POST.get('commId'))
            data={
                'post':commented.post.id,
            }
            commented.delete()
        elif method == 'edit':
            commented= Comment.objects.get(id= request.POST.get('commId'))
            commented.content= request.POST.get('content')
            data={
                'content': request.POST.get('content'),
                'commId':commented.id,
            }
            commented.save()
            
        return JsonResponse(data)