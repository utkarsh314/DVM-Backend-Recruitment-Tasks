from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    bio = models.CharField(max_length=200, blank=True)
    following = models.ManyToManyField(User, blank=True, related_name='followers', default=None)
    emailupdate = models.ManyToManyField(User, blank=True, related_name='notifs', default=None)

    def __str__(self):
        return f"{self.user.username}'s Profile"