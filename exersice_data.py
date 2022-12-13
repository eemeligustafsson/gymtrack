from app import create_app
from models.exercise import Exercise

def insert_data():
    app = create_app()
    with app.app_context():
        Exercise.create('Golden Six', 'Squat, Bench Press, Pull up, Over Head Press, Curl, Sit Up')
        Exercise.create('Upper/Lower', 'Bench Press, Barbell Row, Seated Overhead Dumbbell Press, Pec Dec, V-Bar Lat Pull Down, Side Lateral Raise, Cable Triceb Extensions, Cable Curls')
        Exercise.create('Push, Pull, Legs', 'Bench Press, Seated Dumbbell Shoulder Press, Incline Dumbbell Press, Side Lateral Raises, Triceps Pressdowns, Overhead Triceps Extension')

if __name__ == "__main__":
    insert_data()

