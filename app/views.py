from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView
from .decorators import for_admins
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, CustomUserCreationForm, GadgetFormSet
from .models import CustomUser, Gadget
import requests, os
from django.http import FileResponse, HttpResponse


class HomePageView(TemplateView):
    template_name = 'home.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'


def signup_user(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', context={'form': form})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/signup.html', context={'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email address or password")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


class UserAndGadgets():
    form_class = UserForm
    model = CustomUser
    template_name = "add_users_gadgets.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('dashboard')

    def formset_gadgets_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        gadgets = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in gadgets:
            variant.owner = self.object
            variant.save()

class UserGadgetsCreate(UserAndGadgets, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(UserGadgetsCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'gadgets': GadgetFormSet(prefix='gadgets'),
            }
        else:
            return {
                'gadgets': GadgetFormSet(self.request.POST or None, self.request.FILES or None, prefix='gadgets'),
            }

class UserGadgetsUpdate(UserAndGadgets, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(UserGadgetsUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'gadgets': GadgetFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='gadgets'),
        }


@login_required(login_url='login')
def all_students(request):
    search_input = request.GET.get('search')
    if search_input == None:
        students = CustomUser.objects.filter(user_type='student')
    else:
        students = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'students.html', {'students' : students})

@login_required(login_url='login')
def all_staff(request):
    search_input = request.GET.get('search')
    if search_input == None:
        staff = CustomUser.objects.filter(user_type='staff')
    else:
        staff = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'staff.html', {'staff' : staff})

@login_required(login_url='login')
def all_vendors(request):
    search_input = request.GET.get('search')
    if search_input == None:
        vendors = CustomUser.objects.filter(user_type='vendor')
    else:
        vendors = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'vendors.html', {'vendors' : vendors})


@login_required(login_url='login')
@for_admins
def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect('dashboard')


@login_required(login_url='login')
@for_admins
def delete_gadget(request, id):
    gadget = get_object_or_404(Gadget, id=id)
    gadget.delete()
    return redirect('update_user', id=gadget.owner
    .id)


from django.http import FileResponse
from wsgiref.util import FileWrapper
import requests
import os

def download_template(request):
    # The link should be of the file directly
    url = 'https://github.com/Mannuel25/Gadget-Guardian/blob/main/User_Gadgets_Template.xlsx'
    file_extension = '.xlsx'
    r = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, 'wb') as f:
        f.write(r.content)
    file_wrapper = FileWrapper(open(filename, 'rb'))
    response = FileResponse(file_wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

