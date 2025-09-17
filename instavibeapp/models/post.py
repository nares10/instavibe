from django.db import models
from django.contrib.auth.models import User

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

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()
