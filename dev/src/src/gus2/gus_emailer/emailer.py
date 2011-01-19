from django.db import models

class emailer():
    """ 
	Enables Calender and User to trigger an email to another user or list of users.
	"""

	def send_message(self, message):
        """
        @rtype: int
        @return: self.id
        """
		
		raise Exception("In development", "This function does not work yet")
        
	def archive_message(self, message):
		""" 
		after a message as been sent, add it to the message_history 
		@rtype: bool
		@return confirmation of action
		"""

class message(emailer):
	""" 
	An individual message to be sent out throught the emailer 
	"""	
	#message_id
	
	def __init__ (self, recipients, body, attachments, BCC, CC ):
		""" initiatlize a message object """
		raise Exception("In Development", "This function does not work, yet.")
        
		
class message_history(emailer):
	""" used to store a list of messages sent through the emailer """
	
	#message_list
	
	def add_message(self, message):
		"""
		@rtype: bool
		@return confirmation of action
		"""
		
	def delete_message(self, message_id):
		"""
		@rtype: bool
		@return confirmation of action
		"""
		
	def display_history(self, sort_parameter):
		"""
		@rtype: list
		@return list of messages
		"""