from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        self.stdout.write('Clearing existing data...')
        # Delete existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        
        # Create unique index on email field
        db.users.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))
        
        # Marvel superheroes
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@avengers.com', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'steve.rogers@avengers.com', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor.odinson@avengers.com', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@avengers.com', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'bruce.banner@avengers.com', 'team': 'Team Marvel'},
            {'name': 'Spider-Man', 'email': 'peter.parker@avengers.com', 'team': 'Team Marvel'},
        ]
        
        # DC superheroes
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@justiceleague.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'bruce.wayne@justiceleague.com', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@justiceleague.com', 'team': 'Team DC'},
            {'name': 'Flash', 'email': 'barry.allen@justiceleague.com', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'arthur.curry@justiceleague.com', 'team': 'Team DC'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@justiceleague.com', 'team': 'Team DC'},
        ]
        
        all_heroes = marvel_heroes + dc_heroes
        
        # Insert users
        self.stdout.write('Inserting users...')
        for hero in all_heroes:
            user_doc = {
                'name': hero['name'],
                'email': hero['email'],
                'team': hero['team'],
                'joined_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'total_points': 0
            }
            db.users.insert_one(user_doc)
        
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(all_heroes)} users'))
        
        # Insert teams
        self.stdout.write('Inserting teams...')
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Avengers assemble! The mightiest heroes of Earth.',
                'created_date': datetime.now() - timedelta(days=60),
                'total_points': 0,
                'members': [hero['email'] for hero in marvel_heroes]
            },
            {
                'name': 'Team DC',
                'description': 'Justice League united! Defenders of truth and justice.',
                'created_date': datetime.now() - timedelta(days=55),
                'total_points': 0,
                'members': [hero['email'] for hero in dc_heroes]
            }
        ]
        db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams)} teams'))
        
        # Insert activities
        self.stdout.write('Inserting activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        activities = []
        
        for hero in all_heroes:
            for i in range(random.randint(3, 8)):
                activity = {
                    'user_email': hero['email'],
                    'user_name': hero['name'],
                    'activity_type': random.choice(activity_types),
                    'duration': random.randint(20, 120),  # minutes
                    'distance': round(random.uniform(1.0, 15.0), 2) if random.choice([True, False]) else None,
                    'calories': random.randint(100, 800),
                    'points': random.randint(10, 50),
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'notes': 'Great workout session!'
                }
                activities.append(activity)
        
        db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities)} activities'))
        
        # Calculate and update user points
        self.stdout.write('Calculating user points...')
        for hero in all_heroes:
            user_activities = db.activities.find({'user_email': hero['email']})
            total_points = sum(activity['points'] for activity in user_activities)
            db.users.update_one(
                {'email': hero['email']},
                {'$set': {'total_points': total_points}}
            )
        
        # Calculate and update team points
        self.stdout.write('Calculating team points...')
        for team in teams:
            team_users = db.users.find({'team': team['name']})
            total_points = sum(user['total_points'] for user in team_users)
            db.teams.update_one(
                {'name': team['name']},
                {'$set': {'total_points': total_points}}
            )
        
        # Insert leaderboard entries
        self.stdout.write('Inserting leaderboard entries...')
        leaderboard_entries = []
        
        # Individual leaderboard
        users = list(db.users.find().sort('total_points', -1))
        for rank, user in enumerate(users, 1):
            leaderboard_entries.append({
                'type': 'individual',
                'name': user['name'],
                'email': user['email'],
                'team': user['team'],
                'points': user['total_points'],
                'rank': rank,
                'last_updated': datetime.now()
            })
        
        # Team leaderboard
        teams_sorted = list(db.teams.find().sort('total_points', -1))
        for rank, team in enumerate(teams_sorted, 1):
            leaderboard_entries.append({
                'type': 'team',
                'name': team['name'],
                'points': team['total_points'],
                'rank': rank,
                'last_updated': datetime.now()
            })
        
        db.leaderboard.insert_many(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_entries)} leaderboard entries'))
        
        # Insert workout suggestions
        self.stdout.write('Inserting workout suggestions...')
        workouts = [
            {
                'name': 'Hero Training - Strength',
                'description': 'Build superhero strength with this intense workout',
                'difficulty': 'Hard',
                'duration': 45,
                'exercises': [
                    'Bench Press 4x8',
                    'Squats 4x10',
                    'Deadlifts 3x8',
                    'Pull-ups 3x12',
                    'Shoulder Press 3x10'
                ],
                'category': 'Strength'
            },
            {
                'name': 'Speedster Cardio',
                'description': 'Run like the Flash with this cardio routine',
                'difficulty': 'Medium',
                'duration': 30,
                'exercises': [
                    '5 min warm-up jog',
                    '10x 100m sprints',
                    '5 min cool-down walk',
                    'Dynamic stretching'
                ],
                'category': 'Cardio'
            },
            {
                'name': 'Warrior Flexibility',
                'description': 'Enhance flexibility and balance like a true warrior',
                'difficulty': 'Easy',
                'duration': 25,
                'exercises': [
                    'Sun Salutations 5x',
                    'Warrior Poses',
                    'Tree Pose',
                    'Pigeon Pose',
                    'Meditation 5 min'
                ],
                'category': 'Flexibility'
            },
            {
                'name': 'Combat Training',
                'description': 'Mixed martial arts inspired workout',
                'difficulty': 'Hard',
                'duration': 60,
                'exercises': [
                    'Shadow Boxing 3x3 min',
                    'Heavy Bag 5x2 min',
                    'Burpees 3x20',
                    'Jump Rope 10 min',
                    'Core Work'
                ],
                'category': 'Combat'
            },
            {
                'name': 'Beginner Hero Path',
                'description': 'Start your superhero journey here',
                'difficulty': 'Easy',
                'duration': 20,
                'exercises': [
                    'Push-ups 3x10',
                    'Bodyweight Squats 3x15',
                    'Plank 3x30 sec',
                    'Lunges 3x10 each leg',
                    'Jumping Jacks 3x20'
                ],
                'category': 'Full Body'
            }
        ]
        
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts)} workout suggestions'))
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Leaderboard entries: {db.leaderboard.count_documents({})}')
        self.stdout.write(f'Workouts: {db.workouts.count_documents({})}')
        
        client.close()
