from django.shortcuts import render, redirect

#session setting
from django.utils import timezone
from django.contrib.sessions.models import Session

#import usermodel 임시로 저장된 유저 모델 체크
from user import models as UserModel
#import manage user SessionStorage
from user.views import SessionStorage as UserSessionStorage

def index(request):
    sessions = UserSessionStorage.get_all_user_sessions()
    print("존재하는 세션:", sessions)
    
    UserSessionStorage.rm_expired_session(UserSessionStorage.get_expired_session())
    
    
    try:
        user_email = request.session['email']
        u = UserModel.User.objects.get(email=user_email)
        profile = u.profile
        print("유저 모델에 접근해서 이메일 확인:", u.email)
        print("세션 생성일자:", request.session['create_time'])
        context = {
            'username': u.username
        }
        return render(request, 'yunho/profile.html', context)
    except:
        print("세션 만료 or 세션 미생성")
        
    
    return render(request, 'yunho/profile.html')