from django.db import models
from accounts.models import UserProfile

class Post(models.Model):
    author= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content= models.TextField(max_length=10000)
    media= models.FileField(null=True, blank=True, upload_to='posts_media')
    date= models.DateTimeField(auto_now_add=True) 

    def allUserPosts(theUser):
        posts=Post.objects.filter(author= UserProfile.objects.get(user=theUser)).order_by('-date')
        return posts

    def likes(self):
        myPost= Post.objects.get(id= self.id)
        likesObj= Like.objects.filter(post=myPost).values_list('user',flat=True)
        return list(likesObj)

    def comments(self):
        myPost= Post.objects.get(id= self.id)
        commsObj= Comment.objects.filter(post=myPost)
        return commsObj

class Like(models.Model):
    user= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)



class Comment(models.Model):
    user= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    content= models.TextField(max_length=5000,null=False, blank=False)
