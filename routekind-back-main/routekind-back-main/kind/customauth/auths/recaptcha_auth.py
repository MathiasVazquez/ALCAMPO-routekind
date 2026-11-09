from rest_framework.exceptions import ValidationError
import requests

RECAPTCH_HOST = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCH_SECRET = "6Le3ur4pAAAAAGlTWstd1A_hH-n9XH2csSdzN9jS"

RECAPTCH_TIMEOUT = 30 * 1000  # 30 seconds


def is_valid_recaptcha(recaptcha_token: str, *, raise_exception=False):
    # Get captcha response
    response = requests.post(
        f"{RECAPTCH_HOST}?secret={RECAPTCH_SECRET}&response={recaptcha_token}",
        timeout=RECAPTCH_TIMEOUT
    )
    response_data: dict = response.json()
    success = response_data.get("success")

    # Validate success captcha verification
    if not success:
        if raise_exception:
            raise ValidationError({
                'error': 'No fue posible verificar el recaptcha, por favor vuelva a intentarlo.'
            })
        return False

    # Validate minimum score
    score = response_data.get("score")
    if score < 0.7:
        if raise_exception:
            raise ValidationError({
                'error': 'La verificación por captcha no ha sido superada, '
                'por favor vuelva a intentarlo.'
            })
        return False

    return True
