from django.contrib import admin
from .models import Authentication,Hostel,Floor
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AuthAdmin(UserAdmin):
    model = Authentication

    list_display = ('username','first_name','is_student','is_supervisor')

    fieldsets = (
        (None,{'fields':('username','password')}),
        (('Person Details'),{'fields':('email','first_name','mobile_number')}),
        (('Special Permissions'),{'fields':('is_active','is_supervisor')})
    )

admin.site.register(Authentication,AuthAdmin)

class HostelAdmin(admin.ModelAdmin):
    model = Hostel

    list_display = ('hostel_id','hostel_name','supervisor_mail','floors','location')
    list_filter = ('location',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs['queryset'] = Authentication.objects.filter(is_supervisor = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (('Create Hostel Record'),{'fields':('hostel_id','hostel_name','supervisor_mail','floors','location'),}),
    )

class FloorAdmin(admin.ModelAdmin):
    model = Floor
    list_display = ('floor_id','hostel_id','no_of_rooms','warden_name')

    fieldsets = (
        (('Create Floor Object'),{'fields':('floor_id','hostel_id','no_of_rooms','warden_name')}),
    )


admin.site.register(Floor,FloorAdmin)

admin.site.register(Hostel,HostelAdmin)