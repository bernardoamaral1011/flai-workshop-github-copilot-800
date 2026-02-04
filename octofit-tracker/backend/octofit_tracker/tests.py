from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test Hero',
            'email': 'test@hero.com',
            'team': 'Test Team',
            'joined_date': datetime.now(),
            'total_points': 100
        }
        self.user = User.objects.create(**self.user_data)

    def test_get_users_list(self):
        """Test retrieving list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        """Test retrieving a single user"""
        url = reverse('user-detail', kwargs={'pk': self.user._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user_data['name'])


class TeamAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Team',
            'description': 'A test team',
            'created_date': datetime.now(),
            'total_points': 500,
            'members': ['test1@hero.com', 'test2@hero.com']
        }
        self.team = Team.objects.create(**self.team_data)

    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_detail(self):
        """Test retrieving a single team"""
        url = reverse('team-detail', kwargs={'pk': self.team._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.team_data['name'])


class ActivityAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_email': 'test@hero.com',
            'user_name': 'Test Hero',
            'activity_type': 'Running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'points': 25,
            'date': datetime.now(),
            'notes': 'Great run!'
        }
        self.activity = Activity.objects.create(**self.activity_data)

    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_activity_detail(self):
        """Test retrieving a single activity"""
        url = reverse('activity-detail', kwargs={'pk': self.activity._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], self.activity_data['activity_type'])

    def test_filter_activities_by_user(self):
        """Test filtering activities by user email"""
        url = reverse('activity-list')
        response = self.client.get(url, {'user_email': 'test@hero.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'type': 'individual',
            'name': 'Test Hero',
            'email': 'test@hero.com',
            'team': 'Test Team',
            'points': 100,
            'rank': 1,
            'last_updated': datetime.now()
        }
        self.leaderboard = Leaderboard.objects.create(**self.leaderboard_data)

    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_individual_leaderboard(self):
        """Test retrieving individual leaderboard"""
        url = reverse('leaderboard-individual')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout',
            'difficulty': 'Medium',
            'duration': 45,
            'exercises': ['Push-ups', 'Squats', 'Planks'],
            'category': 'Strength'
        }
        self.workout = Workout.objects.create(**self.workout_data)

    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workout_detail(self):
        """Test retrieving a single workout"""
        url = reverse('workout-detail', kwargs={'pk': self.workout._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.workout_data['name'])

    def test_filter_workouts_by_difficulty(self):
        """Test filtering workouts by difficulty"""
        url = reverse('workout-list')
        response = self.client.get(url, {'difficulty': 'Medium'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTestCase(APITestCase):
    def test_api_root(self):
        """Test API root endpoint"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
