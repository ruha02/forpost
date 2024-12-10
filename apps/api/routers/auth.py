from services import users_api, auth_backend


router = users_api.get_auth_router(
    auth_backend,
)
