from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Blog, Profile
# from .forms import ProfileForm


admin.site.unregister(Group)
admin.site.register(Blog)

# Combine profile to user
class ProfileInline(admin.StackedInline):
    model = Profile
    

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['first_name','last_name','email']
    inlines = [ProfileInline]

    
# Unregister Initial User
admin.site.unregister(User)

# Register user and profile
admin.site.register(User, UserAdmin)

    

