from .serializers import *
from rest_framework.generics import CreateAPIView
from .models import User,VIA_EMAIL,VIA_PHONE
from rest_framework import permissions
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.exceptions import ValidationError
from .models import NEW,CODE_VERIFIED
from rest_framework.response import Response
from .utility import send_email
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerialazier

class VrifyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self,request,*args,**kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.verify_code(user,code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh']
            }
        )
    
    @staticmethod
    def verify_code(user,code):
        verifies =  user.verify_codes.filter(expiration_time__gte=datetime.now(),code=code,is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    def get(self,request,*args,**kwargs):

        user = self.request.user #user

        self.code_verification(user)

        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email,code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number,code)
        else:
            data ={
                'message':'Problem arised with your code'
            }
            raise ValidationError(data)
        return Response({'status':True,
                'message':'Code resend again check'})
    @staticmethod
    def code_verification(user):
            verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(),is_confirmed = True)
            if verifies.exists():
                data = {
                    'message':'Wait ypur code is still working'
                }
                raise ValidationError(data)
            return user
            


class ChangeUserInformation(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ChangeUserInformation


    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
       super(ChangeUserInformation,self).update(request, *args, **kwargs)
       data = {
           'status_code':200,
           'status':"Success",
           'message':'User information updated successfully'
       }
       return Response(data)
    

class LoginViewApi(TokenObtainPairView):
    serializer_class = LoginSerializer






