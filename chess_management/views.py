from django.shortcuts import render,get_object_or_404
from .serializers import *
from .models import User
from rest_framework import permissions
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.forms.models import model_to_dict

#Admin features---------------------------------------------------------------------
class ViewUserInformation(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get(self,request,*args,**kwargs):
        all_players = User.objects.all().exclude(username = self.request.user.username)
        results_dict = [model_to_dict(result) for result in all_players]
        return Response({'all_users':(results_dict)})
       
    
class DeletePlayersView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def delete(self,request,username):
       
            user = get_object_or_404(User, username = username)
            if user:
                user.delete()
                return Response({"status":True,"message":'User deleted successfully'})
            else:
                return Response({"status":False,
                        'message':'User not found'})
   
    

class ChangeUserInformationAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, username):
        user = get_object_or_404(User, username = username)
        serializer = ChangeUserInformationAdmin(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({
                'status': True,
                'message': 'User information updated successfully.'
            })
        return Response({
            'status': False,
            'errors': serializer.errors
        })

class CreateTournamentView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TournamneManagemnetAdmin(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Tournament created successfully.'
            })
        return Response({
            'status': False,
            'errors': serializer.errors
        })
    

class GeneratePairingsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = GeneratePairingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Pairings generated successfully.'
            }, status=201)
        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=400)

class UpdateMatchResultView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        serializer = MatchResultSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Match result updated successfully.'
            }, status=200)
        return Response({
            'status': False,
                'errors': serializer.errors
        }, status=400)
    
class GenerateLeaderBoardView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self,request,tour_id):
        tournament = get_object_or_404(Tournament,id=tour_id)
        all_users = tournament.participants.filter(is_active=True).order_by("rating")
        
        if all_users.exists():
            serializers = UserLeaderboardSerializer(all_users,many=True).data
            return Response({"leadearboard":serializers})
        return Response({'status':False,'message':'Users not found in that tournament'})