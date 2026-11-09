from rest_framework.exceptions import APIException


class InvalidDefaultInitialOrderStateAPIException(APIException):
    def __init__(self) -> None:
        super().__init__({
            "message": "El valor inicial por defecto del estado de los pedidos no puede quedar vacío",
            "code_name": "invalid_default_initial_order_state",
            "code_number": "co-001"
        })
