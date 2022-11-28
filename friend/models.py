from sqlite3 import Timestamp
from django.db import models
from django.contrib.auth.models import User

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            
    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, account):
        """
        Unfriending function
        """
        user_friends_list = self
        user_friends_list.remove_friend(account)

        friends_list = FriendList.objects.get(user=account)
        friends_list.remove_friend(self.user)
     
    def is_mutual_friend(self, friend):
        """
        finding mutual friend
        """
        
        friendList = FriendList.objects.get(user=friend)

        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a friend request
        Update both sender and receiver friend list
        """

        receiver_friend_list = FriendList.objects.get(user = self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user = self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        """
        self.is_active = False
        self.save()
