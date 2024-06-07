FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Elimina esta línea: RUN python Drawing_App.py

EXPOSE 8000


CMD web: python drawing_app.py
# CMD ["python", "main.py"]  # Comenté esta línea porque no sé si tienes un archivo main.py

# No olvides ejecutar el comando para iniciar tu aplicación cuando ejecutes el contenedor
# Ejecuta el comando adecuado en tu terminal cuando quieras ejecutar el contenedor.
