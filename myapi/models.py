from django.db import models
from django.contrib.auth.models import AbstractUser

class UserManagement(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    is_superuser_login = models.BooleanField(default=False)




    def __str__(self):
        return self.username


class Leavemanagement(models.Model):
    CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    user = models.ForeignKey(UserManagement, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, blank=False, null=False)
    startdate = models.DateField()
    enddate = models.DateField()
    choice = models.CharField(max_length=10, choices=CHOICES, default='Pending')
    def __str__(self):
        return self.user.username + ' - ' + self.choice