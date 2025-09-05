from django.core import signing
import time

# Activation token settings
ACTIVATION_SALT = 'accounts-activation'
MAX_AGE = 60 * 60 * 24  # 24 hours in seconds


def make_activation_token(user):
    """Return a signed token containing the user id and timestamp."""
    payload = {'user_id': user.pk, 'ts': int(time.time())}
    return signing.dumps(payload, salt=ACTIVATION_SALT)


def validate_activation_token(token, max_age=MAX_AGE):
    """Return user_id if token is valid and not expired, otherwise None."""
    try:
        payload = signing.loads(token, salt=ACTIVATION_SALT, max_age=max_age)
        return payload.get('user_id')
    except (signing.BadSignature, signing.SignatureExpired):
        return None