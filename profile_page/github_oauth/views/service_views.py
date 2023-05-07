#google_api
from django.shortcuts import render, redirect
from config import settings
import requests #파이썬 모듈 설치 필요 - HTTP 요청을 보낼 때 사용한다.

#Service
from django.core.exceptions import ValidationError

class GithubService:
    def github_get_access_token(authorization_code):
        '''
        access token을 받는 메소드입니다.\n
        Authorization Code Grant Flow에서는 client_id, client_secret, code, grant_type, redirect url을
        'https://oauth2.googleapis.com/token'의 뒤에 붙여 post방식으로 access token을 받아옵니다.
        '''
        client_id = settings.GITHUB_CLIENT_ID
        client_secret_password = settings.GITHUB_CLIENT_SECRET_PASSWORD
        redirect_uri = settings.GITHUB_REDIRECT_URI_GOORM
        github_token_api_uri = settings.GITHUB_TOKEN_API
        grant_type = 'authorization_code' #다른 것도 존재하지만 이걸 쓰는게 보편적임
        #token_response의 값 중 refresh_token값은 원래 null이지만, code를 받는 부분의 scope에 access_type=offline&prompt=consent를 추가시켜, 로그인 시마다 refresh_token을 '새로'발급 받도록 하였다. 참고로 매 로그인 시마다 refresh_token을 갱신할지 안할지는 개발마다 다를 수 있다.
        #'expires_in': 3599 : 3599초 만료시간
        #id_token: 서비스 또는 애플리케이션에 Cloud Run, Cloud Functions, IAP(Identity-Aware Proxy)와 같은 "Google 서비스가 사용되는 경우" Google이 ID 토큰을 검증.
        #추가로 id_token은 ID 토큰은 절대로 API로 보내서는 안 된다. (id_token은 jwt양식)
        #Bearer 토큰은 토큰을 소유한 사람에게 액세스 권한을 부여하는 일반적인 토큰 클래스입니다. 예) 액세스 토큰, ID 토큰
        #expires_in: 만료시간 - Google Access tokens are created by Googles authorization server, Googles access tokens expire after one hour. You do not have access to change this.
        token_response = requests.post(f'{github_token_api_uri}?client_id={client_id}&client_secret={client_secret_password}&code={authorization_code}&grant_type={grant_type}&redirect_uri={redirect_uri}', headers={"Accept" : "application/json"})
        print("token response",token_response.json()) #json형식으로 token_response 확인. 이 정보는, 어떤 authorization code를 넣는지(scope가 다른)에 따라 반환하는 양이 다를 수 있다.
        #토큰이 유효하지 않으면 오류 발생(ex) access token's expires 만료)
        if not token_response.ok:
            raise ValidationError('github_token is invalid')
    
        access_token = token_response.json().get('access_token')
        return access_token
    
    def github_get_user_info(access_token):
        
        user_info_response = requests.get(
            "https://api.github.com/user",
            headers={
                "Accept": "application/vnd.github+json" ,
                "Authorization": f'Bearer {access_token}',
                "X-GitHub-Api-Version": "2022-11-28" ,
            }
        )
        #print(user_info_response.json())
        
        if not user_info_response.ok:
            raise ValidationError('Failed to obtain user info from GitHub.')
        
        user_info = user_info_response.json()
        
        return user_info
        
        """
        위와 같은 방법
            headers = {
                "Accept": "application/vnd.github+json" ,
                "Authorization": f'Bearer {access_token}',
                "X-GitHub-Api-Version": "2022-11-28" ,
            }

            user_info_response = requests.get("https://api.github.com/user", headers=headers)
            print(user_info_response.json())
        """
    
    def github_get_user_repo_info(access_token, username):
        
        user_repo_response = requests.get(
            f'https://api.github.com/users/{username}/repos',
            headers={
                "Accept": "application/vnd.github+json" ,
                "Authorization": f'Bearer {access_token}',
                "X-GitHub-Api-Version": "2022-11-28" ,
            }
        )
        
        if not user_repo_response.ok:
            raise ValidationError('Failed to obtain user info from GitHub.')
        
        user_info = user_repo_response.json()
        #print(user_info)
        
        return user_info