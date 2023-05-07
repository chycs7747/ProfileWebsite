from django.urls import path, include
from .views import main_views, profile_views, document_views
from google_oauth.views import login_views as google_login
from github_oauth.views import login_views as github_login
from user import views as user_views

app_name = 'yunho'

urlpatterns = [
    #main_views.py
    path('', main_views.index, name="main_index"),
    #profile
    path('profile/', profile_views.index, name="profile_index"),
    #document
    path('document/', document_views.index, name="document_index"),

    #Google
    path('login/google/', google_login.GoogleOauthLogin.google_login , name="google_login" ),
    path('login/google/callback', google_login.GoogleOauthLogin.google_callback, name="google_callback"),
    #Github
    path('login/github/', github_login.GithubOauthLogin.github_login , name="github_login" ),
    path('login/github/callback', github_login.GithubOauthLogin.github_callback, name="github_callback"),
    #user
    path('sign_in/', user_views.DkuLogin.sign_in , name="sign_in"),
    path('sign_up/', user_views.DkuLogin.sign_up, name="sign_up"),
    path('sign_out/', user_views.DkuLogin.sign_out, name="sign_out")
]