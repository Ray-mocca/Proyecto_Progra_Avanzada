from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class CompleteProfileMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        # Verifica si el usuario está autenticado
        if request.user.is_authenticated:
            # Intenta obtener el perfil del usuario
            try:
                profile = request.user.profile
                # Verifica si el perfil del usuario está completo
                if not profile.phone_number or not profile.address:
                    # Solo agregar el mensaje si no está ya en la lista de mensajes
                    if not any(msg.get('message') == 'Por favor, completa tu perfil agregando tu número de teléfono y dirección.' for msg in response.context.get('messages', [])):
                        response.context.setdefault('messages', []).append({
                            'level': 'info',
                            'message': 'Por favor, completa tu perfil agregando tu número de teléfono y dirección.'
                        })
            except AttributeError:
                # Si el usuario no tiene un perfil, simplemente no hacer nada
                pass
        return response
