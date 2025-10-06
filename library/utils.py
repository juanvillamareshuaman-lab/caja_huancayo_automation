import time

def hide_keyboard(driver):
    try:
        driver.hide_keyboard()
    except Exception:
        pass


def input_teclado_dinamico(context, text):
    """
    Envía texto al campo activo, adaptado para Appium 5.x (sin TouchAction).
    Si tu app usa teclado personalizado, puedes ajustar el script 'mobile: type'.
    """
    driver = context.mdriver
    try:
        active = driver.switch_to.active_element
        active.send_keys(text)
    except Exception:
        # Intento alternativo con comando 'mobile: type'
        try:
            driver.execute_script('mobile: type', {'text': text})
        except Exception:
            # Último intento: buscar nuevamente el elemento enfocado
            try:
                el = driver.switch_to.active_element
                el.send_keys(text)
            except Exception:
                raise
