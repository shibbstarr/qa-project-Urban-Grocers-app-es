# Cabeceras base para las solicitudes
headers = {
    "Content-Type": "application/json"
}

# Cuerpo base para la creación de usuarios (Necesario para obtener el authToken)
user_body = {
    "firstName": "Andrea",
    "phone": "+11234567890",
    "address": "123 Main Street"
}

# Cuerpo base para la creación de kits
kit_body = {
    "name": "Mi Kit"
}