from rest_framework import exceptions
from rest_framework import serializers
from .models import *
from .utility import check_input,send_email
from django.contrib.auth.password_validation import validate_password 
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignUpSerialazier(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)


    def __init__(self,*args,**kwargs):
        super(SignUpSerialazier,self).__init__(*args,**kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id','auth_type','auth_status')
        extra_kwargs = {
            'auth_type': {'read_only':True,'required':False},
            'auth_status':{'read_only':True,'required':False}
        }

    def create(self,validated_data):
        user = super(SignUpSerialazier,self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email,code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number,code)
        user.save()
        return user
    
    def validate(self, data):
        super(SignUpSerialazier,self).validate(data)

        data = self.auth_validate(data)
        return data
    
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_input(user_input)
        if input_type == 'email':
            data = {
                'email':user_input,
                'auth_type':VIA_EMAIL
                
            }
        elif input_type=='phone':
            data = {
                'phone_number':user_input,
                'auth_type':VIA_PHONE
                
            }
        else: 
            data = {
                'status':False
            }
            raise exceptions.ValidationError(data)
        
        return data
    
    def validate_email_phone_number(self,valid):
        valid = valid.lower()
        if valid and User.objects.filter(email = valid).exists():
            data = {
                'status':False,
                'message':'Bu emaildan odgdin foydalanilgan'
            }
            raise exceptions.ValidationError(data)
        
        elif valid and User.objects.filter(phone_number = valid).exists():
            data = {
                'status':False,
                'message':'Bu raqamdan odgdin foydalanilgan'
            }
            raise exceptions.ValidationError(data)
        return valid

    def to_representation(self, instance):
        data = super(SignUpSerialazier,self).to_representation(instance)
        data.update(instance.token())
        return data
    
class ChangeUserInformation(serializers.Serializer):
    first_name = serializers.CharField(write_only=True,required=True)
    last_name = serializers.CharField(write_only=True,required=True)
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    confirm_password = serializers.CharField(write_only=True,required=True)

    def validate(self,data):
        password = data.get('password',None)
        confirm_password = data.get('confirm_password',None)

        if password != confirm_password:
            data = {
                'status':False,
                'message':'Parollar bir birga mos emas'
            }
            raise exceptions.ValidationError(data)
        if password:
            validate_password(password)
            validate_password(confirm_password)
        return data
    
    def validate_username(self,username):
        if len(username) <5 or len(username)>35:
            data={
                'status':False,
                'message':'username 5 va 35 dan yuqori bolmaslik kerak'
            }
            raise exceptions.ValidationError(data)
        if username.isdigit():
            data = {
                'status':False,
                'message':'usenameda faqat raqmlar ishlatilmaydi'
            }
        return username
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.password = validated_data.get('password',instance.password)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()
        
        return instance
    
    
class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self,*args,**kwargs):
        super(LoginSerializer,self).__init__(*args,**kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required =False,read_only=True)

    def auth_validate(self,data): #validating userinput wheather it is username,phone,email
        user_input = data.get('userinput')
        if check_input(user_input) == 'username':
            username = user_input
        elif check_input(user_input) =='phone':
            user = self.get_user(phone_number=user_input)
            username = user.username
        elif check_input(user_input) =='email':
            user = self.get_user(email__iexact=user_input)
            username = user.username
        else:
            data={
                'status':False,
                'message':'Incorrect username or password was inputeded'
            }
            raise exceptions.ValidationError(data)
        
        # check status user
        current_user = User.objects.filter(username__iexact=username).first()  # None

        if current_user is not None and current_user.auth_status in [NEW, CODE_VERIFIED]:
            raise exceptions.ValidationError(
                {
                    'success': False,
                    'message': "Siz royhatdan toliq otmagansiz!"
                }
            )
        user = authenticate(username=username,password=data['password'])
        if user is not None:
            self.user = user
        else:
            raise exceptions.ValidationError(
                {
                    'success': False,
                    'message': "Sorry, login or password you entered is incorrect. Please check and trg again!"
                }
            )
    def validate(self, data):
        print(data)
        self.auth_validate(data)
        if self.user.auth_status not in [DONE]:
            raise PermissionDenied("Siz login qila olmaysiz. Ruxsatingiz yoq")
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    def get_user(self,**kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise exceptions.ValidationError({
                'message':'No active user found'
            })
        return users.first()
    




