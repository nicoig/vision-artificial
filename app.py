# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/ChatPDF.git
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

################################################


import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# Función para codificar la imagen en base64
def encode_image(image_file):
    _, ext = os.path.splitext(image_file.name)
    if ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        raise ValueError("Invalid image format")
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    return f"data:{mime};base64,{base64_image}"

# Streamlit application layout
st.title("Visión Artificial NG")

# Upload the image
uploaded_file = st.file_uploader("Carga una imagen", type=['jpg', 'jpeg', 'png'])
input_text = st.text_input("Ingrese su pregunta aquí")
submit_button = st.button("Enviar")

# API Key
api_key = os.getenv('OPENAI_API_KEY')


if submit_button and uploaded_file is not None:
    # Encode the uploaded image
    base64_image = encode_image(uploaded_file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": input_text
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": base64_image
                }
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    # Send POST request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()

    # Extraer solo el 'content' del resultado
    content = result['choices'][0]['message']['content'] if result['choices'] else 'No se encontró contenido'

    # Mostrar el 'content' en Streamlit
    st.write(content)

# Run the streamlit application by typing `streamlit run app.py` in your terminal.
