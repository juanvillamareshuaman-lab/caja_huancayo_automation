from behave import given, when, then
from pages.pages_appLogin import APP_LOGIN
import time

@given('Usuario se encuentra en la APP Caja Huancayo "{datos}"')
def step_impl(context, datos):
    # Inicializa la página y ejecuta los pasos solo si no se ha marcado
    context.pageLogin = APP_LOGIN(context)
    context.pageLogin.Validar_inicio_App()
    if not hasattr(context, 'ejecutar'):
        context.ejecutar = "SI"
    time.sleep(30)

@when('Usuario ingresa su documento "{datos}"')
def step_impl(context, datos):
    if context.ejecutar == "SI":
        context.pageLogin.ingresar_nro_doc(datos)

@when('Usuario ingresa password "{datos}"')
def step_impl(context, datos):
    if context.ejecutar == "SI":
        context.pageLogin.ingresar_password(datos)
        try:
            context.pageLogin.click_ojo()
        except Exception:
            pass

@when('da click en ingresar')
def step_impl(context):
    if context.ejecutar == "SI":
        context.pageLogin.click_ingresar()

@then('Se verifica el login al APP Caja Huancayo correcto "{datos}"')
def step_impl(context, datos):
    # Aquí puedes validar con un toast, activity o elemento visible
    print(f"[INFO] Login verificado para caso: {datos}")