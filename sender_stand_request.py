import requests
import configuration
import data


# Función para registrar un nuevo usuario y obtener la respuesta de la API
def post_new_user(user_body):
    return requests.post(
        configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
        json=user_body,
        headers=data.headers
    )


# Función para crear el kit personal de un usuario
def post_new_client_kit(kit_body, auth_token):
    # Clonamos las cabeceras base para no mutar el archivo original
    current_headers = data.headers.copy()
    # Añadimos el encabezado Authorization con el token dinámico recibido
    current_headers["Authorization"] = f"Bearer {auth_token}"

    return requests.post(
        configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,
        json=kit_body,
        headers=current_headers
    )