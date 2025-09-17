from django.db import models
from django.contrib.auth.models import User
from .follow import Follow

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpeg')
    bio = models.TextField(blank=True, max_length=500)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=50,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
            ('Prefer not to say', 'Prefer not to say')
        ],
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    def followers_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()

    def is_following_to(self, user):
        return Follow.objects.filter(follower=self.user, following=user).exists()

    def is_follower_of(self, user):
        return Follow.objects.filter(follower=user, following=self.user).exists()

