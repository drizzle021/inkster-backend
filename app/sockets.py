from flask_socketio import send, emit, join_room, leave_room
from app.middleware import ws_auth_required
from app.extensions import socketio
from app.models.user import follows
from app.extensions import db


@socketio.on('login')
@ws_auth_required
def handle_login(user_id):
    print(f"login {user_id}")
    followed_users = db.session.query(follows).filter(follows.c.follower_id == user_id).all()

    for followed in followed_users:
        join_room(str(followed.followed_id))

    

@socketio.on('follow')
@ws_auth_required
def handle_follow(user_id, json):
    print(f"follow {json}")
    followed_user_id = json.get("followed_user_id")
    join_room(str(followed_user_id))


@socketio.on('unfollow')
@ws_auth_required
def handle_unfollow(user_id, json):
    print(f"unfollow {json}")
    unfollowed_user_id = json.get("unfollowed_user_id")
    leave_room(str(unfollowed_user_id))


@socketio.on('new_post')
@ws_auth_required
def handle_new_post(user_id, json):
    print(f"new_post {json}")
    post_title = json.get("post_title")
    emit("notification", {"message": f"{user_id} created post '{post_title}'"}, room=str(user_id))