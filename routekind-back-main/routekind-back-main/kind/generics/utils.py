import re
import json
import base64
import uuid
import py_mini_racer

from dateutil.parser import parse
from urllib.parse import quote, unquote, urlparse

from django.utils import timezone
from rest_framework.exceptions import ValidationError


class InvalidNameException(ValidationError):
    def __init__(self, detail=None, code=None):
        detail = 'El nombre debe iniciar con una letra y no puede contener espacios en blanco ni caracteres.'
        super().__init__(detail, code)


def to_camel_case(text: str) -> str:
    if text is None:
        return None
    words = text.split('_')
    # Convertir todas las palabras excepto la primera a CamelCase
    camel_case_words = [word.capitalize() for word in words[1:]]
    # Agregar la primera palabra sin modificar
    camel_case_words.insert(0, words[0])
    # Unir las palabras en una sola cadena
    return ''.join(camel_case_words)


def to_snake_case(text: str) -> str:
    # Primera letra en minúsculas
    snake_case = text[0].lower()
    # Iterar por cada letra de la cadena
    for i in range(1, len(text)):
        # Si es una letra mayúscula
        if text[i].isupper():
            # Agregar un guión bajo y la letra en minúsculas
            snake_case += '_'
            snake_case += text[i].lower()
        else:
            # Si es una letra minúscula, agregarla tal cual
            snake_case += text[i]
    # Retornar la cadena en formato snake_case
    return snake_case


def to_verbose_name(text: str) -> str:
    return text.replace('_', ' ').capitalize()


def format_date_to_iso(value, *, include_date=True, include_time=True):
    try:
        # TODO: Definir zona horaria (-04:00) de la empresa, y urilizarlo para formatear los datos, sino, la hora queda muy mal
        # TODO: O bien, especificar en la url 'tz=-4' para formater todas las fechas según este criterio
        local_tz = timezone.get_current_timezone()
        # Return only date
        if not include_time:
            return parse(value, tzinfos={"": local_tz}).date().isoformat()
        # Return only time
        if not include_date:
            return parse(value, tzinfos={"": local_tz}).time().isoformat()
        # Return datetime
        return parse(value).astimezone(local_tz).isoformat()
    except ValueError:
        return None


def is_valid_email(value: str, *, raise_exception=False):
    if value is None:
        return True

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if type(value) != str or not re.match(email_pattern, value):
        if raise_exception:
            raise ValidationError('{} is not a valid email'.format(value))
        return False

    return True


def date_time_validator(value):
    class DateTimeValidationResult:
        def __init__(self, text) -> None:
            self.text = text

        def is_valid_date_only(self):
            try:
                if ':' in self.text:
                    return False
                parsed = parse(self.text, fuzzy=True)
                return bool(parsed.date())
            except:
                return False

        def is_valid_time_only(self):
            try:
                if ':' not in self.text:
                    return False
                parsed = parse(self.text, fuzzy=True)
                return bool(parsed.time())
            except:
                return False

        def is_valid_datetime(self):
            try:
                parsed = parse(self.text, fuzzy=True)
                return bool(parsed.date()) and bool(parsed.time())
            except:
                return False

        def is_valid_text(self):
            try:
                parse(self.text, fuzzy=True)
                return True
            except:
                return False

    return DateTimeValidationResult(value)


def format_list_value_from_json(value, *, default=[]):
    try:
        value = json.loads(value)
        if type(value) == list:
            return value
    except json.JSONDecodeError:
        pass
    return default


def is_valid_url(value):
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def decode_base64_file(value, *, raise_exception=True):
    try:
        return base64.b64decode(value)
    except:
        if raise_exception:
            raise ValidationError('Invalid base64 data.')
        return None


