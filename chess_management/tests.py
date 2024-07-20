from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Tournament, Match

User = get_user_model()

class TournamentTestCase(TestCase):
    def setUp(self):
        # Create test users
        # Create test users with unique emails
            self.admin_user = User.objects.create_superuser(
                username='admin', password='adminpassword', email='admin@example.com'
            )
            self.regular_user = User.objects.create_user(
                username='user', password='userpassword', email='user@example.com'
            )
            self.client = APIClient()
            self.client.force_authenticate(user=self.admin_user)
            self.player1 = User.objects.create_user(
            username='player1', password='password1', email='player1@example.com'
            )
            self.player2 = User.objects.create_user(
            username='player2', password='password2', email='player2@example.com'
            )
            # Create test data
            self.tournament = Tournament.objects.create(
                name="Test Tournament", start_date="2024-08-01", end_date="2024-08-10"
            )
            self.match = Match.objects.create(
                tournament=self.tournament, player1=self.player1, player2=self.player2,round_number=1
            )



    def test_delete_user(self):
        url = reverse('delete_user', kwargs={'username': self.regular_user.username})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertFalse(User.objects.filter(username=self.regular_user.username).exists())

    def test_change_user_information_admin(self):
        url = reverse('view_user_information', kwargs={'username': self.regular_user.username})
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'updateduser')
        self.assertEqual(self.regular_user.email, 'updateduser@example.com')

    def test_create_tournament(self):
        url = reverse('create_tournament')
        data = {
            'name': 'New Tournament',
            'start_date': '2024-08-01',
            'end_date': '2024-08-10',
            'participants': ['Player1', 'Player2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], True)
        self.assertTrue(Tournament.objects.filter(name='New Tournament').exists())

    def test_generate_pairings(self):
        url = reverse('generate_pairings')
        data = {'tournament_id': self.tournament.id, 'participants': ['Player1', 'Player2']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], True)

    def test_change_user_information_admin(self):
        url = reverse('change_user_information_admin', kwargs={'username': self.player1.username})
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.player1.refresh_from_db()
        self.assertEqual(self.player1.username, 'updateduser')
        self.assertEqual(self.player1.email, 'updateduser@example.com')

    def test_update_match_result(self):
        url = reverse('update_match_result', kwargs={'match_id': self.match.id})
        data = {'result': 'Player1 won'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)

    def test_generate_leaderboard(self):
        url = reverse('generate_leaderboard', kwargs={'tour_id': self.tournament.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('leaderboard', response.data)

