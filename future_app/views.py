from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.core.paginator import Paginator


# Create your views here.


def Home(request):
    author = User.objects.all()
    blog = Blog.objects.all()
    return render(request, 'index.html', locals())


def About(request):
    return render(request, 'about.html')


def Blog_view(request):
    author = User.objects.all()
    blog_list = Blog.objects.all()

    # Pagination setup
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page.
    page_number = request.GET.get('page')
    blog = paginator.get_page(page_number)
    return render(request, 'blog.html', locals())


def Blog_Detail(request, id):
    blog = Blog.objects.filter(id=id)
    author = User.objects.all()
    blog_list = Blog.objects.order_by('-date')[:3]
    single_blog = get_object_or_404(Blog, id=id)
    # Fetch related blog posts (randomly)
    related_blog = Blog.objects.exclude(id=single_blog.id).order_by('?')[:2]

    # Fetch previous and next blog posts
    prev_blog = Blog.objects.filter(date__lt=single_blog.date).order_by('-date').first()
    next_blog = Blog.objects.filter(date__gt=single_blog.date).order_by('date').first()

    # Handle search functionality
    query = request.GET.get('q', '')
    if query:
        search_results = Blog.objects.filter(title__icontains=query) | Blog.objects.filter(description__icontains=query)
    else:
        search_results = Blog.objects.none()
    return render(request, 'blog_detail.html', locals())



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact_message = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            datetime=timezone.now()
        )

        # Notify the admin
        admin = User.objects.get(id=1)
        admin_message = "You have a new contact message from {} ({}):\n message: {}".format(
            contact_message.name,
            contact_message.email,
            contact_message.message
        )
        Notification.objects.create(
            user=admin,
            read=False,
            message=admin_message,
            datetime=timezone.now()
        )

        return HttpResponse("<h1>Thanks for contacting us</h1>")
    return render(request, 'contact.html')


def Team(request):
    staff = Staff.objects.all()
    emp = User.objects.all()
    return render(request, 'team.html', locals())


def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        department = request.POST.get('department')
        description = request.POST.get('description')
        address = request.POST.get('address')
        password = request.POST.get('phone')
        print(time)
        print(date)

        # Check if a user with this email already exists
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            # If the user exists, retrieve the existing user
            client = User.objects.get(email=email)
        else:
            # If the user does not exist, create a new user
            client = User.objects.create(
                is_superuser=0,
                is_staff=0,
                username=email,
                email=email,
                name=name,
                phone_number=phone,
                user_type=3
            )
            client.set_password(password)
            client.save()

        details = Appointment.objects.create(client=client,
                                             date=date,
                                             time=time,
                                             address=address,
                                             department=department,
                                             description=description)
        details.save()

        return HttpResponse("<h1>Appointment booked successfully. Our team will reach you shortly </h1>")

    return render(request, 'appointment.html')


def user_login(request):
    return render(request, 'login.html')


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
                print('client')
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


def subscribe(request):
    subscription = Subscription.objects.all()
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                return HttpResponse("<h1>Thanks for subscribing!</h1>")
            else:
                return HttpResponse("<h1>You are already subscribed.</h1>")
    return redirect(Home)



#admin operations

def AdminDashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_notification(request):
    notifications = Notification.objects.filter(user=request.user.id).order_by('-datetime')

    # Get the current time
    current_time = datetime.now()

    # Calculate time ago for each notification
    for i in notifications:
        current_time = datetime.now()
        time_difference = current_time - i.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            i.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            i.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            i.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            i.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            i.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            i.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            i.time_ago = f"{weeks} weeks ago"

    # read true

    for i in notifications:
        i.read = True
        i.save()
    return render(request, 'admin_notification.html', locals())

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
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')

        blog = Blog.objects.create(
            title=title,
            description=description,
            detail=detail,
            image=image,
            sub_title=sub_title,
            image1=image1,
            exp=exp,
            user=user
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
    item = Blog.objects.filter(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')
        try:
            Blog.objects.get(id=id)
            Blog.objects.filter(id=id).update(title=title,
                                              description=description,
                                              detail=detail,
                                              sub_title=sub_title,
                                              user=user,
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
    user = User.objects.get(id=request.user.id)
    if user.is_superuser == 1:
        return redirect(admin_blogs)
    else:
        return redirect(staff_blog)

def appointment_list(request):
    app = Appointment.objects.all()
    app1 = Appointment.objects.filter(status=1)
    app2 = Appointment.objects.filter(status=2)
    client = User.objects.all()
    return render(request, 'appointment_list.html', locals())


def appointment_view(request, id):
    client = User.objects.filter(id=id)
    app = Appointment.objects.filter(client_id=id)

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
        Appointment.objects.filter(id=id).update(staff_name=user, date=date, time=time, status=2)




        # send_mail(
        #     'Appointment Scheduled',
        #     f'Your appointment has been scheduled for {date} at {time}.',
        #     'admin@example.com',
        #     [app.email],
        #     fail_silently=False,
        # )

        return redirect(appointment_list)

def schedule_app_view(request, id):
    app = Appointment.objects.filter(client_id=id)
    client = User.objects.all()
    return render(request, 'schedule_app_view.html', locals())


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
    client = User.objects.all()
    app = Appointment.objects.filter(staff_name_id=user).order_by('-id')
    return render(request, 'staff_appointments.html', locals())


def staff_app_view(request, id):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    client = User.objects.filter(id=id)
    app = Appointment.objects.filter(client_id=id)

    return render(request, 'staff_app_view.html', locals())


def staff_reject_appointment(request, id):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    client = User.objects.filter(id=id)
    app = Appointment.objects.filter(client_id=id)
    return redirect(staff_appointments)


def staff_blog(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    item = Blog.objects.filter(user_id=user).order_by('-id')
    return render(request, 'staff_blog.html', locals())


def create_staff_blog(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')

        blog = Blog.objects.create(
            title=title,
            description=description,
            detail=detail,
            image=image,
            sub_title=sub_title,
            image1=image1,
            exp=exp,
            user=user
        )
        blog.save()
        return redirect(staff_blog)
    else:
        return render(request, 'create_staff_blog.html', locals())


def edit_staff_blog(request, id):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    item = Blog.objects.filter(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        image = request.FILES.get('image')
        sub_title = request.POST.get('sub_title')
        image1 = request.FILES.get('image1')
        exp = request.POST.get('exp')
        try:
            Blog.objects.get(id=id)
            Blog.objects.filter(id=id).update(title=title,
                                              description=description,
                                              detail=detail,
                                              sub_title=sub_title,
                                              user=user,
                                              exp=exp)
            instance = get_object_or_404(Blog, id=id)
            if image:
                instance.image = image
            instance.save()

            extimage = get_object_or_404(Blog, id=id)
            if image1:
                extimage.image1 =image1
            extimage.save()

            return redirect(staff_blog)
        except Blog.DoesNotExist:
            return redirect(staff_blog)

    else:
        return render(request, 'edit_staff_blog.html', locals())



def client_profile(request):
    user = User.objects.get(id=request.user.id)
    client = User.objects.filter(id=request.user.id)
    design_preference = DesignPreference.objects.filter(client_id=user)
    return render(request, 'client_profile.html', locals())

def design_preference(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        style = request.POST.get('style')
        color_palette = request.POST.get('color_palette')
        materials = request.POST.get('materials')
        budget = request.POST.get('budget')
        try:
            design = DesignPreference.objects.create(
                client_id=request.user.id,
                style=style,
                color_palette=color_palette,
                materials=materials,
                budget=budget)
            design.save()
            return redirect(client_profile)
        except DesignPreference.DoesNotExist:
            return render(request, 'design_preference.html',locals())
    else:
        return render(request, 'design_preference.html', locals())


def project_updates(request):
    try:
        user = User.objects.filter(id=request.user.id)
        return render(request, 'project_updates.html', locals())
    except User.DoesNotExist:
        return render(request, 'project_updates.html')