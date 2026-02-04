from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team', 'email']
    search_fields = ['name', 'email']
    ordering_fields = ['total_points', 'joined_date', 'name']
    ordering = ['-total_points']

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users grouped by team"""
        team = request.query_params.get('team', None)
        if team:
            users = User.objects.filter(team=team)
        else:
            users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['total_points', 'created_date', 'name']
    ordering = ['-total_points']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get team members"""
        team = self.get_object()
        users = User.objects.filter(team=team.name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'activity_type']
    search_fields = ['user_name', 'activity_type', 'notes']
    ordering_fields = ['date', 'points', 'duration', 'calories']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user"""
        email = request.query_params.get('email', None)
        if email:
            activities = Activity.objects.filter(user_email=email)
        else:
            activities = Activity.objects.all()
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities"""
        limit = int(request.query_params.get('limit', 10))
        activities = Activity.objects.all()[:limit]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for leaderboard (read-only)
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'team']
    ordering_fields = ['rank', 'points']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard"""
        leaderboard = Leaderboard.objects.filter(type='individual')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def team(self, request):
        """Get team leaderboard"""
        leaderboard = Leaderboard.objects.filter(type='team')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for workout suggestions (read-only)
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'category']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['duration', 'difficulty', 'name']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
        else:
            workouts = Workout.objects.all()
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get workouts by category"""
        category = request.query_params.get('category', None)
        if category:
            workouts = Workout.objects.filter(category=category)
        else:
            workouts = Workout.objects.all()
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
