import streamlit as st
import requests
from passlib.context import CryptContext
import pandas as pd

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

def obtener_usuario_id_por_username(username):
    """Obtiene el usuario por nombre de usuario de la API y devuelve el ID del usuario."""
    response = requests.get(f"{API_URL}/usuarios/username/{username}")
    if response.status_code == 200:
        usuario = response.json()
        return usuario['id']
    else:
        st.error("No se pudo obtener el ID del usuario")
        return None

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

def listar_asesorias_por_usuario(username):
    """Obtiene asesorías del usuario por nombre de usuario de la API."""
    response = requests.get(f"{API_URL}/asesorias/by-username/{username}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener asesorías: {response.text}")
        return []


def pagina_asesorias(username):
    """Página que muestra las asesorías del usuario."""
    st.write("Tus Asesorías")
    asesorias = listar_asesorias_por_usuario(username)
    if asesorias:
        for asesoria in asesorias:
            st.write(f"Titulo: {asesoria['titulo']}, Fecha: {asesoria['fecha']}, Hora: {asesoria['hora']}")
    else:
        st.write("No tienes asesorías registradas.")

def agregar_asesoria(data):
    """Envía los datos de la nueva asesoría a la API."""
    response = requests.post(f"{API_URL}/asesorias", json=data)
    if response.status_code == 200:
        st.success("Asesoría agregada exitosamente.")
    else:
        st.error(f"Error al agregar asesoría: {response.text}")

def pagina_agregar_asesoria(username):
    """Página para agregar una nueva asesoría."""
    usuario_id = obtener_usuario_id_por_username(username)  # Obtener el ID del usuario
    with st.form("form_asesoria"):
        st.write("Agregar nueva asesoría")
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        profesor = st.text_input("Profesor")
        submit = st.form_submit_button("Agregar Asesoría")
        if submit:
            data = {
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha": fecha.isoformat(),
                "hora": hora.strftime("%H:%M"),
                "profesor": profesor,
                "usuario_id": usuario_id
            }
            agregar_asesoria(data)

def actualizar_asesoria(asesoria_id, data):
    """Envía los datos actualizados de la asesoría a la API."""
    response = requests.put(f"{API_URL}/asesorias/{asesoria_id}", json=data)
    if response.status_code == 200:
        st.success("Asesoría actualizada exitosamente.")
    else:
        st.error(f"Error al actualizar asesoría: {response.text}")

def obtener_asesoria_por_id(asesoria_id):
    """Obtiene una asesoría específica por ID desde la API."""
    response = requests.get(f"{API_URL}/asesorias/{asesoria_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Asesoría no encontrada.")
        return None


def pagina_editar_asesoria(asesoria_id):
    """Página para editar una asesoría existente."""
    asesoria = obtener_asesoria_por_id(asesoria_id)
    if asesoria:
        with st.form("form_editar_asesoria"):
            st.write("Editar asesoría")
            titulo = st.text_input("Título", value=asesoria['titulo'])
            descripcion = st.text_area("Descripción", value=asesoria['descripcion'])
            fecha = st.date_input("Fecha", value=pd.to_datetime(asesoria['fecha']))
            hora = st.time_input("Hora", value=pd.to_datetime(asesoria['hora']).time())
            profesor = st.text_input("Profesor", value=asesoria['profesor'])
            submit = st.form_submit_button("Actualizar Asesoría")
            if submit:
                updated_data = {
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "fecha": fecha.isoformat(),
                    "hora": hora.strftime("%H:%M"),
                    "profesor": profesor,
                    "usuario_id": asesoria['usuario_id']  # Asegúrate de incluir el usuario_id si es necesario
                }
                actualizar_asesoria(asesoria_id, updated_data)
    else:
        st.error("No se pudo cargar la asesoría para editar.")

def eliminar_asesoria(asesoria_id):
    """Elimina una asesoría específica mediante su ID."""
    response = requests.delete(f"{API_URL}/asesorias/{asesoria_id}")
    if response.status_code == 200:
        st.success("Asesoría eliminada exitosamente.")
    else:
        st.error("Error al eliminar la asesoría.")


def main():
    st.sidebar.title("Navegación")

    if 'usuario' in st.session_state:
        choice = st.sidebar.radio("Menu", ["Inicio", "Agregar Asesoría", "Cerrar Sesión"])
    else:
        choice = st.sidebar.radio("Menu", ["Iniciar sesión", "Registro"])

    if choice == "Iniciar sesión":
        if 'usuario' not in st.session_state:
            username = st.sidebar.text_input("Nombre de usuario", key="username")
            password = st.sidebar.text_input("Contraseña", type="password", key="password")
            if st.sidebar.button("Login", key="login"):
                if verificar_usuario(username, password):
                    st.session_state['usuario'] = username  # Mantener estado de sesión
                    st.experimental_rerun()  # Forzar la recarga de la página para actualizar la barra lateral
                else:
                    st.error("Nombre de usuario o contraseña incorrectos")
        else:
            st.info("Ya has iniciado sesión.")
            pagina_asesorias(st.session_state['usuario'])

    elif choice == "Registro":
        pagina_registro()

    elif 'usuario' in st.session_state:
        if choice == "Inicio":
            pagina_asesorias(st.session_state['usuario'])
        elif choice == "Agregar Asesoría":
            pagina_agregar_asesoria(st.session_state['usuario'])
        elif choice == "Cerrar Sesión":
            del st.session_state['usuario']  # Limpiar el estado de sesión
            st.experimental_rerun()  # Forzar la recarga de la página para eliminar el estado de sesión

if __name__ == "__main__":
    main()
