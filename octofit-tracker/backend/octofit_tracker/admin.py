from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team', 'total_points', 'joined_date']
    list_filter = ['team', 'joined_date']
    search_fields = ['name', 'email']
    ordering = ['-total_points']
    readonly_fields = ['joined_date']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_points', 'created_date']
    search_fields = ['name', 'description']
    ordering = ['-total_points']
    readonly_fields = ['created_date']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'activity_type', 'duration', 'calories', 'points', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_name', 'user_email', 'activity_type']
    ordering = ['-date']
    readonly_fields = ['date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'name', 'type', 'points', 'team', 'last_updated']
    list_filter = ['type', 'team']
    search_fields = ['name', 'email']
    ordering = ['rank']
    readonly_fields = ['last_updated']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'duration', 'category']
    list_filter = ['difficulty', 'category']
    search_fields = ['name', 'description', 'category']
    ordering = ['name']
