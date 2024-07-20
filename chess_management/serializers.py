from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from users.models import *
from rest_framework import serializers
from .models import Match, Tournament
from datetime import datetime,date


class TournamneManagemnetAdmin(serializers.Serializer): 
    name = serializers.CharField(max_length =200,required=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    participants = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    def validate_name(self,data):
        tour = Tournament.objects.filter(name = data)
        if tour.exists():
            data = {
                "status":False,
                "message":'Sorry but name already taken'
            }
            raise ValidationError(data)
        return data

    def validate_participants(self, data):
        if len(data) < 2:
            raise ValidationError({
                "status": False,
                "message": "A tournament must have at least 2 participants"
            })
        return data
        
    

    def validate_participants(self, data):
        # Ensure all participants exist and are valid users
        users = User.objects.filter(username__in=data)
        if len(users) != len(data):
            raise ValidationError({
                "status": False,
                "message": "Some user usernames are invalid."
            })
        return data
    
    def create(self, validated_data):
        participants = validated_data.pop('participants')
        tournament = Tournament.objects.create(**validated_data)
        tournament.participants.set(User.objects.filter(username__in=participants))
        return tournament



class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'result']

    def update(self, instance, validated_data):
        instance.result = validated_data.get('result', instance.result)
        instance.save()
        return instance
    

class GeneratePairingsSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()

    def create(self, validated_data):
        tournament_id = validated_data.get('tournament_id')
        tournament = get_object_or_404(Tournament, id=tournament_id)
        if tournament.exists():
            participants = list(tournament.participants.exclude(is_superuser=True).order_by('-rating'))
            print(participants)
            current_round = tournament.current_round

            for i in range(0, len(participants), 2):
                Match.objects.create(
                    tournament=tournament,
                    round_number=current_round,
                    player1=participants[i],
                    player2=participants[i+1] if i+1 < len(participants) else  None
                )

            tournament.current_round += 1
            tournament.save()
            return tournament
        raise ValidationError({"status":False,
                               "message":'Given tournament id is not found'})
    

class UserLeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'rating', 'country', 'age']

class ChangeUserInformationAdmin(serializers.Serializer):
    first_name = serializers.CharField(write_only=True,required=True)
    last_name = serializers.CharField(write_only=True,required=True)
    username = serializers.CharField(write_only=True,required=True)
    country = serializers.CharField(write_only=True,required=True)
    age = serializers.CharField(write_only=True,required=True)
    rating = serializers.CharField(write_only=True,required=True)

   
    
    def validate_username(self,username):
        if len(username) <5 or len(username)>35:
            data={
                'status':False,
                'message':'username 5 va 35 dan yuqori bolmaslik kerak'
            }
            raise ValidationError(data)
        if username.isdigit():
            data = {
                'status':False,
                'message':'usenameda faqat raqmlar ishlatilmaydi'
            }
        return username
    
    def validate_first_name(self,first_name):
        if len(first_name) <5 or len(first_name)>35:
            data={
                'status':False,
                'message':'first_name 5 va 35 dan yuqori bolmaslik kerak'
            }
            raise ValidationError(data)
        if first_name.isdigit():
            data = {
                'status':False,
                'message':'usenameda faqat raqmlar ishlatilmaydi'
            }
        return first_name
    
    def validate_last_name(self,last_name):
        if len(last_name) <5 or len(last_name)>35:
            data={
                'status':False,
                'message':'last_name 5 va 35 dan yuqori bolmaslik kerak'
            }
            raise ValidationError(data)
        if last_name.isdigit():
            data = {
                'status':False,
                'message':'last_name faqat raqmlar ishlatilmaydi'
            }
        return last_name



    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.country = validated_data.get('country',instance.country)
        instance.age = validated_data.get('age',instance.age)
        instance.rating = validated_data.get('rating',instance.rating)
        instance.save()
        
        return instance