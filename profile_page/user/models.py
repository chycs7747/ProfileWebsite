from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email = email,
            username = username,
            password = password
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email = email,
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_master = True
        user.save()
        return user
    

#이메일, 권한등급 관련 속성 -> User / 부가적 정보 -> Profile / 
class User(AbstractBaseUser):
    class Meta:
        app_label = 'user'
    
    email = models.EmailField(max_length=50, unique=True) ## 이메일 굳이 필요가 있을까?
    username = models.CharField(max_length=20) # 이름
    password = models.CharField(max_length=20) # 이름
    is_master = models.BooleanField(default=False) # 마스터 권한여부
    is_admin = models.BooleanField(default=False) # 관리자 권한여부
    is_active = models.BooleanField(default=True) # 회원 권한여부

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] ##email을 인증 수단으로 사용해서 뺌

    def __str__(self):
        return str(self.email) ##학번이 profile로 이동했으므로 email로 수정
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username


class Profile(models.Model):
    class Meta:
        app_label = 'user'
    job = models.CharField(max_length=10) # 교수 / 학생
    gender = models.CharField(max_length=10) # 성별 - 프론트
    join_date = models.DateTimeField(auto_now_add=True) # 가입날짜
    user = models.OneToOneField('User', on_delete=models.CASCADE) # 프로필

    def get_job(self):
        return self.job

    def get_gender(self):
        return self.gender

    def get_join_date(self):
        return self.join_date
    
    def get_user(self):
        return self.user