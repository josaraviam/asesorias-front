import streamlit as st
import requests

API_URL = "https://asesorias-api.azurewebsites.net"  # Asegúrate de usar la URL correcta de tu API de FastAPI

def create_asesoria(data):
    response = requests.post(f"{API_URL}/asesorias/", json=data)
    if response.status_code != 200:
        st.error(f"Error al crear asesoría: {response.text}")
    else:
        st.success("Asesoría creada exitosamente.")
        return response.json()

def list_asesorias():
    response = requests.get(f"{API_URL}/asesorias/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener la lista de asesorías.")
        return []

def update_asesoria(id, data):
    response = requests.put(f"{API_URL}/asesorias/{id}", json=data)
    if response.status_code == 200:
        st.success("Asesoría actualizada exitosamente.")
        return response.json()
    else:
        st.error(f"Error al actualizar la asesoría: {response.text}")

def delete_asesoria(id):
    response = requests.delete(f"{API_URL}/asesorias/{id}")
    if response.status_code == 200:
        st.success("Asesoría eliminada exitosamente.")
    else:
        st.error(f"Error al eliminar la asesoría: {response.text}")

def main():
    st.title("Gestión de Asesorías")

    with st.form("create_asesoria"):
        st.subheader("Crear nueva asesoría")
        usuario_id = st.text_input("ID del Usuario", help="Ingrese el ID del usuario asociado a la asesoría.")
        titulo = st.text_input("Título", help="Ingrese el título de la asesoría.")
        descripcion = st.text_area("Descripción", help="Ingrese una descripción para la asesoría.")
        fecha = st.date_input("Fecha", help="Seleccione la fecha de la asesoría.")
        hora = st.time_input("Hora", help="Seleccione la hora de la asesoría.")
        profesor = st.text_input("Profesor", help="Ingrese el nombre del profesor para la asesoría.")
        submit = st.form_submit_button("Crear Asesoría")
        if submit:
            asesoria_data = {
                "usuario_id": usuario_id,
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha": str(fecha),
                "hora": str(hora),
                "profesor": profesor
            }
            create_asesoria(asesoria_data)

    st.subheader("Lista de Asesorías")
    asesorias = list_asesorias()
    for asesoria in asesorias:
        st.write(f"{asesoria['id']} - {asesoria['titulo']} - {asesoria['descripcion']}")

    with st.form("update_asesoria"):
        st.subheader("Actualizar Asesoría")
        asesoria_id = st.text_input("ID de Asesoría a Actualizar", key="update_id")
        new_titulo = st.text_input("Nuevo Título", key="new_title")
        update_button = st.form_submit_button("Actualizar Asesoría")
        if update_button:
            update_asesoria(asesoria_id, {"titulo": new_titulo})

    with st.form("delete_asesoria"):
        st.subheader("Eliminar Asesoría")
        delete_id = st.text_input("ID de Asesoría a Eliminar", key="delete_id")
        delete_button = st.form_submit_button("Eliminar Asesoría")
        if delete_button:
            delete_asesoria(delete_id)

if __name__ == "__main__":
    main()
