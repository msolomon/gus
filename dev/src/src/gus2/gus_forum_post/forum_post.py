from django.db import import models
from gus_forum.models import forum_thread

class forum_post():
    """
    class forum_post is the basic level class in our forums, aggregating to forum thread
    """
    
    #All following fields are initialized upon creation, and cannot be modified by this class
    #ID of parent thread; cant be modified by this class
    thread_id = models.IntegerField()
    post_id = models.IntegerField() 
    user_id = models.IntegerField()
    date_created = models.DateTimeField()
    
    #Post text; not sure if we need a max post length. This is the only field that can be modified within this class
    post_content = models.CharField(max_length=5000)
    
    def EditPost(self,user_id):
        """
        Allows a user to edit the text of a post if they have the proper user_id, giving direct access to post_content
        """
        raise Exception("In development", "This function does not work yet")
    #End
#End
