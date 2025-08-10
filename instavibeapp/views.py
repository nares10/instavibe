import re
from django.shortcuts import render,reverse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ProfileForm
from .models import Post, Like, Comment, Follow


def home_view(request):
    return render(request, 'instavibeapp/home.html', {'repeat_list': range(10)})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('instavibeapp:home')  
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'instavibeapp/login.html')


def register_view(request):

    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein",
        "trustno1", "dragon", "baseball", "111111", "iloveyou", "adobe123", "123123", "admin",
        "123456789", "1234567890", "1234", "sunshine", "welcome", "login", "solo", "photoshop",
        "1qaz2wsx", "mustang", "access", "flower", "starwars", "shadow", "passw0rd", "master",
        "654321", "555555", "lovely", "7777777", "!@#$%^&*", "888888", "password1", "superman",
        "prince", "qwertyuiop", "696969", "hottie", "freedom", "hello", "charlie", "aa123456",
        "azerty", "whatever", "donald", "batman", "zaq1zaq1", "qazwsx", "000000", "123qwe"
    ]


    def is_strong_password(password):
        # At least 8 characters
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        # Must contain uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit."
        if not re.search(r'[^\w\s]', password):  # special char
            return False, "Password must contain at least one special character."

        # Check against common passwords
        if password.lower() in COMMON_PASSWORDS:
            return False, "Password is too common. Please choose a stronger password."

        return True, ""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if len(username) < 3 or len(username) > 50:
            messages.error(request, "Username must be between 3 and 50 characters.")
            return redirect('instavibeapp:register')
        
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            messages.error(request, "Username can only contain letters, numbers, underscores, and hyphens.")
            return redirect('instavibeapp:register')
        
        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('instavibeapp:register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('instavibeapp:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('instavibeapp:register')
        
        is_valid, error_message = is_strong_password(password)
        if not is_valid:
            messages.error(request, error_message)
            return redirect('instavibeapp:register')
        
        if len(username) < 3 or len(username) > 50:
            messages.error(request, "Username must be between 3 and 50 characters.")
            return redirect('instavibeapp:register')
        
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            messages.error(request, "Username can only contain letters, numbers, underscores, and hyphens.")
            return redirect('instavibeapp:register')

        # Create user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('instavibeapp:login')
    
    return render(request, 'instavibeapp/register.html')


def logout_view(request):
    logout(request)
    return redirect('instavibeapp:login')


def test_view(request):
    return render(request, 'instavibeapp/test.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    posts = Post.objects.filter(owner=request.user).prefetch_related('likes', 'comments').order_by('-created_at')
    viewing_user = request.user
    
    # Get is_following status if viewing other's profile
    is_following = profile.is_following(viewing_user) if viewing_user != profile.user else False
    
    return render(request, 'instavibeapp/profile.html', {
        'profile': profile,
        'posts': posts,
        'is_following': is_following
    })
    


@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        image = request.FILES.get('image')
        date_of_birth = request.POST.get('date_of_birth', None)
        gender = request.POST.get('gender', '')

        profile.bio = bio
        if image:
            profile.image = image
        profile.date_of_birth = date_of_birth if date_of_birth else None
        profile.gender = gender
        profile.save()
        return redirect('instavibeapp:profile')
    return render(request, 'instavibeapp/edit_profile.html', {'profile': profile})

@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        
        if image:
            post = Post.objects.create(
                owner=request.user,
                image=image,
                caption=caption
            )
            messages.success(request, "Post created successfully!")
            return redirect('instavibeapp:profile')
        else:
            messages.error(request, "Image is required!")
    
    return render(request, 'instavibeapp/create_post.html')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        post.caption = caption
        post.save()
        messages.success(request, "Post updated successfully!")
        return redirect('instavibeapp:profile')
    
    return render(request, 'instavibeapp/edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('instavibeapp:profile')
    
    return render(request, 'instavibeapp/delete_post.html', {'post': post})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    
    if like:
        # User already liked the post, so unlike it
        like.delete()
        is_liked = False
    else:
        # User hasn't liked the post, so create a like
        Like.objects.create(user=request.user, post=post)
        is_liked = True
    
    return JsonResponse({
        'status': 'success',
        'is_liked': is_liked,
        'likes_count': post.likes_count
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )
            messages.success(request, "Comment added successfully!")
            # Redirect to profile with post ID in fragment identifier
            return redirect(f'{reverse("instavibeapp:profile")}#post-{post_id}')
        else:
            messages.error(request, "Comment cannot be empty!")
            
    return redirect(f'{reverse("instavibeapp:profile")}#post-{post_id}')

@login_required
def view_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    return render(request, 'instavibeapp/comments.html', {
        'post': post,
        'comments': comments
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post_id = comment.post.id
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('instavibeapp:view_comments', post_id=post_id)

# Add new views

@login_required
@require_POST
def follow_unfollow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if user_to_follow == request.user:
        return JsonResponse({
            'status': 'error',
            'message': 'You cannot follow yourself'
        })
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True
    
    return JsonResponse({
        'status': 'success',
        'is_following': is_following,
        'followers_count': user_to_follow.profile.followers_count(),
        'following_count': user_to_follow.profile.following_count()
    })

@login_required
def followers_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.followers.all().select_related('follower__profile')
    
    # Create a dictionary of following status for each follower
    following_status = {
        follow.follower.id: request.user.profile.is_following(follow.follower)
        for follow in followers
    }
    
    return render(request, 'instavibeapp/followers_list.html', {
        'user_profile': user.profile,
        'followers': followers,
        'following_status': following_status
    })

@login_required
def following_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = user.following.all().select_related('following__profile')
    return render(request, 'instavibeapp/following_list.html', {
        'user_profile': user.profile,
        'following': following
    })