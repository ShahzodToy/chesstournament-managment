from django.urls import path
from .views import *

urlpatterns = [
    path('registration',SignUpView.as_view()),# for users to register with emial or phonenumber
    path('verify',VrifyAPIView.as_view()), #After reciving 4 digit code verify with endpoint
    path('re-send',GetNewVerification.as_view()),# re-send back to smtp,console code
    path('change-info',ChangeUserInformation.as_view()),# entering main information for users
    path('login',LoginViewApi.as_view()),# Successfully sign up should login
    

]