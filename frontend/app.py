import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Clasificador de Mensajes", layout="wide")

# Título
st.title("📨 Clasificador de Mensajes con IA")
st.markdown("""
Clasifica tus mensajes en categorías: **Urgente**, **Normal** o **Moderado**.
""")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    api_url = st.text_input(
        "URL de la API", 
        value="http://127.0.0.1:8000/classify/",
        help="URL del endpoint de clasificación"
    )
    st.markdown("---")
    st.markdown("**Instrucciones:**")
    st.markdown("1. Escribe o pega tu mensaje")
    st.markdown("2. Haz clic en 'Clasificar'")
    st.markdown("3. Revisa los resultados")

# Función para establecer ejemplos
def set_example_text(example_text):
    st.session_state.message_text = example_text

# Ejemplos de mensajes
examples = [
    "¡El servidor está caído! Necesitamos acción inmediata.",
    "La reunión de mañana se ha pospuesto para el viernes.",
    "Podrías revisar este documento cuando tengas un momento."
]

# Mostrar ejemplos como botones
st.markdown("### Ejemplos para probar:")
cols = st.columns(len(examples))
for i, example in enumerate(examples):
    with cols[i]:
        st.button(
            f"Ejemplo {i+1}",
            on_click=set_example_text,
            args=(example,),
            key=f"example_{i}",
            help=example 
        )

# Entrada de texto con valor inicial del session_state
message = st.text_area(
    "Escribe tu mensaje aquí:",
    height=150,
    value=st.session_state.get("message_text", ""),
    key="message_input"
)

if st.button("Clasificar Mensaje"):
    if not message.strip():
        st.warning("Por favor ingresa un mensaje para clasificar")
    else:
        with st.spinner("Clasificando mensaje..."):
            try:
                response = requests.post(
                    api_url,
                    json={"text": message}
                )
                if response.status_code == 200:
                    result = response.json()
                    
                    # Mostrar resultados
                    st.success("¡Mensaje clasificado!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 📝 Mensaje original")
                        st.info(message)
                    
                    with col2:
                        st.markdown("### 🏷️ Clasificación")
                        label = result["classification"]
                        confidence = result["confidence"] * 100
                        
                        if label == "Urgente":
                            st.error(f"🔴 **{label}** (Confianza: {confidence:.1f}%)")
                        elif label == "Normal":
                            st.success(f"🟢 **{label}** (Confianza: {confidence:.1f}%)")
                        else:
                            st.warning(f"🟡 **{label}** (Confianza: {confidence:.1f}%)")
                    
                    # Visualización de confianza
                    st.markdown("### 📊 Confianza por categoría")
                    
                    scores = result["all_scores"]
                    df = pd.DataFrame({
                        "Categoría": list(scores.keys()),
                        "Confianza": [score * 100 for score in scores.values()]
                    }).sort_values("Confianza", ascending=False)
                    
                    fig = px.bar(
                        df,
                        x="Categoría",
                        y="Confianza",
                        color="Categoría",
                        text="Confianza",
                        color_discrete_map={
                            "Urgente": "red",
                            "Normal": "green",
                            "Moderado": "orange"
                        }
                    )
                    
                    fig.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside'
                    )
                    fig.update_layout(
                        yaxis_title="Confianza (%)",
                        xaxis_title="Categoría",
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.error(f"Error en la API: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")
            except Exception as e:
                st.error(f"Error inesperado: {str(e)}")

# Nota para el usuario
st.markdown("---")
st.caption("ℹ️ Haz clic en los ejemplos para probar el clasificador automáticamente")