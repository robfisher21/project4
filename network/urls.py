
from django.urls import path, include
import debug_toolbar
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.all_posts, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.all_posts, name="allposts"),
    path("createpost", views.create_post, name="create_post"),
    path("updatepost/<int:post_id>", views.update_post, name="update_post"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("updatefollowers/<str:profile>", views.updatefollowers, name="updatefollowers"),
    path('__debug__/', include(debug_toolbar.urls))
]
