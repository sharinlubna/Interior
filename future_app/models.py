from django.db import models

from django.contrib.auth.models import AbstractUser



# Create your models here.
userchoices = (
    (1,"Admin"),
    (2,"Employee"),
    (3,"Client")
)

# designationchoices = (
#     (1, "Architect"),
#     (2, "Interior Designer"),
#     (3, "Project Manager"),
#     (4, "Design Consultant"),
#     (5, "Draftsperson"),
#     (6, "Lighting Designer"),
#     (7, "Furniture Designer"),
#     (8, "Materials Specialist"),
#     (9, "3D Visualizer"),
#     (10, "Site Supervisor"),
#     (11, "Procurement Manager"),
#     (12, "Client Relations Manager"),
#     (13, "Junior Interior Designer"),
#     (14, "Senior Interior Designer"),
#     (15, "Administrative Assistant")
# )

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
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


