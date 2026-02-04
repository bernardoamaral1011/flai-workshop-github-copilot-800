from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'joined_date', 'total_points']

    def get_id(self, obj):
        return str(obj._id)


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_date', 'total_points', 'members']

    def get_id(self, obj):
        return str(obj._id)


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_email', 'user_name', 'activity_type', 'duration', 
                  'distance', 'calories', 'points', 'date', 'notes']

    def get_id(self, obj):
        return str(obj._id)


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'type', 'name', 'email', 'team', 'points', 'rank', 'last_updated']

    def get_id(self, obj):
        return str(obj._id)


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 'exercises', 'category']

    def get_id(self, obj):
        return str(obj._id)
