# 📨 Clasificador de Mensajes con IA

## Descripción
Aplicación web para clasificar mensajes de texto en categorías de prioridad (Urgente, Normal, Moderado) utilizando inteligencia artificial.



## 🚀 Características
- Clasificación automática de mensajes
- Interfaz intuitiva con Streamlit
- API REST con FastAPI
- Modelo BART-large-MNLI de Hugging Face
- Visualización gráfica de resultados

## 📦 Instalación

1. Clonar repositorio:
```bash
git clone https://github.com/kevinseya/clasificador-mensajes.git
cd clasificador-mensajes
```
2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
3. Instalar Dependencias:
```bash
pip install -r requirements.txt
```
4. Configurar variables:
```bash
cp .env.example .env
# Editar .env con tu token de Hugging Face
```
## 🏃 Uso
Iniciar Backend:
```bash
cd backend
uvicorn main:app --reload
```
Iniciar Frontend:
```bash
cd frontend
streamlit run app.py
```
## 🛠️ Tecnologías
Python 3.8+
Streamlit
FastAPI
HuggingFace Transformers
Plotly