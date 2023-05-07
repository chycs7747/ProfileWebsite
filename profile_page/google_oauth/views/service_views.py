#google_api
from django.shortcuts import render, redirect
from config import settings
import requests #파이썬 모듈 설치 필요 - HTTP 요청을 보낼 때 사용한다.

#Service
from django.core.exceptions import ValidationError

class GoogleService:
    def google_get_token(authorization_code):
        '''
        access token을 받는 메소드입니다.\n
        Authorization Code Grant Flow에서는 client_id, client_secret, code, grant_type, redirect url을
        'https://oauth2.googleapis.com/token'의 뒤에 붙여 post방식으로 access token을 받아옵니다.
        '''
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret_password = settings.GOOGLE_CLIENT_SECRET_PASSWORD
        redirect_uri = settings.GOOGLE_REDIRECT_URI_GOORM
        google_token_api_uri = settings.GOOGLE_TOKEN_API
        grant_type = 'authorization_code' #다른 것도 존재하지만 이걸 쓰는게 보편적임
        #token_response의 값 중 refresh_token값은 원래 null이지만, code를 받는 부분의 scope에 access_type=offline&prompt=consent를 추가시켜, 로그인 시마다 refresh_token을 '새로'발급 받도록 하였다. 참고로 매 로그인 시마다 refresh_token을 갱신할지 안할지는 개발마다 다를 수 있다.
        #'expires_in': 3599 : 3599초 만료시간
        #id_token: 서비스 또는 애플리케이션에 Cloud Run, Cloud Functions, IAP(Identity-Aware Proxy)와 같은 "Google 서비스가 사용되는 경우" Google이 ID 토큰을 검증.
        #추가로 id_token은 ID 토큰은 절대로 API로 보내서는 안 된다. (id_token은 jwt양식)
        #Bearer 토큰은 토큰을 소유한 사람에게 액세스 권한을 부여하는 일반적인 토큰 클래스입니다. 예) 액세스 토큰, ID 토큰
        #expires_in: 만료시간 - Google Access tokens are created by Googles authorization server, Googles access tokens expire after one hour. You do not have access to change this.
        token_response = requests.post(f'{google_token_api_uri}?client_id={client_id}&client_secret={client_secret_password}&code={authorization_code}&grant_type={grant_type}&redirect_uri={redirect_uri}')
        print("token response",token_response.json()) #json형식으로 token_response 확인. 이 정보는, 어떤 authorization code를 넣는지(scope가 다른)에 따라 반환하는 양이 다를 수 있다.
        #토큰이 유효하지 않으면 오류 발생(ex) access token's expires 만료)
        if not token_response.ok:
            raise ValidationError('google_token is invalid')
    
        access_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        
        return access_token, refresh_token
    
    def google_get_user_info(access_token):
        '''
        Goodle의 user info api를 이용한다.\n
        <참고>\n
        구글 api를 이용하는 방식에는 두가지가 있다.
        1. access token을 Query Parameter로 보내는 것
        2. Authorization: Bearer 을 Header로 전송하는 것 (더 안전한 방식)\n
        2번을 쓰기 위해선 curl을 사용(사용하려면 추가설치를 하나 해야함)해야해서 1번을 사용함.
        '''
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={
                'access_token': access_token
            }
        )

        if not user_info_response.ok:
            raise ValidationError('Failed to obtain user info from Google.')
        
        user_info = user_info_response.json()
        
        return user_info
    
    
    def google_refresh_access_token(refresh_token):
        # 요청할 URL
        url = 'https://oauth2.googleapis.com/token'

        # POST 요청에 필요한 데이터
        data = {
            'grant_type': 'refresh_token',
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET_PASSWORD,
            'refresh_token': refresh_token
        }

        # POST 요청을 보내 엑세스 토큰 받아오기
        response = requests.post(url, data=data)
        print(response.json())
        new_access_token = response.json().get('access_token')

        return new_access_token