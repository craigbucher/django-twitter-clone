from django.db import models
from django.contrib.auth.models import User	# model django uses for authentication
from django.db.models.signals import post_save

# create deet model
class Deet(models.Model):
	user = models.ForeignKey(	# ForeignKey = 'user' in 'Profiles' model, below
		User, related_name="deets", 
		on_delete=models.DO_NOTHING	# don't delete the user!
		)
	body = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)	# runs only when created
	modified_at = models.DateTimeField(auto_now=True)
	likes = models.ManyToManyField(User, related_name="deet_like", blank=True)	# which deets this user liked

	# Keep track or count of likes for each deet:
	def number_of_likes(self):
		return self.likes.count()

	def __str__(self):
		return(
			f"{self.user} "
			f"({self.created_at:%Y-%m-%d %H:%M}): "
			f"{self.body}..."
			)

# Create A User Profile Model
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self", 
		related_name="followed_by",	# used to specify the name of the reverse relationship on the related model
		symmetrical=False,	# following is not necessarily both ways
		blank=True)	
	
	date_modified = models.DateTimeField(User, auto_now=True)	
	profile_image = models.ImageField(null=True, blank=True, upload_to="images/")	# = media/images; will be automatically created
	profile_bio = models.CharField(null=True, blank=True, max_length=500)
	homepage_link = models.CharField(null=True, blank=True, max_length=100)
	facebook_link = models.CharField(null=True, blank=True, max_length=100)
	instagram_link = models.CharField(null=True, blank=True, max_length=100) 
	linkedin_link = models.CharField(null=True, blank=True, max_length=100)
	
	def __str__(self):
		return self.user.username

# Create Profile When New User Signs Up
# Don't have to make migation after add this - why???? Because is using a signal?
# @receiver(post_save, sender=User) = could use this decorator, instead, if we wanted to
def create_profile(sender, instance, created, **kwargs):	# 'instance' = new user
	if created:	# if new user has been created:
		user_profile = Profile(user=instance)	# associate them with a profile
		user_profile.save()
		# Have the user follow themselves (so they can see their own posts)
		user_profile.follows.set([instance.profile.id])
		user_profile.save()	# can't include in save, above, because profile has to be created first

# run 'create_profile' after new user is created:
post_save.connect(create_profile, sender=User)