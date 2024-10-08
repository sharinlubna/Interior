from django.db import models

from django.contrib.auth.models import AbstractUser



# Create your models here.
userchoices = [
    (1, "Admin"),
    (2, "Employee"),
    (3, "Client")
]

status = [
    (1, "Pending"),
    (2, "Scheduled"),
    (3, "Accepted"),
    (4, "Rejected")
]

STATUS_CHOICES = [
        (1, 'In Progress'),
        (2, 'On Hold'),
        (3, 'Completed')
    ]

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    user_type = models.IntegerField(default=1, choices=userchoices)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username



class Staff(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_profile')
    designation = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

class Appointment(models.Model):
    date = models.CharField(max_length=10, null=True, blank=True)
    time = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    staff_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_staff', null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_client', default=1)  # Set a valid default
    status = models.IntegerField(default=1, choices=status)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Blog(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True, upload_to="images/")
    exp = models.TextField(null=True, blank=True)


class Notification(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Contact(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class DesignPreference(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_profile')
    style = models.CharField(max_length=50, null=True, blank=True)
    color_palette = models.CharField(max_length=50, null=True, blank=True)
    materials = models.CharField(max_length=50, null=True, blank=True)
    budget = models.CharField(max_length=50, null=True, blank=True)
    layout =models.CharField(max_length=50, null=True, blank=True, default='3 BHK')

    def __str__(self):
        return self.style

class Project(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='1')
    design = models.ForeignKey(DesignPreference, on_delete=models.CASCADE, related_name='design_as_client')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_as_staff', null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_as_client', default=1)
    starting_date = models.DateField(null=True, blank=True)
    ending_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    actual_budget = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    mainimage = models.ImageField(null=True, blank=True, upload_to="images/")
    image1 = models.ImageField(null=True, blank=True, upload_to="images/")
    image2 = models.ImageField(null=True, blank=True, upload_to="images/")
    image3 = models.ImageField(null=True, blank=True, upload_to="images/")
    image4 = models.ImageField(null=True, blank=True, upload_to="images/")
    image5 = models.ImageField(null=True, blank=True, upload_to="images/")
    image6 = models.ImageField(null=True, blank=True, upload_to="images/")
    image7 = models.ImageField(null=True, blank=True, upload_to="images/")


class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

class Services(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Subscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email