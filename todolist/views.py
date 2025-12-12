from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . forms import TaskForm, UserCreationForm
from . models import Task
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        return redirect ('dashboard')
    
    return redirect ('login')


@login_required
def dashboard(request):
    is_manager = request.user.groups.filter(name="Manager").exists()
    
    if is_manager:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(users=request.user)
        
    # Filtrar por estado
    status = request.GET.get("status")

    if status:
        tasks = tasks.filter(status=status)
        
    # Filtrar por fecha de vencimiento
    due = request.GET.get("due")
    today = timezone.now().date()
    
    if due == "today":
        tasks = tasks.filter(due_date=today)
    elif due == "week":
        week_end = today + timedelta(days=7)
        tasks = tasks.filter(due_date__range=[today, week_end])
    elif due == "late":
        tasks = tasks.filter(due_date__lt=today)
     
    # Filtrar por usuario asignado (solo managers)
    if is_manager:
        user_id = request.GET.get("assigned_to")
        
        # Corregido: Si user_id existe (no es None) Y NO es una cadena vacía (value="")
        # Y aseguramos que sea un dígito antes de usarlo en el filtro
        if user_id and user_id.isdigit():
            # Filtra las tareas asignadas al usuario con ese ID
            tasks = tasks.filter(users__id=user_id) # Usar users__id si es un M2M field
            
    tasks = tasks.order_by("status")
    
    return render(request, 'dashboard.html', {
        'nombre_usuario': request.user.username,
        'tasks': tasks,
        "is_manager": is_manager,
        "all_users": User.objects.all(),
    })


def create(request):
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task =  form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            
            if task.users.count() == 0:
                task.users.add(request.user)
            
            return redirect('dashboard')
    
    else:
        form = TaskForm()
        
    return render (request, "create.html", {"form":form})

def update(request, id):
    task = get_object_or_404(Task, id=id)
    
    if not (
        task.creator == request.user or 
        request.user.groups.filter(name="Manager").exists()
    ):
        return HttpResponseForbidden("No tienes permiso para editar esta tarea.")

    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid:
            form.save()
            return redirect('dashboard')
        
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'update.html', {"form":form, "task":task})
    
def delete(request, id):
    task = get_object_or_404(Task, id=id)
    
    if not (
        task.creator == request.user or 
        request.user.groups.filter(name="Manager").exists()
    ):
        return HttpResponseForbidden("No tienes permiso para eliminar esta tarea.")

    task.delete()
    
    return redirect('dashboard')

def detail(request, id):
    is_manager =  request.user.groups.filter(name="Manager").exists()
    task = get_object_or_404(Task, id=id)
    usuarios = task.users.all()
    
    return render (request, 'detail.html', {"task":task, "usuarios":usuarios, "is_manager":is_manager})

def task_status(request, id):
    task = get_object_or_404(Task, id=id)
    
    if task.status == "pendiente":
        task.status = "terminada"
        task.save()
        return redirect('dashboard')
    
    else:
        task.status = "pendiente"
        task.save()
        return redirect('dashboard')
    
def register_user(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        
    return render(request, "register.html", {"form":form})
            