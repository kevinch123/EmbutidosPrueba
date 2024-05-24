from django.shortcuts import render, redirect
from .models import pedido
from django.urls import reverse

def index(request):
    data = pedido.objects.all().order_by('-id')
    context = {"db_data": data, "update": None}
    return render(request, "app/index.html", context)

def insert(request):
    if request.method == 'POST':
        try:
            task_subject = request.POST["subject"]
            task_description = request.POST["description"]
            if not task_subject or not task_description:
                raise ValueError("El texto no puede estar vacío.")
            db_data = pedido(subject=task_subject, description=task_description)
            db_data.save()
        except ValueError as err:
            print(err)  # Log the error for debugging purposes
    return redirect("index")

def update(request):
    if request.method == 'POST':
        task_id = request.POST["id"]
        task_subject = request.POST["subject"]
        task_description = request.POST["description"]
        db_data = pedido.objects.get(pk=task_id)
        db_data.subject = task_subject
        db_data.description = task_description
        db_data.save()
    return redirect("index")

def update_form(request, task_id):
    data = pedido.objects.all().order_by('-id')
    update_data = pedido.objects.get(pk=task_id)
    context = {"db_data": data, "update": update_data}
    return render(request, "app/index.html", context)

def delete(request, task_id):
    pedido.objects.filter(id=task_id).delete()
    return redirect("index")
