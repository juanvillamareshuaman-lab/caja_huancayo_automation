import os
import random
from datetime import datetime
from docx import Document

# ===========================================================
# Funciones base que ya tienes
# ===========================================================

def generate_word_stub(text):
    """Salida simple al log, útil para depuración."""
    print(f"[WORD] {text}")


def add_image_to_word(driver):
    """Captura un pantallazo de la app y lo guarda localmente."""
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    seq = random.randint(1000, 9999)
    name = f"screenshot_{seq}.png"
    path = os.path.join(screenshots_dir, name)
    try:
        screenshot = driver.get_screenshot_as_png()
        with open(path, "wb") as f:
            f.write(screenshot)
    except Exception:
        # Si el driver no está disponible, crea un archivo vacío
        with open(path, "wb") as f:
            f.write(b"")
    return path

# ===========================================================
# Funciones requeridas por environment.py
# ===========================================================

def start_up_word(scenario_name):
    """
    Inicializa un archivo Word para el escenario actual.
    Se ejecuta al inicio del escenario en environment.py
    """
    os.makedirs("evidencias", exist_ok=True)
    file_path = os.path.join("evidencias", f"{scenario_name.replace(' ', '_')}.docx")

    document = Document()
    document.add_heading(f"Escenario: {scenario_name}", level=1)
    document.add_paragraph(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    document.save(file_path)

    print(f"[WORD] Documento inicial creado: {file_path}")
    return file_path


def end_to_word(status, context):
    """
    Cierra y completa el documento Word al finalizar el escenario.
    """
    try:
        evidencias_dir = "evidencias"
        # Buscar el documento correspondiente
        for filename in os.listdir(evidencias_dir):
            if filename.endswith(".docx"):
                path = os.path.join(evidencias_dir, filename)
                doc = Document(path)
                doc.add_paragraph(f"Estado final del escenario: {status}")
                doc.add_paragraph(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                doc.save(path)
                print(f"[WORD] Documento actualizado con estado final: {status}")
    except Exception as e:
        print(f"⚠️ Error al cerrar documento Word: {e}")
