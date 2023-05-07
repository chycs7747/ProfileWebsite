#google_api
from django.shortcuts import render, redirect
from config import settings
from django.conf import settings

#import service
from . import service_views


# Create your views here.

class GoogleOauthLogin:
    def google_login(request): #구글 로그인->코드받아옴->redirect로인해 google_callback실행
        '''
        Authorization Server에 client_id, response_type, redirect_url, scope 등을 넘겨주어 google_callback을 실행
        '''
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI_GOORM
        print(redirect_uri)
        scope = settings.GOOGLE_SCOPE

        #required: response_type, client_id, state? / optional: redirect_url, scope, access_type, prompt
        return redirect(f'{settings.GOOGLE_ENDPOINT}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}&access_type=offline&prompt=select_account')

    def google_callback(request):
        code = request.GET.get('code') #get authorization_code(Use as approval permissions for resource servers) -> for Authorization Code Grant Flow
        
        #액세스 토큰은 API에서 읽고 유효성을 검사하기 위한 것
        #하단의 엑세스 토큰을 발급받고,
        
        access_token, refresh_token = service_views.GoogleService.google_get_token(code) #code를 이용해서 access token을 받아옴 / views_service.py의 class Service 이용
        request.session.modified = True
        request.session['check'] = 'check'
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session.save()
        print("구글컬백함수안 : ",request.session['access_token'])
        
        
        return redirect('https://opensource-egynk.run.goorm.site/yunho/sign_in')
        
