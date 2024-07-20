from django.urls import path
from .views import *


urlpatterns = [
    path('all-players',ViewUserInformation.as_view(),name="view_user_information"),
    path('delete-user/<str:username>',DeletePlayersView.as_view(),name='delete_user'),
    path('update-playersinfo/<str:username>',ChangeUserInformationAdminView.as_view(),name="change_user_information_admin"),
    path('create-tournament',CreateTournamentView.as_view(),name="create_tournament"),
    path('generate-pairings',GeneratePairingsView.as_view(),name="generate_pairings"),
    path('result-update/<int:match_id>',UpdateMatchResultView.as_view(),name="update_match_result"),
    path('leadbord/<int:tour_id>',GenerateLeaderBoardView.as_view(),name="generate_leaderboard")
]