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
import requests, os, datetime
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
import openpyxl
from django.db.models import Count, Case, When, F
from django.db import models

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

def format_current_date_time():
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date as MM/DD/YYYY
    formatted_date = current_datetime.strftime("%m/%d/%Y")

    # Format the time as HH:MM AM/PM
    formatted_time = current_datetime.strftime("%I:%M %p")

    return formatted_date + " " + formatted_time
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

    def formset_gadgets_valid(self, formset):
        # Call the parent formset valid method to save the formset.
        super(UserGadgetsUpdate, self).formset_gadgets_valid(formset)

        # get the particular gadget that was set to missing or not..making use of
        # the current timeand date, store the time and date it was reported missing
        # if it's been found, remove the date and time
        for gadget_form in formset:
            if gadget_form.instance.missing:
                gadget_form.instance.missing_date = format_current_date_time()
                gadget_form.instance.save()
            elif not gadget_form.instance.missing:
                gadget_form.instance.missing_date = None
                gadget_form.instance.save()

    def get_context_data(self, **kwargs):
        ctx = super(UserGadgetsUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        formsets = {
            'gadgets': GadgetFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='gadgets'),
            }
        return formsets


@login_required(login_url='login')
def all_students(request):
    search_input = request.GET.get('search')
    if search_input == None:
        students = CustomUser.objects.filter(user_type='student')
    else:
        students = CustomUser.objects.filter(user_type='student', full_name__icontains=search_input)
    gadgets = Gadget.objects.all()
    for student in students:
        student.first_gadget = student.gadget_set.first()
        if student.gadget_set.count() > 0:
            student.gadget_count = student.gadget_set.count() - 1
        else:
            student.gadget_count = student.gadget_set.count()

    return render(request, 'students.html', {'students' : students, 'gadgets' :gadgets})

@login_required(login_url='login')
def all_staff(request):
    search_input = request.GET.get('search')
    if search_input == None:
        staff = CustomUser.objects.filter(user_type='staff')
    else:
        staff = CustomUser.objects.filter(full_name__icontains=search_input, user_type='staff')
    gadgets = Gadget.objects.all()
    for user in staff:
        user.first_gadget = user.gadget_set.first()
        if user.gadget_set.count() > 0:
            user.gadget_count = user.gadget_set.count() - 1
        else:
            user.gadget_count = user.gadget_set.count()

    return render(request, 'staff.html', {'staff' : staff, 'gadgets' :gadgets})

@login_required(login_url='login')
def all_vendors(request):
    search_input = request.GET.get('search')
    if search_input == None:
        vendors = CustomUser.objects.filter(user_type='vendor')
    else:
        vendors = CustomUser.objects.filter(user_type='vendor', full_name__icontains=search_input)
    gadgets = Gadget.objects.all()
    for user in vendors:
        user.first_gadget = user.gadget_set.first()
        if user.gadget_set.count() > 0:
            user.gadget_count = user.gadget_set.count() - 1
        else:
            user.gadget_count = user.gadget_set.count()
    return render(request, 'vendors.html', {'vendors' : vendors, 'gadgets' :gadgets})


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
    return redirect('dashboard')


def download_template(request):
    url = 'https://res.cloudinary.com/dq5fvxkeo/raw/upload/v1698499311/User_Gadgets_Template_zkqpch.xlsx'
    r = requests.get(url)
    filename = 'User_Gadgets_Template.xlsx'
    with open(filename, 'wb') as f:
        f.write(r.content)
    file_wrapper = FileWrapper(open(filename, 'rb'))
    response = FileResponse(file_wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required(login_url='login')
def missing_gadgets(request):
    search_input = request.GET.get('search')
    if search_input == None:
        gadgets = Gadget.objects.filter(missing=True)
    else:
        gadgets = Gadget.objects.filter(owner__full_name__icontains=search_input, missing=True)
    return render(request, 'missing_gadgets.html', {'gadgets' : gadgets})


@login_required(login_url='login')
def mark_gadget_as_found(request, id):
    gadget = Gadget.objects.get(id=id)
    gadget.missing, gadget.missing_date = False, None
    gadget.save()
    return redirect('missing_gadgets')

