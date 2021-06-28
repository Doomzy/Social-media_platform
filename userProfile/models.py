from django.db import models
from accounts.models import UserProfile
from django.contrib.auth.models import User

class Friend(models.Model):
    status_choices = {
        ('B', 'Binding'),
        ('F', 'Friends')
    }
    user1= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    user2= models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciver')
    status= models.CharField(choices=status_choices, max_length=2)
    
    def __str__(self):
        return (self.user1.username + " > " + self.user2.username + " = " + self.status)

    def friendList(user):
        userFriends=[]
        f1= Friend.objects.filter(user1=user.id, status= 'F').values(f_id=models.F('user2'))
        f2= Friend.objects.filter(user2=user.id, status= 'F').values(f_id=models.F('user1'))
        for f in f2:
            userFriends.append(UserProfile.objects.get(user=f['f_id']))
        for f in f1:
            userFriends.append(UserProfile.objects.get(user=f['f_id']))
        return (userFriends)

    def friendRequestsList(user):
        userFriends=[]
        allFriends= Friend.objects.filter(user2=user.id ,status= 'B').values('user1')
        for f in allFriends:
            userFriends.append(UserProfile.objects.get(user=f['user1']))
        return (userFriends)

    def sentFriendRequests(user):
        userFriends=[]
        allFriends= Friend.objects.filter(user1=user.id, status= 'B').values('user2')
        for f in allFriends:
            userFriends.append(UserProfile.objects.get(user=f['user2']))
        return (userFriends)