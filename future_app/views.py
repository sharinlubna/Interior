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


def Blog_view(request):
    blog = Blog.objects.all()
    return render(request, 'blog.html', locals())


def Blog_Detail(request, id):
    blog = Blog.objects.filter(id=id)
    return render(request, 'blog_detail.html', locals())


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
        print(time)
        print(date)

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
            if user.is_staff == 1:
                if user.is_superuser == 1:
                    login(request, user)
                    return redirect(AdminDashboard)
                else:
                    login(request, user)
                    return redirect(staff_dashboard)
            else:
                print('not admin/staff')
                return redirect(Home)
        else:
            print('authentication failed')
            return redirect(Home)
    else:
        print('not a POST request')
        return redirect(Home)


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
                    phone_number=phone_number,
                    user_type=2  # Assuming 2 is for staff members
                )
                stf.set_password(password)
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
                return redirect(staff_list)

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

        return redirect(staff_list)
    else:
        return render(request, 'edit_staff.html', locals())


def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, staff_id=staff_id)
    User.objects.filter(id=staff_id).delete()
    staff.delete()
    messages.success(request, 'Staff member deleted successfully.')
    return redirect(staff_list)


def create_admin_blog(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')

        blog = Blog.objects.create(
            title=title,
            author=author,
            description=description,
            detail=detail,
            image=image,
            sub_title=sub_title,
            image1=image1,
            exp=exp
        )
        blog.save()
        return redirect(admin_blogs)
    else:
        return render(request, 'create_admin_blog.html', locals())


def admin_blogs(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    item = Blog.objects.all()
    return render(request, 'admin_blogs.html', locals())


def edit_admin_blog(request, id):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    item = Blog.objects.filter(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')
        try:
            Blog.objects.get(id=id)
            Blog.objects.filter(id=id).update(title=title,
                                              author=author,
                                              description=description,
                                              detail=detail,
                                              sub_title=sub_title,
                                              exp=exp)
            instance = get_object_or_404(Blog, id=id)
            if image:
                instance.image = image
            instance.save()

            extimage = get_object_or_404(Blog, id=id)
            if image1:
                extimage.image1 =image1
            extimage.save()

            return redirect(admin_blogs)
        except Blog.DoesNotExist:
            return redirect(admin_blogs)

    else:
        return render(request, 'edit_admin_blog.html', locals())


def delete_item(request,id):
    Blog.objects.filter(id=id).delete()
    return redirect(admin_blogs)

def appointment_list(request):
    app = Appointment.objects.all()
    return render(request, 'appointment_list.html', locals())


def appointment_view(request, id):
    app = Appointment.objects.filter(id=id)
    return render(request, 'appointment_view.html', locals())

def schedule(request, id):
    app = Appointment.objects.filter(id=id)
    staff = User.objects.filter(is_staff=1, is_superuser=0)
    return render(request, 'schedule_appointment.html', locals())
def schedule_appointment(request, id):
    app = Appointment.objects.filter(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        user = User.objects.get(id=name)
        date = request.POST.get('date')
        time = request.POST.get('time')
        Appointment.objects.filter(id=id).update(staff_name=user, date=date, time=time)
        print(name)
        app.status = '2'


        # send_mail(
        #     'Appointment Scheduled',
        #     f'Your appointment has been scheduled for {date} at {time}.',
        #     'admin@example.com',
        #     [app.email],
        #     fail_silently=False,
        # )

        return redirect(appointment_list)


def reject_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    # Add your rejection logic here
    # For example, updating the status of the appointment
    appointment.status = '3'
    appointment.save()
    return redirect(appointment_list)


def staff_dashboard(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)

    return render(request, 'staff_dashboard.html', locals())


def staff_appointments(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    app = Appointment.objects.all()
    return render(request, 'staff_appointments.html', locals())
