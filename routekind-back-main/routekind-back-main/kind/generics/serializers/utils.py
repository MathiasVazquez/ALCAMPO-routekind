from rest_framework.exceptions import APIException


def get_request_data_from_context(context, raise_exception=True):
    # Get serializer request data
    # 1. From self.context["request"].data if the serializer was invoked from a view
    # 2. From self.context["data"] if the serializer was invoked from another NestedModelSerializerMixin
    request_data = context.get("data", None)
    if request_data is None:
        request = context.get("request")
        if request is not None:
            request_data = request.data

    if request_data is None and raise_exception:
        raise APIException("Cannot get serializer's request data.")

    return request_data
