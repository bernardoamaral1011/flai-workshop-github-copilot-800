from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=100)
    joined_date = models.DateTimeField()
    total_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_date = models.DateTimeField()
    total_points = models.IntegerField(default=0)
    members = models.JSONField()

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField(null=True, blank=True)  # in km
    calories = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    type = models.CharField(max_length=20)  # 'individual' or 'team'
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    points = models.IntegerField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.rank}. {self.name} - {self.points} pts"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    duration = models.IntegerField()  # in minutes
    exercises = models.JSONField()
    category = models.CharField(max_length=50)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
