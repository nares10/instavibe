from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from .utils import encode_id  # Make sure your encode_id function is imported


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "Testpass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.post = Post.objects.create(owner=self.user, caption="Test post", image=image)

    def test_home_view(self):
        response = self.client.get(reverse('instavibeapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/home.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('instavibeapp:login'),{
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('instavibeapp:home'))

    def test_login_view_post(self):
        response = self.client.post(reverse('instavibeapp:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success

    def test_register_view_get(self):
        response = self.client.get(reverse('instavibeapp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/register.html')

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('instavibeapp:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('instavibeapp:profile', args=[self.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/profile.html')

    def test_edit_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('instavibeapp:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/edit_profile.html')

    def test_create_post_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('instavibeapp:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/create_post.html')

    def test_edit_post_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('instavibeapp:edit_post', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/edit_post.html')

    def test_delete_post_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('instavibeapp:delete_post', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/delete_post.html')

    def test_view_comments(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('instavibeapp:view_comments', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instavibeapp/comments.html')

    def test_add_comment_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.post(reverse('instavibeapp:add_comment', args=[encoded_post_id]), {
            'text': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding comment
        self.assertTrue(self.post.comments.filter(text='This is a test comment').exists())

    def test_delete_comment_view(self):
        self.client.login(username=self.username, password=self.password)
        comment = Comment.objects.create(user=self.user, post=self.post, text='To be deleted')
        encoded_comment_id = encode_id(comment.id)
        response = self.client.get(reverse('instavibeapp:delete_comment', args=[encoded_comment_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())