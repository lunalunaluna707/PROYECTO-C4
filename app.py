from flask import Flask, render_template, send_from_directory
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

class MiDiagrama(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("diagrama.puml"):
            print("Generando imagen...")
            imagen_modificada()

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def imagen_modificada():
    archivo = os.path.abspath('diagrama.puml') 
    imagenDiagrama = os.path.abspath('static/diagrama.png')  
    jar_path = os.path.abspath('static/plantuml.jar')  
    print(f"Ruta del archivo .puml: {archivo}")
    print(f"Ruta del JAR: {jar_path}")

    comando = f'java -jar "{jar_path}" "{archivo}" -o static'

    try:
        subprocess.run(comando, shell=True, check=True)
        if os.path.exists(imagenDiagrama):
            print(f"Imagen generada: {imagenDiagrama}")
        else:
            print("Error al generar la imagen")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar comando: {e}")


if __name__ == '__main__':
    event_handler = MiDiagrama()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    app.run(debug=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
