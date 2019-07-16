from django.contrib import admin
from people.models import Person, Organizations, User_info, ClubAnnouncements, MembershipApplication

# Register your models here.
admin.site.register(Person)
admin.site.register(Organizations)
admin.site.register(User_info)
admin.site.register(ClubAnnouncements)
admin.site.register(MembershipApplication)