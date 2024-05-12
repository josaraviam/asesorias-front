import streamlit as st
import requests

API_URL = "https://asesorias-api.azurewebsites.net"

def login(username, password):
    """Función para autenticar a un usuario."""
    response = requests.post(f"{API_URL}/auth/token", data={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fallo al iniciar sesión.")
        return None


def create_user(nombre, apellido, email, username, password):
    """Función para registrar un nuevo usuario."""
    response = requests.post(f"{API_URL}/usuarios", json={
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        st.success("Usuario creado exitosamente.")
    elif response.status_code == 204:
        st.info("No se devolvió contenido.")
    else:
        try:
            # Intentamos obtener el mensaje de error detallado, si está disponible
            error_detail = response.json().get("detail", "Error desconocido al crear el usuario.")
        except ValueError:
            # No se pudo decodificar JSON, manejamos el caso genérico
            error_detail = "Error sin respuesta detallada del servidor."
        st.error(f"Error al crear el usuario: {error_detail}")


def get_asesorias(token):
    """Función para obtener las asesorías del usuario autenticado."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/asesorias", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener asesorías.")
        return []

def create_asesoria(token, title, description):
    """Función para crear una nueva asesoría."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/asesorias", json={
        "title": title,
        "description": description
    }, headers=headers)
    if response.status_code == 200:
        st.success("Asesoría creada exitosamente.")
    else:
        st.error("Error al crear la asesoría.")

def delete_asesoria(token, asesoria_id):
    """Función para eliminar una asesoría."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_URL}/asesorias/{asesoria_id}", headers=headers)
    if response.status_code == 204:
        st.success("Asesoría eliminada correctamente.")
    else:
        st.error("Error al eliminar la asesoría.")

def app():
    st.sidebar.title("Navegación")
    menu = ["Inicio", "Registro", "Login", "Mis Asesorías"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Inicio":
        st.subheader("Bienvenido a la plataforma de Asesorías Académicas")

        # En la sección de registro:
    elif choice == "Registro":
        with st.form("Formulario de Usuario"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            email = st.text_input("Correo Electrónico")
            username = st.text_input("Nombre de Usuario")
            password = st.text_input("Contraseña", type="password")
            submit_button = st.form_submit_button("Registrar Usuario")
            if submit_button:
                create_user(nombre, apellido, email, username, password)


    elif choice == "Login":
        with st.form("Formulario de Login"):
            username = st.text_input("Nombre de Usuario")
            password = st.text_input("Contraseña")
            submit_button = st.form_submit_button("Iniciar Sesión")
            if submit_button:
                token_response = login(username, password)
                if token_response:
                    st.session_state['token'] = token_response['access_token']
                    st.success("Inicio de sesión exitoso!")
                    st.experimental_rerun()

    elif choice == "Mis Asesorías":
        if 'token' in st.session_state:
            asesorias = get_asesorias(st.session_state['token'])
            for asesoria in asesorias:
                st.write(f"Titulo: {asesoria['title']}")
                st.write(f"Descripción: {asesoria['description']}")
                if st.button(f"Eliminar {asesoria['title']}"):
                    delete_asesoria(st.session_state['token'], asesoria['id'])
            with st.form("Crear Asesoría"):
                title = st.text_input("Título")
                description = st.text_area("Descripción")
                submit_button = st.form_submit_button("Crear Asesoría")
                if submit_button:
                    create_asesoria(st.session_state['token'], title, description)
        else:
            st.warning("Por favor, inicia sesión para ver tus asesorías.")

if __name__ == "__main__":
    app()
