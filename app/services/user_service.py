from app.models import User

class UserService:
    @staticmethod
    def get_all_users():
        """
        Retrieves all users from the database.
        """
        users = User.query.all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            for user in users
        ]
