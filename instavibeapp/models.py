from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.jpeg')
    bio = models.TextField(blank=True, max_length=500)
    # --- New Fields ---
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
    


# Signals to create/save Profile for every new User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
