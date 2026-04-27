from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow, Notification
from .utils import encode_id 
from channels.testing import WebsocketCommunicator
from nexus.asgi import application


# ---------------- Base setup mixin ----------------
class BaseSetupMixin:
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "Testpass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.post = Post.objects.create(owner=self.user, caption="Test post", image=image)


# ---------------- Auth related views ----------------
class AuthViewsTestCase(BaseSetupMixin, TestCase):
    def test_login_view_post_success(self):
        response = self.client.post(reverse('nexusapp:login'),{
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('nexusapp:home'))

    def test_register_view_get(self):
        response = self.client.get(reverse('nexusapp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/register.html')

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('nexusapp:logout'))
        self.assertEqual(response.status_code, 302)


# ---------------- Profile related views ----------------
class ProfileViewsTestCase(BaseSetupMixin, TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('nexusapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/home.html')

    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('nexusapp:profile', args=[self.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/profile.html')

    def test_edit_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('nexusapp:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/edit_profile.html')


# ---------------- Post related views ----------------
class PostViewsTestCase(BaseSetupMixin, TestCase):
    def test_create_post_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('nexusapp:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/create_post.html')

    def test_edit_post_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('nexusapp:edit_post', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/edit_post.html')

    def test_delete_post_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('nexusapp:delete_post', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/delete_post.html')


# ---------------- Comment related views ----------------
class CommentViewsTestCase(BaseSetupMixin, TestCase):
    def test_view_comments(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.get(reverse('nexusapp:view_comments', args=[encoded_post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/comments.html')

    def test_add_comment_view(self):
        self.client.login(username=self.username, password=self.password)
        encoded_post_id = encode_id(self.post.id)
        response = self.client.post(reverse('nexusapp:add_comment', args=[encoded_post_id]), {
            'text': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.post.comments.filter(text='This is a test comment').exists())

    def test_delete_comment_view(self):
        self.client.login(username=self.username, password=self.password)
        comment = Comment.objects.create(user=self.user, post=self.post, text='To be deleted')
        encoded_comment_id = encode_id(comment.id)
        response = self.client.get(reverse('nexusapp:delete_comment', args=[encoded_comment_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())


# ---------------- Notification tests ----------------
class NotificationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.post = Post.objects.create(owner=self.user1, image='test.jpg')

    def test_like_generates_notification(self):
        Like.objects.create(user=self.user2, post=self.post)
        notif = Notification.objects.filter(receiver=self.user1, type='like').first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.sender, self.user2)
        self.assertEqual(notif.post, self.post)

    def test_comment_generates_notification(self):
        Comment.objects.create(user=self.user2, post=self.post, text="Nice post!")
        notif = Notification.objects.filter(receiver=self.user1, type='comment').first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.sender, self.user2)
        self.assertEqual(notif.post, self.post)

    def test_follow_generates_notification(self):
        Follow.objects.create(follower=self.user2, following=self.user1)
        notif = Notification.objects.filter(receiver=self.user1, type='follow').first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.sender, self.user2)

    def test_notifications_delivered_in_order(self):
        Like.objects.create(user=self.user2, post=self.post)
        Comment.objects.create(user=self.user2, post=self.post, text="Hi")
        Follow.objects.create(follower=self.user2, following=self.user1)
        notif_types = list(Notification.objects.filter(receiver=self.user1)
                           .order_by('created_at')
                           .values_list('type', flat=True))
        self.assertEqual(notif_types, ['like', 'comment', 'follow'])

    async def test_websocket_receives_pending_notifications(self):
        Like.objects.create(user=self.user2, post=self.post)
        Comment.objects.create(user=self.user2, post=self.post, text="Hi")
        communicator = WebsocketCommunicator(application, f"/ws/notifications/{self.user1.id}/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        received1 = await communicator.receive_json_from()
        received2 = await communicator.receive_json_from()
        types = {received1["type"], received2["type"]}
        self.assertIn("like", types)
        self.assertIn("comment", types)
        await communicator.disconnect()
