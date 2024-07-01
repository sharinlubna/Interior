from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.


def Home(request):
    return render(request, 'index.html')


def About(request):
    return render(request, 'about.html')


def Blog(request):
    return render(request, 'blog.html')


def Blog_Detail(request):
    return render(request, 'blog_detail.html')


def Contact(request):
    return render(request, 'contact.html')


def Team(request):
    staff = Staff.objects.all()
    emp = User.objects.all()
    return render(request, 'team.html', locals())


def Team_Detail(request):
    return render(request, 'team_detail.html')


def user_login(request):
    return render(request, 'login.html')


def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        department = request.POST.get('department')
        description = request.POST.get('description')

        details = Appointment.objects.create(name=name,
                                             email=email,
                                             phone=phone,
                                             date=date,
                                             time=time,
                                             department=department,
                                             description=description)
        details.save()

        return HttpResponse("<h1>Appointment booked successfully. Our team will reach you shortly </h1>")

    return render(request, 'appointment.html')


def UserLoginPage(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        password = request.POST.get('password')

        user = authenticate(username=u_id, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                if user.is_superuser:
                    return redirect('AdminDashboard')
                else:
                    return redirect('staff_home')
            else:
                print('not admin/staff')
                return redirect('Home')
        else:
            print('authentication failed')
            return redirect('Home')
    else:
        print('not a POST request')
        return redirect('Home')


def Logout(request):
    logout(request)
    return redirect(Home)




#admin operations

def AdminDashboard(request):
    return render(request, 'admin_dashboard.html')

def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        image = request.FILES.get('image')

        # Validate password matching
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
        else:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                # Create the User and Staff objects
                stf = User.objects.create(
                    is_staff=1,
                    username=username,
                    email=email,
                    name=name,
                    password=password,
                    phone_number=phone_number,
                    user_type=2  # Assuming 2 is for staff members
                )
                stf.save()

                staff = Staff.objects.create(
                    staff=stf,
                    image=image,
                    designation=designation,
                    experience=experience,
                    qualification=qualification
                )
                staff.save()

                messages.success(request, 'Staff member added successfully.')
                return redirect('staff_list')

    return render(request, 'add_staff.html')


def staff_list(request):
    stf = User.objects.filter(user_type=2)
    staff_members = Staff.objects.filter(staff__user_type=2)

    return render(request, 'staff_list.html', locals())


def edit_staff(request, staff_id):
    stff = Staff.objects.filter(staff_id=staff_id)
    stf = User.objects.filter(id=staff_id)
    instance = get_object_or_404(User, id=staff_id)
    profile = get_object_or_404(Staff, staff_id=staff_id)
    s_id = User.objects.get(id=staff_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        image = request.FILES.get('image')
        print(name, phone_number, designation, experience, qualification)

        User.objects.filter(id=staff_id).update(name=name,
                                                phone_number=phone_number)

        if username:
            instance.username = username
            instance.save()



        Staff.objects.filter(staff_id=staff_id).update(designation=designation,
                                                       staff_id=s_id,
                                                       experience=experience,
                                                       qualification=qualification)
        if image:
            profile.image = image
            profile.save()

        return redirect('staff_list')
    else:
        return render(request, 'edit_staff.html', locals())


def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, staff_id=staff_id)
    User.objects.filter(id=staff_id).delete()
    staff.delete()
    messages.success(request, 'Staff member deleted successfully.')
    return redirect('staff_list')



