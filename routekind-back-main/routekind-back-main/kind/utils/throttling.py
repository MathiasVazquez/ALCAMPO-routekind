from rest_framework.throttling import UserRateThrottle


class NonGetRateThrottle(UserRateThrottle):
    scope = 'non_get'

    def allow_request(self, request, view):
        if request.method == 'GET':
            return True  # Siempre permite GET, sin contarlas
        return super().allow_request(request, view)


class GetRateThrottle(UserRateThrottle):
    scope = 'on_get'

    def allow_request(self, request, view):
        if request.method == 'GET':
            return super().allow_request(request, view)
        return True  # Siempre permite GET, sin contarlas
