from django.http import HttpResponse
import os
class IPRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Obtener las IPs permitidas desde el archivo .env usando os.environ.get
        # allowed_ips_str = os.environ.get('ALLOWED_IPS', '')  # Obtenemos la cadena de IPs
        # self.allowed_ips = [ip.strip() for ip in allowed_ips_str.split(',')]  # Convertimos la cadena en lista

    def __call__(self, request):
        # Aplica la restricción solo si la ruta empieza con /api/admin
        # if request.path.startswith('/api/admin'):
        #     # Obtener la IP del cliente
        #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        #     if x_forwarded_for:
        #         client_ip = x_forwarded_for.split(',')[0]
        #     else:
        #         client_ip = request.META.get('REMOTE_ADDR')

        #     # Verificar si la IP está permitida
        #     if client_ip not in self.allowed_ips:
        #         return self.forbidden_response()

        # Permitir el acceso para otras rutas
        response = self.get_response(request)
        return response
    def forbidden_response(self):
        return HttpResponse(status=403)