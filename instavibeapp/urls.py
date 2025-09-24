from django.urls import path
from . import views 

app_name = 'instavibeapp'
urlpatterns = [

    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_view, name='test'),

    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    
    #Explore Page:
    path("explore/", views.explore_view, name='explore'),
    #Feed
    path("feed/", views.feed_view, name="feed"),

    # Profile-related
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('<str:username>/following-list/', views.following_list, name='following_list'),
    path('<str:username>/follower-list/', views.followers_list, name='followers_list'),
    path('<str:username>/', views.profile_view, name='profile'),

    # Posts
    path('post/create/', views.create_post, name='create_post'),
    path('post/<str:encoded_post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<str:encoded_post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<str:encoded_post_id>/like/', views.like_post, name='like_post'),
    path('post/<str:encoded_post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<str:encoded_post_id>/comments/', views.view_comments, name='view_comments'),

    # Comments
    path('comment/<str:encoded_comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Follow system
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),

]
