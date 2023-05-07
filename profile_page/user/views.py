#setting
from django.shortcuts import render, redirect
from config import settings
from django.conf import settings

#import session model
from django.utils import timezone
from django.contrib.sessions.models import Session

#import github, google service
from google_oauth.views import service_views as google_service_views
from github_oauth.views import service_views as github_service_views

#import user model
from user import models as UserModel

#import djanho's login system
from django.contrib.auth import authenticate, login, logout



class DkuLogin:
    def sign_in(request):
        
        #user_manager = UserModel.UserManager() 직접 만들어서 사용 권장되지 않음 -> username 필드 인식을 못함
        #user_manager.test()
        print("체크:", request.session['check'])
        print(request.session['access_token'])
        access_token = request.session['access_token']
        print(request.session['refresh_token'])
        
        
        try:
            user_info = google_service_views.GoogleService.google_get_user_info(access_token)
            profile_data = {
                'email': user_info['email'], #쓰임
                'username': user_info.get('name', ''), #쓰임
                'path': "google",
            }
        except:
            user_info = github_service_views.GithubService.github_get_user_info(access_token)
            profile_data = {
                'email': "https://github.com/"+user_info['login'], #쓰임
                'username': user_info['login'], #쓰임
                'path': "google",
            }
            
        try:
            user = UserModel.User.objects.get(email = profile_data['email'])
            request.session['create_time'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

            SessionStorage.rm_duplicated_session(user.email)


            request.session['email'] = user.email

            print(profile_data['email'],"- 사용자 존재\n유저명:",profile_data['username'])
            print("유저이름:",user.username,"유저비번:",user.password)
            print(request.session['email'])


            return redirect('https://opensource-egynk.run.goorm.site/yunho/')
        
          
            
        except UserModel.User.DoesNotExist:
            print("회원가입 진행 필요 email:",profile_data['email'],"username:",profile_data['username'] )
            return render(request, 'user/sign_up.html')
        
    def sign_up(request):
        print("Here is signup method!")
        if request.method == "POST":
            print(request.POST['job'])
            print(request.POST['gender'])
            
            job = request.POST['job']
            gender = request.POST['gender']
        
        
            access_token = request.session['access_token']
            
            try:
                user_info = google_service_views.GoogleService.google_get_user_info(access_token)
                profile_data = {
                    'email': user_info['email'], #쓰임
                    'username': user_info.get('name', ''), #쓰임
                    'path': "google",
                }
            except:
                user_info = github_service_views.GithubService.github_get_user_info(access_token)
                profile_data = {
                    'email': "https://github.com/"+user_info['login'], #쓰임
                    'username': user_info['login'], #쓰임
                    'path': "google",
                }
            user = UserModel.User.objects.create_user(email = profile_data['email'], username = profile_data['username'])
            print("user저장 완료")
            profile = UserModel.Profile.objects.create(user=user, job=job, gender=gender)
            print("profile저장 완료")

        
        return redirect('https://opensource-egynk.run.goorm.site/yunho/')
    
    def sign_out(request):
        session = Session.objects.get(pk=request.session.session_key)
        if session.expire_date < timezone.now():
            print("만료된 세션에서 로그아웃 완료")
            session.delete()
        else:
            session.delete()
            print("만료되지 않은 세션에서 로그아웃 완료")
        return redirect('https://opensource-egynk.run.goorm.site/yunho/')

class SessionStorage:
    def get_all_user_sessions():
        return Session.objects.all() #from django.contrib.sessions.models import Session
    
    def rm_duplicated_session(email):
        flag=0
        #checked by email (We denoted USERNAME_FIELD = 'email')
        sessions = SessionStorage.get_all_user_sessions()
        for session in sessions: #sessions are QuerySet
            session_data = session.get_decoded() #QuerySet -> dictionary
            if session_data.get('email') == email: #QuerySet can't use get method
                print('중복 로그인 존재(이전 로그인 일자):', session_data.get('create_time'))
                session.delete()
                print("중복 세션 지우기 완료")
                flag=1
        if flag==0:
            print("중복로그인이 존재하지 않았습니다.")
    
    def get_expired_session():
        expired_sessions = Session.objects.filter(expire_date__lte=timezone.now())
        if expired_sessions.exists(): #better than using None
            print("만료된 세션 존재")
        else:
            print("expired_sessions 미존재")
        return expired_sessions
    
    def rm_expired_session(expired_sessions): #Delete all expired sessions at once while checking for the expiration of a specific user. (It is deemed unnecessary to delete only those belonging to a specific user.)
        if expired_sessions.exists():
            print("만료된 세션들:", expired_sessions)
            expired_sessions.delete() #delete expired_sessions (expired_sessions: QuerySet)
            print("세션 삭제 완료")
        else:
            print("아직 만료된 세션이 없습니다.")
            