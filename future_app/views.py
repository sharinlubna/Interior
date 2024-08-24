from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def Home(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    author = User.objects.all()
    blog = Blog.objects.all()
    services = Services.objects.all()
    review1 = Comment.objects.all().order_by('-created_at')
    review = Comment.objects.all()
    project = Project.objects.filter(status=3).order_by('-last_updated')
    project1 = Project.objects.filter(status=3).order_by('last_updated')
    design = DesignPreference.objects.all()
    staff = Staff.objects.all()

    # Calculate category-wise counts
    interior_count = max(Project.objects.filter(category="Interior").count() - 2, 0)
    construction_count = max(Project.objects.filter(category="Full House Construction").count() - 2, 0)

    # Calculate total projects done
    projects_done_count = max(Project.objects.filter(status=3).count() - 2, 0)

    # Calculate total staff count
    staff_count = max(Staff.objects.count() - 2, 0)
    return render(request, 'index.html', locals())


def About(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    staff = Staff.objects.all()
    author = User.objects.all()
    review1 = Comment.objects.all().order_by('-created_at')
    review = Comment.objects.all()
    return render(request, 'about.html', locals())


def Blog_view(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    author = User.objects.all()
    blog_list = Blog.objects.all()

    # Pagination setup
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page.
    page_number = request.GET.get('page')
    blog = paginator.get_page(page_number)
    return render(request, 'blog.html', locals())


def Blog_Detail(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
        contact_message.save()

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
        messages.success(request, "Thanks for contacting us")

    return render(request, 'contact.html', locals())


def Team(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    staff = Staff.objects.all()
    emp = User.objects.all()
    return render(request, 'team.html', locals())

def project(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    project = Project.objects.filter(status=3)
    staff = User.objects.all()
    return render(request, 'project.html', locals())


def project_view(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    project = Project.objects.filter(id=id)
    project_list = Project.objects.order_by('-end_date')[:3]
    design = DesignPreference.objects.all()
    staff = User.objects.all()
    single_project = get_object_or_404(Project, id=id)
    # Fetch related project(randomly)
    related_project = Project.objects.filter(status=3).exclude(id=single_project.id).order_by('?')[:2]
    projects = Project.objects.get(id=id)
    if projects:
        actual_budget = float(projects.actual_budget) if projects.actual_budget else 0
        cost = round(actual_budget / 100000, 2)
    else:
        cost = None

    return render(request, 'project_detail.html', locals())


def appointment(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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

        admin = User.objects.get(id=1)
        admin_message = "You have new appointment>"
        Notification.objects.create(user=admin,
                                    read=False,
                                    message=admin_message)

        messages.success(request, "Appointment booked successfully. Our team will reach you shortly")
        # return HttpResponse("<h1>Appointment booked successfully. Our team will reach you shortly </h1>")

    return render(request, 'appointment.html',locals())



def search_view(request):
    user = User.objects.all()
    query = request.GET.get('q')
    blogs = services = projects = staff = []

    if query:
        if Staff.objects.filter(designation__icontains=query).exists():
            staff = Staff.objects.filter(designation__icontains=query)
            return render(request, 'team_search.html', locals())

        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        services = Services.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query))
        return render(request, 'search_results.html',locals())

    return render(request, 'search_results.html', locals())

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
                messages.success(request, "Successfully subscribed.")
            else:
                messages.info(request, "You are already subscribed.")
    return redirect(Home)



#admin operations
@login_required
def AdminDashboard(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    staff = Staff.objects.all().count()
    projects = Project.objects.filter(status=3).count()
    enquiry = Appointment.objects.all().count()
    client = User.objects.all()
    app = Appointment.objects.filter(status=1).order_by('-created_at')[:10]
    return render(request, 'admin_dashboard.html', locals())


@login_required
def admin_profile(request):
    return render(request, 'admin_profile.html', locals())


@login_required
def admin_update(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    try:
        user = request.user
        if request.method == 'POST':
            name = request.POST.get('profileName')
            email = request.POST.get('profileEmail')
            phone = request.POST.get('profilePhone')

            # Update user fields

            user.name = name
            user.email = email
            user.phone_number = phone
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('admin_update')

        return render(request, 'admin_profile.html', locals())
    except User.DoesNotExist:
        return render(request, 'admin_profile.html')


@login_required
def admin_notification(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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


@login_required
def delete_notifications(request,id):
    my_notify = Notification.objects.filter(user_id=request.user.id)
    if my_notify:
        Notification.objects.filter(id=id).delete()
        return redirect(admin_notification)


@login_required
def add_staff(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
                return redirect(staff_list)

    return render(request, 'add_staff.html',locals())


@login_required
def staff_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    stf = User.objects.filter(user_type=2)
    staff_members = Staff.objects.all().order_by('-id')

    return render(request, 'staff_list.html', locals())


@login_required
def search_staff(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    searched = None
    staff_members = Staff.objects.all().order_by('-id')
    stf = User.objects.filter(user_type=2)
    if request.method == 'POST':
        s_data = request.POST.get('search')
        searched = Staff.objects.filter(
            Q(staff__name__icontains=s_data) |
            Q(designation__icontains=s_data) |
            Q(staff__phone_number__icontains=s_data) |
            Q(id__icontains=s_data)
        )

        return render(request, 'staff_list.html', locals())
    return render(request, 'staff_list.html', locals())


@login_required
def edit_staff(request, staff_id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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

        # User.objects.filter(id=staff_id).update(name=name,
        #                                         phone_number=phone_number)

        if username:
            instance.username = username
            instance.name = name
            instance.phone_number = phone_number
            instance.save()

        Staff.objects.filter(staff_id=staff_id).update(designation=designation,
                                                       staff_id=s_id,
                                                       experience=experience,
                                                       qualification=qualification)
        if image:
            profile.image = image
            profile.save()


        #notification generation

        staff_message = 'Your profile has been edited. do check it out.'
        Notification.objects.create(user=s_id,
                                    read=False,
                                    message=staff_message)

        admin = User.objects.get(id=1)
        for i in stf:
            name = i.name
            admin_message = 'You have edited {} profile successfully.'.format(name)
            Notification.objects.create(user=admin,
                                        read=False,
                                        message=admin_message)
        return redirect(staff_list)
    else:
        return render(request, 'edit_staff.html', locals())


@login_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, staff_id=staff_id)
    User.objects.filter(id=staff_id).delete()
    staff.delete()
    return redirect(staff_list)


@login_required
def create_admin_blog(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
        # notification
        client = User.objects.filter(user_type=3)
        client_message = "New blog uploaded '{}'".format(blog.title)
        for client_user in client:
            Notification.objects.create(user=client_user,
                                        read=False,
                                        message=client_message)
        return redirect(admin_blogs)
    else:
        return render(request, 'create_admin_blog.html', locals())


@login_required
def admin_blogs(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    item = Blog.objects.all().order_by('-date')

    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)

        admin_id = 1  # Assuming the admin user has id=1
        if blog.user_id == admin_id:
            return redirect('edit_admin_blog', blog_id=blog_id)
        else:
            staff_id = blog.user_id
            staff = get_object_or_404(User, id=staff_id)
            staff_message = f'You have a new blog edit request for "{blog.title}".'
            Notification.objects.create(user=staff, read=False, message=staff_message)

            admin = User.objects.get(id=admin_id)
            admin_message = f'You have requested {staff.username} to edit the blog "{blog.title}".'
            Notification.objects.create(user=admin, read=False, message=admin_message)

            return redirect('admin_blogs')
    return render(request, 'admin_blogs.html', locals())


@login_required
def search_ablog(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')

        searched = Blog.objects.filter(Q(title__icontains=s_data) |
                                       Q(description__icontains=s_data) |
                                       Q(user__username__icontains=s_data))

        return render(request, 'admin_blogs.html', locals())
    return render(request, 'admin_blogs.html', locals())


@login_required
def edit_admin_blog(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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


@login_required
def delete_item(request,id):
    Blog.objects.filter(id=id).delete()
    user = User.objects.get(id=request.user.id)
    if user.is_superuser == 1:
        return redirect(admin_blogs)
    else:
        return redirect(staff_blog)


@login_required
def admin_project_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    project = Project.objects.all().order_by('-last_updated')
    person = User.objects.all()
    return render(request, 'admin_project_list.html', locals())


@login_required
def search_aproject(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')
        searched = Project.objects.filter(
            Q(id__icontains=s_data) |
            Q(staff__name__icontains=s_data) |
            Q(client__name__icontains=s_data) |
            Q(status__icontains=s_data)
        ).select_related('staff', 'client')
        return render(request, 'admin_project_list.html', locals())
    return render(request, 'admin_project_list.html', locals())


@login_required
def admin_project_view(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    project = Project.objects.filter(id=id)
    person = User.objects.all()
    staff = Staff.objects.all()
    design = DesignPreference.objects.all()
    app = Appointment.objects.all()
    for i in app:
        for j in project:
            if i.client_id == j.client_id:
                address = i.address
    return render(request, 'admin_project_view.html', locals())


@login_required
def delete_project(request, id):
    Project.objects.filter(id=id).delete()
    return redirect(admin_project_list)


@login_required
def appointment_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    app1 = Appointment.objects.filter(status=1).order_by('-id')
    app2 = Appointment.objects.filter(status=2)
    client = User.objects.all()
    return render(request, 'appointment_list.html', locals())


@login_required
def appointment_view(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    client = User.objects.filter(id=id)
    app_t = Appointment.objects.all()
    for i in app_t:
        for j in client:
            if i.client_id == j.id:
                time = i.created_at
                app = Appointment.objects.filter(client_id=id, status=1, created_at=time)

    return render(request, 'appointment_view.html', locals())


@login_required
def schedule(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    app = Appointment.objects.filter(id=id)
    staff = User.objects.filter(is_staff=1, is_superuser=0)
    return render(request, 'schedule_appointment.html', locals())


@login_required
def schedule_appointment(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    app = Appointment.objects.filter(id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        user = User.objects.get(id=name)
        date = request.POST.get('date')
        time = request.POST.get('time')
        Appointment.objects.filter(id=id).update(staff_name=user, date=date, time=time, status=2)

        # notification to staff
        appoint = Appointment.objects.get(id=id)
        staff = appoint.staff_name
        # Format the date and time
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')

        time_obj = datetime.strptime(time, '%H:%M')
        formatted_time = time_obj.strftime('%I:%M %p')
        staff_message = 'You have new appointment scheduled on {} at {}'.format(formatted_date,formatted_time)
        Notification.objects.create(user=staff,
                                    read=False,
                                    message=staff_message)

        #send email
        clientdata = User.objects.filter(id=appoint.client_id)
        client_message = "Your appointment is scheduled on {} at {}. Please do login to your account using email as email/username and phone number as password. Thank you'".format(formatted_date,formatted_time)
        for i in clientdata:
            email = i.email
        appointment_email_to_client(email, client_message)

        return redirect(appointment_list)

#send email
def appointment_email_to_client(email, client_message):
    subject = "Appointment Scheduled"
    message = client_message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@login_required
def schedule_app_view(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    app = Appointment.objects.filter(id=id)
    client = User.objects.all()
    return render(request, 'schedule_app_view.html', locals())


@login_required
def reject_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = '4'
    appointment.save()

    # send email
    client = User.objects.filter(id=appointment.client_id)
    client_message = "Your appointment is rejected. Thank you."
    for i in client:
        email = i.email
    appointment_email_to_client(email, client_message)
    return redirect(appointment_list)


#send email
def reject_email_to_client(email, client_message):
    subject = "Appointment Rejected"
    message = client_message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@login_required
def services_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    services = Services.objects.all()
    return render(request, 'services.html', locals())


@login_required
def create_services(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:

            services = Services.objects.create(
                title=title,
                description=description,
                image=image,
            )
            services.save()
            return redirect(services_list)

        except Services.DoesNotExist:
            return redirect(services_list)

    else:
        return render(request, 'create_services.html', locals())


@login_required
def edit_services(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    services = Services.objects.filter(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            Services.objects.filter(id=id).update(
                title=title,
                description=description,
            )
            instance = get_object_or_404(Services, id=id)
            if image:
                instance.image = image
            instance.save()
            return redirect(services_list)

        except Services.DoesNotExist:
            return redirect(services_list)
    else:
        return render(request, 'edit_services.html', locals())

def delete_services(request, id):
    Services.objects.filter(id=id).delete()
    return redirect(services_list)

#staff module

@login_required
def staff_dashboard(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    client = Project.objects.filter(staff_id=user).count()
    ongoing = Project.objects.filter(staff_id=user, status=1).count()
    complete = Project.objects.filter(staff_id=user, status=3).count()
    app = Appointment.objects.filter(staff_name=user, status=2).order_by('-created_at')[:10]
    clnt = User.objects.all()

    return render(request, 'staff_dashboard.html', locals())


@login_required
def staff_notification(request):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    # Get the count of unread notifications
    unread_count = Notification.objects.filter(user=request.user, read=False).count()

    # Get all notifications for the current user, ordered by datetime
    notifications = Notification.objects.filter(user=request.user).order_by('-datetime')

    # Get the current time
    current_time = datetime.now()

    # Calculate time ago for each notification
    for notification in notifications:
        time_difference = current_time - notification.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            notification.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            notification.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            notification.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            notification.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            notification.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            notification.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            notification.time_ago = f"{weeks} weeks ago"

        # Mark the notification as read
        notification.read = True
        notification.save()
    return render(request, 'staff_notification.html', locals())


@login_required
def delete_notification(request,id):
    my_notify = Notification.objects.filter(user_id=request.user.id)
    if my_notify:
        Notification.objects.filter(id=id).delete()
        return redirect(staff_notification)


@login_required
def staff_appointments(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    client = User.objects.all()
    app = Appointment.objects.filter(staff_name_id=user, status=2).order_by('-id')
    return render(request, 'staff_appointments.html', locals())


@login_required
def search_app(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')

        searched = Appointment.objects.filter(staff_name=user, status=2).filter(Q(address__icontains=s_data) |
                                                                       Q(time__icontains=s_data) |
                                                                       Q(date__icontains=s_data))

        return render(request, 'staff_appointments.html', locals())
    return render(request, 'staff_appointments.html', locals())


@login_required
def staff_app_view(request, id, id1):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    client = User.objects.filter(id=id)
    app = Appointment.objects.filter(client_id=id, id=id1)
    return render(request, 'staff_app_view.html', locals())


@login_required
def staff_reject_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = '2'  # Assuming '2' indicates rejection
    appointment.save()

    # Get the staff and client names
    staff = User.objects.get(id=appointment.staff_name).username
    client = User.objects.get(id=appointment.client_id).name

    # Create the admin notification message
    admin = User.objects.get(id=1)
    admin_message = "{} rejected the appointment of {}".format(staff, client)
    Notification.objects.create(user=admin, read=False, message=admin_message)

    return redirect('staff_appointments')

def staff_blog(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    item = Blog.objects.filter(user_id=user).order_by('-id')

    return render(request, 'staff_blog.html', locals())


@login_required
def search_sblog(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')

        searched = Blog.objects.filter(user=user).filter(Q(title__icontains=s_data) | Q(description__icontains=s_data) | Q(date__icontains=s_data))

        return render(request, 'staff_blog.html', locals())
    return render(request, 'staff_blog.html', locals())


@login_required
def create_staff_blog(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
        #notification
        client = User.objects.filter(user_type=3)
        client_message = "New blog uploaded '{}'".format(blog.title)
        Notification.objects.create(user=client,
                                    read=False,
                                    message=client_message)
        return redirect(staff_blog)
    else:
        return render(request, 'create_staff_blog.html', locals())


@login_required
def edit_staff_blog(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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


@login_required
def project_schedule(request, id, id1):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    app = Appointment.objects.filter(client_id=id)
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    Appointment.objects.filter(id=id1).update(status=3)
    return render(request, 'project_schedule.html',locals())


@login_required
def project_form(request):
    staff = User.objects.filter(id=request.user.id)
    staf_f = User.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(staff_name=staf_f)
    design = DesignPreference.objects.all()
    for i in appointments:
        for j in design:
            if i.client_id == j.client_id:
                designid = j.id
                clientid = i.client_id

                if request.method == 'POST':
                    start_date = request.POST.get('start_date')
                    end_date = request.POST.get('end_date')
                    status = request.POST.get('status')
                    comment = request.POST.get('comment')

                    project = Project.objects.create(
                        starting_date=start_date,
                        ending_date=end_date,
                        status=status,
                        comment=comment,
                        staff=staf_f,
                        client_id=clientid,
                        design_id=designid,
                    )
                    project.save()

                    #notification
                    admin = User.objects.get(id=1)
                    client = User.objects.get(id=clientid)
                    admin_message = "{} has accepted the appointment of {}".format(staf_f.name, client.name)
                    Notification.objects.create(user=admin,
                                                read=False,
                                                message=admin_message)

                    client = User.objects.get(id=clientid)

                    client_message = "Your project has been accepted"
                    Notification.objects.create(user=client,
                                                read=False,
                                                message=client_message)
                    return redirect(staff_project_list)
                else:
                    return render(request, 'staff_appointments.html', locals())
    return render(request, 'staff_appointments.html', locals())


@login_required
def staff_project_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    person = User.objects.all()
    project = Project.objects.filter(staff_id=request.user.id).exclude(status=3).order_by('last_updated')
    return render(request, 'staff_project_list.html', locals())


@login_required
def search_sproject(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')
        searched = Project.objects.filter(
            Q(id__icontains=s_data) |
            Q(ending_date__icontains=s_data) |
            Q(client__name__icontains=s_data))
        return render(request, 'staff_project_list.html', locals())
    return render(request, 'staff_project_list.html', locals())


@login_required
def staff_project_view(request, id, id1):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    project = Project.objects.filter(id=id1)
    client = User.objects.filter(id=id)
    design = DesignPreference.objects.filter(client_id=id)
    app = Appointment.objects.all()
    for i in app:
        for j in project:
            if i.client_id == j.client_id:
                address = i.address
    return render(request, 'staff_project_view.html', locals())


@login_required
def staff_project_update(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    project = Project.objects.filter(id=id)
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    return render(request, 'staff_project_update.html', locals())


@login_required
def project_form_update(request, id):
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        end_date = request.POST.get('end_date')
        category = request.POST.get('category')
        actual_budget = request.POST.get('actual_budget')
        mainimage = request.FILES.get('mainimage')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        image5 = request.FILES.get('image5')
        image6 = request.FILES.get('image6')
        image7 = request.FILES.get('image7')

        if end_date == '':
            project.end_date = None
        else:
            project.end_date = end_date

        if status:
            project.status = status

        if category:
            project.category = category

        project.title = title
        project.description = description
        project.comment = comment
        project.actual_budget = actual_budget

        if mainimage:
            project.mainimage = mainimage
        if image1:
            project.image1 = image1
        if image2:
            project.image2 = image2
        if image3:
            project.image3 = image3
        if image4:
            project.image4 = image4
        if image5:
            project.image5 = image5
        if image6:
            project.image6 = image6
        if image7:
            project.image7 = image7

        project.save()

        # Notification
        client = project.client_id
        client_message = f'Your project i.e id number "{project.id}" has been updated.'
        Notification.objects.create(user_id=client, read=False, message=client_message, datetime=timezone.now())

        admin = User.objects.get(id=1)
        admin_message = f'Project id "{project.id}" has been updated.'
        Notification.objects.create(user=admin, read=False, message=admin_message, datetime=timezone.now())

        return redirect('staff_project_view', id=project.client_id, id1=project.id)
    else:
        return redirect('staff_project_update', id=id)


@login_required
def staff_myproject_list(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    person = User.objects.all()
    app = Appointment.objects.all()
    project = Project.objects.filter(staff_id=request.user.id, status=3).order_by('last_updated')
    for i in app:
        for j in project:
            if i.client_id == j.client_id:
                address = i.address
    return render(request, 'staff_myproject_list.html', locals())


@login_required
def search_myproject(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    searched = None
    if request.method == 'POST':
        s_data = request.POST.get('search')
        searched = Project.objects.filter(staff_id=user, status=3).filter(
            Q(id__icontains=s_data) |
            Q(title__icontains=s_data) |
            Q(description__icontains=s_data) |
            Q(client__name__icontains=s_data))
        app = Appointment.objects.all()
        for i in app:
            for j in searched:
                if i.client_id == j.client_id:
                    address = i.address
        return render(request, 'staff_myproject_list.html', locals())
    return render(request, 'staff_myproject_list.html', locals())


@login_required
def staff_myproject_view(request, id):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    project = Project.objects.filter(id=id)
    person = User.objects.all()
    design = DesignPreference.objects.all()
    app = Appointment.objects.all()
    for i in app:
        for j in project:
            if i.client_id == j.client_id:
                address = i.address
    return render(request, 'staff_myproject_view.html', locals())


@login_required
def staff_profile(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
    user = User.objects.get(id=request.user.id)
    staff = Staff.objects.filter(staff_id=user)
    details = User.objects.filter(id=request.user.id)
    return render(request, 'staff_profile.html', locals())


@login_required
def request_update(request):
    user = User.objects.get(id=request.user.id)
    admin = User.objects.get(id=1)
    # Send notification to admin
    admin_message = "{} requested for profile updation!".format(user.name)
    Notification.objects.create(user=admin, read=False, message=admin_message)
    # Send notification to staff
    staff_message = 'Your request for profile updation sent to admin.'
    Notification.objects.create(user=user,
                                read=False,
                                message=staff_message)
    return redirect(staff_profile)


#client side

@login_required
def client_profile(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    user = User.objects.get(id=request.user.id)
    client = User.objects.filter(id=request.user.id)
    design = DesignPreference.objects.filter(client_id=user)
    return render(request, 'client_profile.html', locals())


@login_required
def design_preference(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        style = request.POST.get('style')
        color_palette = request.POST.get('color_palette')
        materials = request.POST.get('materials')
        budget = request.POST.get('budget')
        layout = request.POST.get('layout')
        other_layout = request.POST.get('other_layout')

        if layout == 'Other':
            layout = other_layout

        try:
            design = DesignPreference.objects.create(
                client_id=request.user.id,
                style=style,
                color_palette=color_palette,
                materials=materials,
                layout=layout,
                budget=budget)
            design.save()
            app = Appointment.objects.all()
            staff = Staff.objects.all()
            for i in design:
                for j in app:
                    if i.client_id == j.client_id:
                        staff_id = j.staff_name_id
                        client_name = user.name
                        staff_message = '{} has submitted a Design preference'.format(client_name)
                        Notification.objects.create(user=staff_id, read=False, message=staff_message)

                        return redirect(client_profile)
        except DesignPreference.DoesNotExist:
            return render(request, 'design_preference.html',locals())
    else:
        return render(request, 'design_preference.html', locals())


@login_required
def delete_design_preference(request, id):
    DesignPreference.objects.filter(id=id).delete()
    return redirect(client_profile)



@login_required
def project_updates(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    user = User.objects.get(id=request.user.id)
    project = Project.objects.filter(client_id=user)
    staff = User.objects.all()
    return render(request, 'project_updates.html', locals())



@login_required
def client_notification(request):
    # Get the count of unread notifications
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()
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
    return render(request, 'client_notification.html', locals())


@login_required
def delete_client_notification(request,id):
    my_notify = Notification.objects.filter(user_id=request.user.id)
    if my_notify:
        Notification.objects.filter(id=id).delete()
        return redirect(client_notification)


@login_required
def client_review(request):
    unread_count = Notification.objects.filter(user=request.user.id, read=False).count()

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        comments = Comment.objects.create(
            comment=comment,
            rating=rating,
            client_id=request.user.id,
        )
        comments.save()

        # notification
        admin = User.objects.get(id=1)
        client_id = User.objects.get(id=request.user.id)
        admin_message = "{} has sent a review".format(client_id.name)
        Notification.objects.create(user=admin,
                                    read=False,
                                    message=admin_message)

        client_message = "Your review has been sent"
        Notification.objects.create(user=client_id,
                                    read=False,
                                    message=client_message)
        return redirect(client_review)
    else:
        return render(request, 'client_comment.html', locals())