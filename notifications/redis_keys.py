def get_user_unread_notifications_key(user_id):
    return f"notifications:user:{user_id}:unread_count"