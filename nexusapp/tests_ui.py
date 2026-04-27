"""
UI Tests for Nexus Application
Tests user interface interactions using Django test client and forms
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Profile, Follow, Notification


class UIAuthenticationTests(TestCase):
    """Test authentication UI flows"""
    
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "TestPass123!"
        self.email = "test@example.com"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
    
    def test_registration_page_loads(self):
        """Test registration page is accessible"""
        response = self.client.get(reverse('nexusapp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/register.html')
        self.assertIn('form', response.context)
    
    def test_user_registration_flow(self):
        """Test complete user registration flow"""
        response = self.client.post(reverse('nexusapp:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        # Should redirect to login after successful registration
        self.assertEqual(response.status_code, 302)
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_page_loads(self):
        """Test login page is accessible"""
        response = self.client.get(reverse('nexusapp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/login.html')
    
    def test_user_login_flow(self):
        """Test complete user login flow"""
        response = self.client.post(reverse('nexusapp:login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('nexusapp:home'))
        # Verify user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_with_invalid_credentials(self):
        """Test login fails with wrong credentials"""
        response = self.client.post(reverse('nexusapp:login'), {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/login.html')
    
    def test_logout_flow(self):
        """Test user logout"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('nexusapp:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('nexusapp:home'))


class UIProfileTests(TestCase):
    """Test profile UI interactions"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='TestPass123!')
    
    def test_profile_page_loads(self):
        """Test profile page is accessible"""
        response = self.client.get(
            reverse('nexusapp:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/profile.html')
        self.assertEqual(response.context['user_obj'].username, self.user.username)
    
    def test_edit_profile_page_loads(self):
        """Test edit profile page is accessible"""
        response = self.client.get(reverse('nexusapp:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/edit_profile.html')
    
    def test_edit_profile_updates_bio(self):
        """Test updating profile bio"""
        image = SimpleUploadedFile(
            name='profile.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('nexusapp:edit_profile'), {
            'bio': 'Updated bio',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
    
    def test_home_feed_loads(self):
        """Test home feed page loads"""
        response = self.client.get(reverse('nexusapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/home.html')


class UIPostTests(TestCase):
    """Test post creation and interaction UI"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='TestPass123!')
    
    def test_create_post_page_loads(self):
        """Test create post page is accessible"""
        response = self.client.get(reverse('nexusapp:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/create_post.html')
    
    def test_create_post_flow(self):
        """Test creating a new post"""
        image = SimpleUploadedFile(
            name='post.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('nexusapp:create_post'), {
            'caption': 'Test post caption',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        # Verify post was created
        self.assertTrue(Post.objects.filter(caption='Test post caption').exists())
    
    def test_post_detail_page_loads(self):
        """Test post detail page"""
        image = SimpleUploadedFile(
            name='post.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        post = Post.objects.create(
            owner=self.user,
            caption='Test post',
            image=image
        )
        response = self.client.get(
            reverse('nexusapp:post_detail', args=[post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/post_detail.html')
        self.assertEqual(response.context['post'].id, post.id)
    
    def test_edit_post_page_loads(self):
        """Test edit post page"""
        image = SimpleUploadedFile(
            name='post.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        post = Post.objects.create(
            owner=self.user,
            caption='Test post',
            image=image
        )
        response = self.client.get(
            reverse('nexusapp:edit_post', args=[post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/edit_post.html')
    
    def test_delete_post_flow(self):
        """Test deleting a post"""
        image = SimpleUploadedFile(
            name='post.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        post = Post.objects.create(
            owner=self.user,
            caption='Test post',
            image=image
        )
        response = self.client.post(
            reverse('nexusapp:delete_post', args=[post.id])
        )
        self.assertEqual(response.status_code, 302)
        # Verify post was deleted
        self.assertFalse(Post.objects.filter(id=post.id).exists())


class UIFollowTests(TestCase):
    """Test follow/unfollow UI interactions"""
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)
        self.client.login(username='user1', password='TestPass123!')
    
    def test_follow_user_flow(self):
        """Test following a user"""
        response = self.client.post(
            reverse('nexusapp:follow', args=[self.user2.username])
        )
        self.assertEqual(response.status_code, 302)
        # Verify follow relationship was created
        self.assertTrue(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )
    
    def test_unfollow_user_flow(self):
        """Test unfollowing a user"""
        Follow.objects.create(follower=self.user1, following=self.user2)
        response = self.client.post(
            reverse('nexusapp:unfollow', args=[self.user2.username])
        )
        self.assertEqual(response.status_code, 302)
        # Verify follow relationship was deleted
        self.assertFalse(
            Follow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )
    
    def test_view_followers_page(self):
        """Test viewing followers list"""
        response = self.client.get(
            reverse('nexusapp:followers', args=[self.user1.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/followers_list.html')
    
    def test_view_following_page(self):
        """Test viewing following list"""
        response = self.client.get(
            reverse('nexusapp:following', args=[self.user1.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/following_list.html')


class UIInteractionTests(TestCase):
    """Test like and comment interactions"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user)
        image = SimpleUploadedFile(
            name='post.jpg',
            content=b'image_content',
            content_type='image/jpeg'
        )
        self.post = Post.objects.create(
            owner=self.user,
            caption='Test post',
            image=image
        )
        self.client.login(username='testuser', password='TestPass123!')
    
    def test_like_post_flow(self):
        """Test liking a post"""
        response = self.client.post(
            reverse('nexusapp:like_post', args=[self.post.id])
        )
        # Check for redirect or JSON response
        self.assertIn(response.status_code, [200, 302])
        # Verify like was created
        self.assertTrue(
            self.post.like_set.filter(user=self.user).exists()
        )
    
    def test_comment_on_post_flow(self):
        """Test commenting on a post"""
        response = self.client.post(
            reverse('nexusapp:comment', args=[self.post.id]),
            {'body': 'Great post!'}
        )
        self.assertIn(response.status_code, [200, 302])
        # Verify comment was created
        self.assertTrue(
            self.post.comment_set.filter(user=self.user, body='Great post!').exists()
        )


class UIExploreTests(TestCase):
    """Test explore/discovery UI"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='TestPass123!')
    
    def test_explore_page_loads(self):
        """Test explore page is accessible"""
        response = self.client.get(reverse('nexusapp:explore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/explore.html')
    
    def test_notifications_page_loads(self):
        """Test notifications page is accessible"""
        response = self.client.get(reverse('nexusapp:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nexusapp/notifications.html')


# Run tests with: python manage.py test nexusapp.tests_ui
# Run specific test: python manage.py test nexusapp.tests_ui.UIAuthenticationTests
# Run with verbose output: python manage.py test nexusapp.tests_ui -v 2
