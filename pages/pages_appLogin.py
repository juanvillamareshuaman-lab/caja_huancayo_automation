import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from library.word_generate import add_image_to_word, generate_word_stub
from library.utils import hide_keyboard, input_teclado_dinamico
from pages.Objects import excelObjects
from appium.webdriver.common.appiumby import AppiumBy


class APP_LOGIN:

    lblTextoIncial = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.cajahuancayo.cajahuancayo.appcajahuancayo:id/texto_cargando"]')
    input_doc      = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.cajahuancayo.cajahuancayo.appcajahuancayo:id/texto_cargando"]')
    input_password = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.cajahuancayo.cajahuancayo.appcajahuancayo:id/texto_cargando"]')
    btn_ojo        = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.cajahuancayo.cajahuancayo.appcajahuancayo:id/texto_cargando"]')
    btn_ingresar   = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.cajahuancayo.cajahuancayo.appcajahuancayo:id/texto_cargando"]')



    def __init__(self, context):
        self.context = context

    def get_data(self):
        return self.context.data_excel  # Ahora usa context.data_excel

    def Validar_inicio_App(self, logWord=True, timeout=15):
        try:
            wait = WebDriverWait(self.context.mdriver, timeout)
            lblElemento = wait.until(EC.presence_of_element_located(self.lblTextoIncial))

            if lblElemento.text == "Cargando datos":
                print("[LOG] Se valida correctamente el texto inicial al abrir la app")

            if logWord:
                generate_word_stub(f"Se valida el texto inicial -> {lblElemento.text}")
                img = add_image_to_word(self.context.mdriver)
                self.context.nameImg.append(img)

        except (NoSuchElementException, TimeoutException) as e:
            self.context.mdriver.save_screenshot("evidencias/error_lblTextoInicial.png")
            raise AssertionError(f"[ERROR] No se encontró el lblTextoIncial: {e}")


    def ingresar_nro_doc(self, datos, logWord=True):
        try:
            fila = self.get_data()[int(datos)-1]  # fila como diccionario
            nroDoc = fila[excelObjects.columnNroDoc]
            wait = WebDriverWait(self.context.mdriver, 8)
            input_doc = wait.until(EC.element_to_be_clickable(self.input_doc))
            input_doc.click()
            input_doc.send_keys(str(nroDoc))
            hide_keyboard(self.context.mdriver)
            if logWord:
                generate_word_stub(f"Se ingresa número de Documento -> {nroDoc}")
                img = add_image_to_word(self.context.mdriver)
                self.context.nameImg.append(img)
        except (NoSuchElementException, TimeoutException) as e:
            raise AssertionError(f"[ERROR] No se encontró el campo de documento: {e}")

    def ingresar_password(self, datos, noHappy="False", logWord=True):
        try:
            fila = self.get_data()[int(datos)-1]
            password = str(fila[excelObjects.columnPassword])
            wait = WebDriverWait(self.context.mdriver, 8)
            input_pass = wait.until(EC.element_to_be_clickable(self.input_password))
            input_pass.click()
            input_teclado_dinamico(self.context, password)
            try:
                if self.context.mdriver.is_keyboard_shown():
                    self.context.mdriver.hide_keyboard()
            except Exception:
                pass
            if logWord:
                generate_word_stub("Se ingresa contraseña")
                img = add_image_to_word(self.context.mdriver)
                self.context.nameImg.append(img)
        except (NoSuchElementException, TimeoutException) as e:
            raise AssertionError(f"[ERROR] No se encontró el campo de contraseña: {e}")

    def click_ojo(self, logWord=True):
        try:
            self.context.mdriver.find_element(*self.btn_ojo).click()
            if logWord:
                generate_word_stub("Se da click en el ojo para ver contraseña")
                img = add_image_to_word(self.context.mdriver)
                self.context.nameImg.append(img)
        except Exception:
            pass

    def click_ingresar(self, logWord=True):
        try:
            try:
                if self.context.mdriver.is_keyboard_shown():
                    self.context.mdriver.hide_keyboard()
            except Exception:
                pass
            btn = self.context.mdriver.find_element(*self.btn_ingresar)
            btn.click()
            if logWord:
                generate_word_stub("Se da click en ingresar")
                img = add_image_to_word(self.context.mdriver)
                self.context.nameImg.append(img)
        except NoSuchElementException:
            raise AssertionError("[ERROR] No se encontró el botón ingresar")
