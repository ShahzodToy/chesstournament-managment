from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel
from datetime import datetime,timedelta
import random
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

ORDINARY_USER,MANAGER,ADMIN = ('ordinary_user','manager','admin')
VIA_EMAIL,VIA_PHONE = ('via_email','via_phone')
NEW,CODE_VERIFIED,DONE = ('new','code_verified','done')

class User(AbstractUser,BaseModel):
    USER_ROLES = (
        (ORDINARY_USER,ORDINARY_USER),
        (MANAGER,MANAGER),
        (ADMIN,ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE,VIA_PHONE),
        (VIA_EMAIL,VIA_EMAIL)
    )
    AUTH_STATUS = (
        (NEW,NEW),
        (CODE_VERIFIED,CODE_VERIFIED),
        (DONE,DONE),

    )

    user_roles = models.CharField(max_length=150,choices=USER_ROLES,default=ORDINARY_USER)
    auth_type = models.CharField(max_length=100,choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=100,choices=AUTH_STATUS,default=NEW)
    email = models.EmailField(null=True,unique=True,blank=True)
    phone_number = models.CharField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def create_verify_code(self,verify_type):
        code = ''.join([str(random.randint(0,100)%10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id = self.id,
            verify_type=verify_type,
            code = code
        )
        return code
    
    def check_username(self): #before creating real username it will generate ramdom username
        if not self.username:
            temp_username = f"instagram-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username = temp_username):
                temp_username = f'{temp_username}{random.randint(0,9)}'
            self.username = temp_username

    def check_email(self):
        if self.email:
            temp_email = self.email.lower()
            self.email = temp_email

    def check_pass(self):#before creating real password it will generate ramdom password
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self): # it will hash regular passwords
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)


    def token(self): # will give access and refresh token
        refresh = RefreshToken.for_user(self)
        return {
            'access':str(refresh.access_token),
            'refresh':str(refresh)
        }



    def save(self,*args,**kwargs):
        self.clean()
        super(User,self).save(*args,**kwargs)
    
    def clean(self): # for calling in one func to make clear
        self.check_username()
        self.check_email()
        self.check_pass()
        self.hashing_password()

EMAIL_EXP = 5
PHONE_EXP =2

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_EMAIL,VIA_EMAIL),
        (VIA_PHONE,VIA_PHONE)
    )

    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args,**kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now() + timedelta(minutes=(EMAIL_EXP))
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=(PHONE_EXP))

        super(UserConfirmation,self).save(*args,**kwargs)


    
