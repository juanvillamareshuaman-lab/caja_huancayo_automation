import os
from datetime import datetime
from behave import fixture, use_fixture
from appium import webdriver
from appium.options.android import UiAutomator2Options
import configparser

# ===============================
# 📦 IMPORTS SEGÚN TU ESTRUCTURA
# ===============================
from library.word_generate import start_up_word, end_to_word
from library.utils import *
from library.config_mobile import AppConfig
from library.excel_reader import read_excel
# ===============================
# ⚙️ VARIABLES GLOBALES
# ===============================
contador_ejecuciones = 0

# ===============================
# 📱 LECTURA DE CONFIGURACIÓN
# ===============================
def load_properties():
    """Carga el archivo mobile.properties"""
    config = configparser.ConfigParser()
    config.read('mobile.properties')
    return config

def get_device_and_app(config):
    """Obtiene el dispositivo y aplicación desde mobile.properties"""
    device = config.get('kobiton', 'username')
    app_name = config.get('kobiton', 'aplicacion')
    return device, app_name

# ===============================
# 📲 FIXTURE PRINCIPAL (Kobiton)
# ===============================
@fixture
def init_kobiton(context, app_config, app_name):
    """Inicializa el driver Appium conectado a Kobiton"""
    try:
        print("🌐 Conectando con Kobiton...")

        # Configuración específica de la app Caja Huancayo
        app_config['appPackage'] = 'com.cajahuancayo.app'
        app_config['appActivity'] = 'com.cajahuancayo.app.ui.splash.SplashActivity'
        context.app = app_config['appPackage']

        # Opciones de Appium 2.x
        options = UiAutomator2Options().load_capabilities(app_config)

        # URL de conexión remota Kobiton desde AppConfig
        kobiton_server = app_config['kobiton_server_url']

        # Inicia la sesión remota
        context.mdriver = webdriver.Remote(
            command_executor=kobiton_server,
            options=options
        )

        print("✅ Conectado correctamente a Kobiton y a la app Caja Huancayo.")
        yield context.mdriver

    except Exception as e:
        print(f"❌ Error al inicializar Appium con Kobiton: {e}")
        raise

# ===============================
# 🔄 HOOKS BEHAVE
# ===============================
# features/environment.py


def before_all(context):
    """Configuración global antes de ejecutar las pruebas"""
    print("📲 Inicializando entorno Caja Huancayo - Kobiton...")

    # Cargar propiedades y dispositivo
    config = load_properties()
    device, app_name = get_device_and_app(config)

    # Validar existencia del dispositivo configurado
    if hasattr(AppConfig, device):
        app_config = getattr(AppConfig, device)
        use_fixture(init_kobiton, context,
                    app_config=app_config,
                    app_name=app_name)
    else:
        raise Exception(f"⚠️ El dispositivo '{device}' no existe en AppConfig.")

    # ===== Leer Excel y guardarlo en context =====
    excel_file = "data.xlsx"   # archivo dentro de resources
    sheet_name = "Sheet1"      # hoja que quieras leer
    context.data_excel = read_excel(excel_file, sheet_name)
    print(f"✅ Datos de prueba cargados desde resources/{excel_file}, hoja {sheet_name}")


def before_scenario(context, scenario):
    global contador_ejecuciones
    contador_ejecuciones += 1

    print(f"\n🚀 Iniciando escenario #{contador_ejecuciones}: {scenario.name}")
    context.start_time = datetime.now()
    context.name_scenario = scenario.name
    start_up_word(scenario.name)
    context.step_img = []

def after_scenario(context, scenario):
    print(f"✅ Finalizó escenario: {scenario.name} ({scenario.status.name})")

    try:
        end_to_word(scenario.status.name, context)
    except Exception as e:
        print(f"⚠️ Error al generar reporte Word: {e}")

    try:
        app_pkg = context.mdriver.capabilities.get('appPackage')
        if app_pkg:
            context.mdriver.terminate_app(app_pkg)
            print("🛑 Aplicación cerrada correctamente.")
    except Exception as e:
        print(f"⚠️ Error al cerrar app: {e}")

def after_all(context):
    print("\n📴 Finalizando entorno global Caja Huancayo...")
    try:
        if hasattr(context, 'mdriver'):
            context.mdriver.quit()
            print("✅ Driver cerrado correctamente en Kobiton.")
    except Exception as e:
        print(f"⚠️ Error al cerrar driver: {e}")

def before_step(context, step):
    context.nameImg = []

def after_step(context, step):
    step_img = {
        'scenario_name': context.name_scenario,
        'step_name': step.name,
        'imagen': context.nameImg
    }
    context.step_img.append(step_img)
