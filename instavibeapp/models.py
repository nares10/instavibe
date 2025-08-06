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

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Show newest posts first

    def __str__(self):
        return f"Post by {self.owner.username} on {self.created_at.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        # Delete old image if it's being updated
        try:
            old_post = Post.objects.get(id=self.id)
            if old_post.image != self.image:
                old_post.image.delete(save=False)
        except Post.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete image file when post is deleted
        self.image.delete(save=False)
        super().delete(*args, **kwargs)
    
        
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s comment on {self.post}"