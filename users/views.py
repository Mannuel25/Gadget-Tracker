from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm


def index(request):
    data = User.objects.all()
    context = {'data': data}
    return render(request, 'display.html', context)

def upload(request):
    if request.method == 'GET':
        form  = UserForm()
    else:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'upload.html', {'form':form})



