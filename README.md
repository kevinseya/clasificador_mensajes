# 📨 Clasificador de Mensajes con IA

## Descripción
Aplicación web para clasificar mensajes de texto en categorías de prioridad (Urgente, Normal, Moderado) utilizando inteligencia artificial.

![Captura de pantalla 2025-06-06 151824](https://github.com/user-attachments/assets/8d7428a1-2670-4c5b-bd20-b84417040385)


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
