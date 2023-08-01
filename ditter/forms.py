from django import forms
from .models import Deet, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User	# model django uses for authentication

class SignUpForm(UserCreationForm):
	# 'attrs' = passed to form
	# bootstrap requires 'class':'form-control'
	# widgets are classes that are used to render form fields 	
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	# form metadata
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	# since 'username' and 'password' are part of the django 'User' model, we
	# have to define their layout a bit differently:
	# called when the form is created. It is used to initialize the form's fields 
	# and attributes. 
	# *args is used to pass a variable number of positional arguments to a function
	# **kwargs is used to pass a variable number of keyword arguments to a function
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)	# superset of 'SignUpForm' above

		# pretty much the same definitions as above, but in a different format:
		self.fields['username'].widget.attrs['class'] = 'form-control'	# required for bootstrap
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'	# displayed if/when form doesn't validate

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class DeetForm(forms.ModelForm):
	body = forms.CharField(required=True, 
		widget=forms.widgets.Textarea(
			attrs={
			"placeholder": "Enter Your Deet!",
			"class":"form-control",	# bootstrap class (all bootstrap forms have this)
			}
			),
			label="",
		)

	# The meta class in a Django form is used to specify the meta data for the 
	# form. This includes the model that the form is associated with, the fields 
	# that should be included in the form, and the widgets that should be used 
	# for each field. 

	class Meta:
		model = Deet
		exclude = ("user", "likes",)	# don't allow user to set 'likes' when creating a deet

# Profile Extras Form
class ProfilePicForm(forms.ModelForm):
	profile_image = forms.ImageField(label="Profile Picture")
	profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
	homepage_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
	facebook_link =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
	instagram_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
	linkedin_link =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'LinkedIn Link'}))
	
	class Meta:
		model = Profile	# save to 'Profile' model, **not** the 'User' model
		# adding 'fields' will allow them to be pre-filled with user's info:
		fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link', )

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
