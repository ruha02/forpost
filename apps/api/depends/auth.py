from services import users_api

current_active_user = users_api.current_user(active=True)
current_admin_user = users_api.current_user(active=True, superuser=True)
