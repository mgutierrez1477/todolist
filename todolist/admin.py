from django.contrib import admin
from . models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    
    list_display = ("title", "description", "status", "due_date", "get_users")
    
    list_filter = ("status", "due_date")
    
    search_fields = ("title", "status")
    
    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    
    get_users.short_description = "Usuarios asignados"
    
    
admin.site.register(Task, TaskAdmin)
