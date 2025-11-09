import streamlit as st
from groq import Groq

st.title("Aplicación de Chat con IA")

modelos = ['llama-3.3-70b-versatile']

def configurarPagina():

    st.title("NeuroChat")
    st.set_page_config(page_title="NeuroChat", page_icon="🌸", layout="centered")
    st.sidebar.title("Configuración")
    elegirModelo = st.sidebar.selectbox("Elige un modelo de IA", options=modelos, index=0)
    return elegirModelo

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Bienvenido a mi aplicación de Streamlit.")

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""

    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():

    modelo  = configurarPagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

    mensaje = st.chat_input("Escribe tu mensaje aquí...")
    area_chat()

    chat_completo = None

    if mensaje:
        actualizar_historial("user", mensaje, "😋")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
            actualizar_historial("assistant", respuesta_completa, "🌸")
            st.rerun()


if __name__ == "__main__":
    main()