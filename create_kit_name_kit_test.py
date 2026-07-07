import sender_stand_request
import data


# Función de apoyo para registrar un usuario de forma dinámica y extraer su token
def get_new_user_token():
    user_body = data.user_body.copy()
    response = sender_stand_request.post_new_user(user_body)
    return response.json()["authToken"]


# Función de apoyo para clonar el molde del kit y cambiar el parámetro "name"
def get_kit_body(name):
    current_kit_body = data.kit_body.copy()
    current_kit_body["name"] = name
    return current_kit_body


# --- FUNCIONES DE ASERCIÓN REUTILIZABLES ---

# Aserción para casos de prueba positivos (ER: Código 201 y nombres idénticos)
def positive_assert(kit_name):
    kit_body = get_kit_body(kit_name)
    token = get_new_user_token()

    response = sender_stand_request.post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_name


# Aserción para casos de prueba negativos (ER: Código 400)
def negative_assert_code_400(kit_name):
    kit_body = get_kit_body(kit_name)
    token = get_new_user_token()

    response = sender_stand_request.post_new_client_kit(kit_body, token)

    assert response.status_code == 400


# --- AUTOMATIZACIÓN DE LA LISTA DE COMPROBACIÓN ---

# 1. El número permitido de caracteres (1)
def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("a")


# 2. El número permitido de caracteres (511)
def test_create_kit_511_letter_in_name_get_success_response():
    string_511 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcM"
    positive_assert(string_511)


# 3. El número de caracteres es menor que la cantidad permitida (0)
def test_create_kit_empty_name_get_error_response():
    negative_assert_code_400("")


# 4. El número de caracteres es mayor que la cantidad permitida (512)
def test_create_kit_512_letter_in_name_get_error_response():
    string_512 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    negative_assert_code_400(string_512)


# 5. Se permiten caracteres especiales
def test_create_kit_special_characters_in_name_get_success_response():
    positive_assert('"№%@",')


# 6. Se permiten espacios
def test_create_kit_spaces_in_name_get_success_response():
    positive_assert(" A Aaa ")


# 7. Se permiten números
def test_create_kit_numbers_in_name_get_success_response():
    positive_assert("123")


# 8. El parámetro no se pasa en la solicitud
def test_create_kit_no_name_param_get_error_response():
    token = get_new_user_token()
    # Se envía un cuerpo de solicitud totalmente vacío
    empty_body = {}
    response = sender_stand_request.post_new_client_kit(empty_body, token)
    assert response.status_code == 400


# 9. Se ha pasado un tipo de parámetro diferente (número entero)
def test_create_kit_int_type_name_param_get_error_response():
    token = get_new_user_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = 123  # Tipo entero sin comillas

    response = sender_stand_request.post_new_client_kit(kit_body, token)
    assert response.status_code == 400
