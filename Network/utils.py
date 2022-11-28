from glob import escape
from friend.models import FriendList, FriendRequest

def check_condition(sender, receiver):
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
        return friend_request
    except:
        return False