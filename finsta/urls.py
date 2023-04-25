"""finsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("profiles/<int:pk>/change/",views.ProfileEditView.as_view(),name="profile-edit"),
    path("posts/<int:pk>/like/",views.add_like_view, name="addlike"),
    path("posts/<int:pk>/comment/add/",views.add_comment_view,name="addcomment"),
    path("comments/<int:pk>/remove/",views.comment_remove_View,name="removecomment"),
    path("profile/<int:pk>/details/",views.Profile_detail_View.as_view(),name="profiledetail"),
    path("profile/<int:pk>/coverpic/change/",views.Update_Coverpic_View,name="coverpic-change"),
    path("profile/<int:pk>/propic/change/",views.Update_profilepic_view,name="profilepic-change"),
    path("profile/list/",views.ProfileListView.as_view(),name="profile-list"),
    path("profile/<int:pk>/follow/",views.followView,name="follow"),
    path("profile/<int:pk>/unfollow/",views.unfollowView,name="unfollow"),
    path("logout/",views.SignOutView,name="signout")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
