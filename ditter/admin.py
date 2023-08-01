from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Deet

# Unregister Groups - get rid of selection on main admin page
admin.site.unregister(Group)

# Mix Profile info into general User info in admin panel
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	# Just display username fields on admin page
	fields = ["username"]
	# add profile info to general 'User' listing
	inlines = [ProfileInline]

# Unregister initial User (so changes in UserAdmin can take effect)
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)

# Register Deets
admin.site.register(Deet)