def is_valid_file_data(value: dict):
    basic_validation = all([
        type(value) == dict,
        'data' in value,
        'fileName' in value,
        'contentType' in value,
        type(value.get('data')) == str,
        type(value.get('fileName')) == str,
        type(value.get('contentType')) == str,
    ])
    if not basic_validation:
        return False

    if decode_base64_file(value.get('data')) is None:
        return False

    # Validate content type structure
    content_type: str = value.get('contentType')
    # TODO: Mostrar mensaje de error 'content type is not valid' al usuario...
    if len(content_type.split('/')) != 2:
        return False

    # TODO: Validate content type values (image, file, ...) (pdf, png, ...)

    return True


def is_valid_file_data_response(value: dict):
    return all([
        type(value) == dict,
        'url' in value,
        'fileName' in value,
        'contentType' in value,
        type(value.get('url')) == str,
        type(value.get('fileName')) == str,
        type(value.get('contentType')) == str,
    ])


def is_valid_image_data(value):
    if not is_valid_file_data(value):
        return False

    content_type: str = value.get('contentType')
    [type, format] = content_type.split('/')

    if type.lower() != 'image':
        return False

    # TODO: Validate format is a valid option (PNG, JPEG, etc...)

    return True


def validate_strict_name(value, *, raise_exception=True):
    if value in ["id", "created_by", "updated_by", "created_at", "updated_at"]:
        raise ValidationError(f"{value} is a restricted name")

    if re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', value):
        return True

    if raise_exception:
        raise InvalidNameException()

    return False


def is_valid_uuid(uuid_str: str, *, raise_exception=True):
    try:
        uuid_obj = uuid.UUID(uuid_str, version=4)
        return str(uuid_obj) == uuid_str
    except ValueError:
        if raise_exception:
            raise ValidationError(f'{uuid_str} no es un id válido')
        return False


def uuid_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError("Tipo no serializable")


def eval_contextualized_js_code(
    code: str,
    data=None,
    *,
    in_function=True,
    global_data_prop_name='data'
):
    def in_function_code(code: str):
        return f"(() => {{ {code} }})()"

    # Eval code with data
    try:
        ctx = py_mini_racer.MiniRacer()
        # Load data to context
        if data is not None:
            ctx.eval("const {name} = {data};".format(
                name=global_data_prop_name,
                data=json.dumps(data, default=uuid_serializer)
            ))
        # Evaluate function in a function an save the result
        ctx.eval("const result = {code}".format(
            code=in_function_code(code) if in_function else code
        ))
        # Convert result to json and the to dict
        str_result = ctx.eval("JSON.stringify({ result });")
        return json.loads(str_result).get('result')
    except Exception as e:
        print("[ERROR] on eval_contextualized_code:", e.args)
        raise ValidationError({"error": f"Unable to evaluate code. {e.args}"})


def str_is_int(value: str):
    if not value:
        return False
    if value[0] in ('-', '+'):
        return value[1:].isdigit()
    return value.isdigit()


def str_is_float(value: str):
    if value[0] in ('-', '+'):
        value = value[1:]

    parts = value.split('.')

    # Debe tener al menos una parte y máximo dos (parte entera y decimal)
    if len(parts) > 2:
        return False

    # Todas las partes deben ser dígitos
    for part in parts:
        if not part.isdigit():
            return False

    return True

def has_consecutive_charactes(text: str):
    counter = 1
    for i in range(1, len(text)):
        if text[i].isalpha() and text[i - 1].isalpha():
            if ord(text[i]) - ord(text[i - 1]) == 1:
                counter += 1
                if counter > 2:
                    return True
            else:
                counter = 1
        else:
            counter = 1
    return False


def has_consecutive_numbers(text: str):
    counter = 1
    for i in range(1, len(text)):
        if text[i].isdigit() and text[i - 1].isdigit():
            if int(text[i]) - int(text[i - 1]) == 1:
                counter += 1
                if counter > 2:
                    return True
            else:
                counter = 1
        else:
            counter = 1
    return False

def get_password_salt_from_username(username: str):
    return f"{username}{username}{username}{username}"