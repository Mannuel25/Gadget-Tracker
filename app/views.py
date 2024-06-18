from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView
from .decorators import for_admins
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, CustomUserCreationForm, GadgetFormSet, UploadedTemplatesForm
from .models import CustomUser, Gadget
import requests, datetime, os, openpyxl, time
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone


def format_current_date_time():
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date as MM/DD/YYYY
    formatted_date = current_datetime.strftime("%m/%d/%Y")

    # Format the time as HH:MM AM/PM
    formatted_time = current_datetime.strftime("%I:%M %p")
    print(formatted_date + " " + formatted_time)

    return formatted_date + " " + formatted_time


class HomePageView(TemplateView):
    template_name = 'home.html'


@login_required(login_url='login')
def dashboard(request):
    search_input = request.GET.get('search')
    gadgets = Gadget.objects.filter(model__icontains=search_input) if search_input else None
    missing_gadgets = Gadget.objects.filter(missing=True)
    student_count = CustomUser.objects.filter(user_type='student').count()
    staff_count = CustomUser.objects.filter(user_type='staff').count()
    vendor_count = CustomUser.objects.filter(user_type='vendor').count()
    total_count = student_count + staff_count + vendor_count
    users_count = {
        'total_count' : total_count, 'student_count' : student_count, 
        'staff_count' : staff_count, 'vendor_count' : vendor_count
        }
    return render(request, 'dashboard.html', {
        'gadgets' : gadgets, 'users_count' : users_count, 'missing_gadgets' : missing_gadgets
        }
    )


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
            # Log in the current user
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email address or password")

    return render(request, 'login.html')


@login_required(login_url='login')
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

    def formset_gadgets_valid(self, formset):
        for gadget_form in formset:
            if gadget_form.instance.missing:
                gadget_form.instance.missing_date = format_current_date_time()
            else:
                gadget_form.instance.missing_date = None
        formset.save()

        super(UserGadgetsUpdate, self).formset_gadgets_valid(formset)

    def get_context_data(self, **kwargs):
        ctx = super(UserGadgetsUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['is_edit'] = True
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
        for gadget in gadgets:
            if Gadget.objects.filter(owner=student, missing=True).exists():
                student.missing_gadget_exists = True

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
        for gadget in gadgets:
            if Gadget.objects.filter(owner=user, missing=True).exists():
                user.missing_gadget_exists = True

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
        for gadget in gadgets:
            if Gadget.objects.filter(owner=user, missing=True).exists():
                user.missing_gadget_exists = True

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


@login_required(login_url='login')
def download_template(request):
    url = 'https://res.cloudinary.com/dq5fvxkeo/raw/upload/v1698532497/User_Gadgets_Template_iqiefc.xlsx'
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
        gadgets = Gadget.objects.filter(model__icontains=search_input, missing=True)
    return render(request, 'missing_gadgets.html', {'gadgets' : gadgets})


@login_required(login_url='login')
def mark_gadget_as_found(request, id):
    gadget = Gadget.objects.get(id=id)
    gadget.missing, gadget.missing_date = False, None
    gadget.save()
    return redirect('missing_gadgets')


@login_required(login_url='login')
def report_missing_gadget(request, id):
    gadget = Gadget.objects.get(id=id)
    gadget.missing, gadget.missing_date = format_current_date_time(), None
    gadget.save()
    return redirect('dashboard')


def read_upload_users(filename):
    """
    It reads through the uploaded excel sheet, and saves the
    user details with their gadgets to the DB
    """
    try:
        filepath = f'media/uploaded_templates/{filename}'
        wb_obj = openpyxl.load_workbook(filepath)
        sheet_obj = wb_obj.active
        headers = next(sheet_obj.rows)
        headers, records = [i.value for i in headers], []
        row_count = 1
        DEPARTMENT_CHOICES = {
            'Mass Communication' : 'mass_com',
            'Information Technology' : 'info_tech',
            'International Relations' : 'interel',
            'Medical Laboratory Sciences' : 'med_lab',
            'Accounting' : 'accounting',
            'Political Science' : 'pol_sci',
            'Nursing Sciences' : 'nursing',
            'Business Administration' : 'bus_admin',
            'Economics' : 'econs',
            'B-Tech' : 'b_tech',
            'Marketing' : 'marketing',
            'Micobiology' : 'micro_bio',
            'BioTechnology' : 'bio_tech',
            'Computer Science' : 'comp_sci',
        }
        for c in sheet_obj.rows:
            if row_count > 1:
                if not all([rec.value is None for rec in c]):
                    # get the inputed details and save in a list
                    data = [rec.value for rec in c]
                    # check if that user with a gadget exists...if it does udpate the gadgets he/she has
                    user = CustomUser.objects.filter(user_id=data[1])
                    if user.exists():
                        gadget_ = Gadget.objects.filter(owner=user.first(), model=data[8])
                        if not gadget_.exists():
                            gadget_details = {
                                'owner' : user.first(),
                                'model' : data[8],
                                'color' : data[9],
                                'device_id' : data[10]
                            }
                            Gadget.objects.create(**gadget_details)
                    else:
                        # create a new user instance
                        user_details = {
                            'full_name' : data[0],
                            'user_id' : data[1],
                            'user_type' : data[2].lower(),
                            'phone_no' : data[3],
                            'email' : data[4],
                            'address' : data[5],
                            'department' : DEPARTMENT_CHOICES[data[6]] if data[6] else None,
                            'level' : data[7],
                            }
                        new_user = CustomUser.objects.create(**user_details)
                        # create a gadget instance
                        gadget_details = {  
                            'owner' : new_user,
                            'model' : data[8],
                            'color' : data[9],
                            'device_id' : data[10]
                        }
                        gadget = Gadget.objects.create(**gadget_details)
                else:
                    pass
            row_count += 1
        wb_obj.close()
        print(CustomUser.objects.all().count())
        return True, "Users uploaded successfully"
    except Exception as e:
        return False, "Users upload failed " + str(e)


@login_required(login_url='login')
def upload(request):
    if request.method == 'GET':
        form = UploadedTemplatesForm
    elif request.method == 'POST':
        form = UploadedTemplatesForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.uploaded_by = request.user
            form.save()
            filename = request.FILES["doc"].name
            filepath = f"media/uploaded_templates/{filename}"
            if filename.split('.')[-1] != 'xlsx':
                messages.error(request, "Invalid file uploaded!")
            else:
                upload_func = read_upload_users(filename)
                if upload_func[0]:
                    messages.success(request, upload_func[1])
                else:
                    messages.warning(request, upload_func[1])
                time.sleep(1)
    return render(request, 'upload_users.html', context={'form': form})

