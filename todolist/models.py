from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ESTADOS = [
    ('pendiente','Pendiente'),
    ('terminada', 'Terminada')
]


class Task(models.Model):
    title = models.CharField(max_length=40, null=False, blank=False, verbose_name="Titulo")
    description = models.TextField(max_length=300, null=False, blank=False, verbose_name="Descripcion")
    status = models.CharField(default='pendiente',choices=ESTADOS, verbose_name="Estado")
    due_date = models.DateField(verbose_name="Fecha de limite")
    
    users = models.ManyToManyField(
    User,
    related_name="tasks", blank=True                
    )
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_task")
    
    def __str__(self):
        return self.title
    
