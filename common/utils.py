# utils.py or some relevant file
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
     
    refresh['user_id'] = str(user.user_id)
    refresh['mobile_number'] = user.mobile_number

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
