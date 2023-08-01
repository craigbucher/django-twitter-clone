# from: https://www.youtube.com/watch?v=u6IskcT14LQ
# https://github.com/flatplanet/musker

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Deet
from django.contrib.auth.models import User
from .forms import DeetForm, SignUpForm, ProfilePicForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

def home(request):
	if request.user.is_authenticated:
		form = DeetForm(request.POST or None)	# 'None' = form submitted without any data
		if request.method == "POST":
			if form.is_valid():
				deet = form.save(commit=False)	# don't save to database just yet because we have to associate it with a user (below)
				deet.user = request.user
				deet.save()
				messages.success(request, ("Your Deet Has Been Posted!"))
				return redirect('home')
		
		deets = Deet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"deets":deets, "form":form})
	else:
		deets = Deet.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"deets":deets})

def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)	# all profiles except my own
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		deets = Deet.objects.filter(user_id=pk).order_by("-created_at")
		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()
		return render(request, "profile.html", {"profile":profile, "deets":deets})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:	# 'None' if form is blank
			login(request, user)
			messages.success(request, (f"Welcome {user.first_name}! Get DEETING!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')
	else:
		return render(request, "login.html", {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out. Sorry to Deet You Go..."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Validate data:
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']	# optional - format doesn't really affect anything
			# second_name = form.cleaned_data['second_name']	# optional - format doesn't really affect anything
			# email = form.cleaned_data['email']	# optional - format doesn't really affect anything
			# Log in user #
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, (f"You have successfully registered! Welcome {user.first_name}!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)	# get User info
		# since 'User' is a realtional field in 'Profile', django refer's to it as 'user__id':
		profile_user = Profile.objects.get(user__id=request.user.id)	# get User *Profile* info
		# Get Forms:
		# None = no information submitted in form
		# instance = fill form with 'current_user's information
		user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=current_user)	# request.FILES = for profile image
		# user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)	# request.FILES = for profile image
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)	# request.FILES = for profile image
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			login(request, current_user)	# django logs user out when user info is updated (!)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')

def deet_like(request, pk):
	if request.user.is_authenticated:
		deet = get_object_or_404(Deet, id=pk)	# query database and return 404 if object doesn't exits
		if deet.likes.filter(id=request.user.id):	# if user already likes deet
			deet.likes.remove(request.user)	# unlike the deet
		else:
			deet.likes.add(request.user)	# like the deet
		# request.META.get("HTTP_REFERER") = page we came from - allows us to go
		# back to the same page from which the user liked the deet;
		# use this because users all have different id's, so URL would be different
		# for each user; also can be used on 'Home' page
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	
def deet_show(request, pk):
	deet = get_object_or_404(Deet, id=pk)
	if deet:	# confirm deet id actually exists
		return render(request, "show_deet.html", {'deet':deet})
	else:
		messages.success(request, ("That Deet Does Not Exist..."))
		return redirect('home')	

def delete_deet(request, pk):
	if request.user.is_authenticated:
		deet = get_object_or_404(Deet, id=pk)
		# Check to see if you own the deet
		if request.user.username == deet.user.username:
			# Delete The Deet
			deet.delete()
			messages.success(request, ("Your Deet Has Been Deleted!"))
			# request.META.get("HTTP_REFERER") = page we came from - allows us to go
			# back to the same page from which the user deleted the deet;
			# use this because users all have different id's, so URL would be 
			# different	for each user; also can be used on 'Home' page
			return redirect(request.META.get("HTTP_REFERER"))	
		else:
			messages.success(request, ("You Don't Own That Deet!!"))
			return redirect('home')
	else:
		messages.success(request, ("Please Log In To Continue..."))
		# HTTP_REFERER = see above
		return redirect(request.META.get("HTTP_REFERER"))

def edit_deet(request,pk):
	if request.user.is_authenticated:
		# Grab The Deet!
		deet = get_object_or_404(Deet, id=pk)
		# Check to see if you own the deet
		if request.user.username == deet.user.username:
			# use the deet form, but fill with current info (instance=deet):
			form = DeetForm(request.POST or None, instance=deet)
			if request.method == "POST":
				if form.is_valid():
					deet = form.save(commit=False)
					deet.user = request.user
					deet.save()
					messages.success(request, ("Your Deet Has Been Updated!"))
					return redirect('home')
			else:
				return render(request, "edit_deet.html", {'form':form, 'deet':deet})
		else:
			messages.success(request, ("You Don't Own That Deet!!"))
			return redirect('home')
	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect('home')

def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()
		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		# request.META.get("HTTP_REFERER") = page we came from - allows us to go
		# back to the same page from which the user followed the profile;
		# use this because users all have different id's, so URL would be 
		# different	for each user; also can be used on 'Home' page
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()
		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		# request.META.get("HTTP_REFERER") = page we came from - allows us to go
		# back to the same page from which the user unfollowed the profile;
		# use this because users all have different id's, so URL would be 
		# different	for each user; also can be used on 'Home' page
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

# Basically just a subset of profile list
def follows(request, pk):	# pk = profile.user.id
	if request.user.is_authenticated:
		# if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			user = User.objects.get(id=pk)
			return render(request, 'follows.html', {"profiles":profiles, "user":user})
		# else:
			# messages.success(request, ("That's Not Your Profile Page..."))
			# return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

# Basically just a subset of profile list
def followers(request, pk):	# pk = profile.user.id
	if request.user.is_authenticated:
		# if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			user = User.objects.get(id=pk)
			return render(request, 'followers.html', {"profiles":profiles, "user":user})
		# else:
			# messages.success(request, ("That's Not Your Profile Page..."))
			# return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def search(request):
	if request.method == "POST":
		# Grab the form field input
		search = request.POST['search']	# = 'name="search"' in <input> tag
		# Search the database
		searched = Deet.objects.filter(body__contains = search)
		return render(request, 'search.html', {'search':search, 'searched':searched})
	else:
		return render(request, 'search.html', {})

def search_user(request):
	if request.method == "POST":
		# Grab the form field input
		search = request.POST['search']	# = 'name="search"' in <input> tag
		# Search the database
		searched = User.objects.filter(username__contains = search)
		return render(request, 'search_user.html', {'search':search, 'searched':searched})
	else:
		return render(request, 'search_user.html', {})

def change_password(request, pk):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)	# get User info
		# Get Forms:
		pwd_form = PasswordChangeForm(request.user, request.POST)
		if pwd_form.is_valid():
			print(pwd_form)
			pwd_form.save()
			# print(current_user)
			update_session_auth_hash(request, request.user)	# otherwise django logs user out when user info is updated (!)
			messages.success(request, ("Your Password Has Been Updated!"))
			return redirect('home')
		return render(request, "change_password.html", {'pwd_form':pwd_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')