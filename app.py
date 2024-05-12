import streamlit as st
import requests
from passlib.context import CryptContext

# Configurar el contexto de passlib para manejo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
API_URL = "https://asesorias-api.azurewebsites.net"

def obtener_usuario_por_username(username):
    """Obtiene un usuario por nombre de usuario de la API."""
    response = requests.get(f"{API_URL}/usuarios/username/{username}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("No se pudo obtener el usuario")
        return None

def verificar_usuario(username, password):
    """Verifica las credenciales del usuario contra la información obtenida de la API."""
    user = obtener_usuario_por_username(username)
    if user and pwd_context.verify(password, user['password']):
        return True
    return False

def registrar_usuario(data):
    """Envía los datos del usuario a la API para registrar un nuevo usuario."""
    response = requests.post(f"{API_URL}/usuarios/", json=data)
    if response.status_code == 200:
        st.success("Usuario registrado exitosamente.")
    else:
        st.error(f"Error al registrar usuario: {response.text}")

def pagina_registro():
    """Página de registro de usuario."""
    with st.form("form_registro"):
        st.write("Registro de nuevo usuario")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        email = st.text_input("Email")
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input("Confirmar contraseña", type="password")

        submit = st.form_submit_button("Registrar")
        if submit:
            if password == confirm_password:
                data = {
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "username": username,
                    "password": password  # El hashing debe hacerse en el servidor
                }
                registrar_usuario(data)
            else:
                st.error("Las contraseñas no coinciden.")

def listar_asesorias(usuario_id):
    """Lista las asesorías del usuario."""
    response = requests.get(f"{API_URL}/asesorias", params={"usuario_id": usuario_id})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener asesorías.")
        return []

def pagina_asesorias():
    """Página que muestra las asesorías del usuario."""
    st.write("Tus Asesorías")
    if 'usuario_id' in st.session_state:
        asesorias = listar_asesorias(st.session_state['usuario_id'])
        for asesoria in asesorias:
            st.subheader(asesoria['titulo'])
            st.write("Descripción:", asesoria['descripcion'])
            st.write("Fecha:", asesoria['fecha'])
            st.write("Hora:", asesoria['hora'])
            st.write("Profesor:", asesoria['profesor'])

def main():
    st.sidebar.title("Navegación")
    choice = st.sidebar.radio("Menu", ["Iniciar sesión", "Registro"])

    if choice == "Iniciar sesión":
        username = st.sidebar.text_input("Nombre de usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Login"):
            if verificar_usuario(username, password):
                st.session_state['usuario'] = username  # Mantener estado de sesión
                st.success("Inicio de sesión exitoso")
            else:
                st.error("Nombre de usuario o contraseña incorrectos")
        if 'usuario' in st.session_state:
            st.write(f"Bienvenido, {st.session_state['usuario']}!")
        else:
            st.info("Por favor, inicia sesión para continuar.")

    elif choice == "Registro":
        pagina_registro()
    elif choice == "Ver Asesorías":
        if 'usuario_id' in st.session_state:
            pagina_asesorias()
        else:
            st.warning("Por favor, inicia sesión para ver tus asesorías.")

if __name__ == "__main__":
    main()
