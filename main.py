import data
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException


# Función utilitaria proporcionada por el repositorio para interceptar el SMS
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string."""
    import json
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # --- CATÁLOGO DE LOCALIZADORES ---
    # 1. Tipo: By.ID
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    phone_input = (By.ID, 'phone')
    sms_code_input = (By.ID, 'code')
    credit_card_number_input = (By.ID, 'number')
    credit_card_cvv_input = (By.CSS_SELECTOR, '.card-code-input #code')  # Resuelve conflicto de ID duplicado con CSS
    comment_input = (By.ID, 'comment')

    # 2. Tipo: By.XPATH
    comfort_tariff_card = (By.XPATH, "//div[contains(@class, 'tcard')]//img[@alt='Comfort']/ancestor::div[contains(@class, 'tcard')]")
    submit_button = (By.XPATH, "//button[contains(@class, 'smart-button')]")
    phone_picker_button = (By.XPATH, "//div[@class='np-text' and text()='Número de teléfono']")
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    sms_confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_picker = (By.XPATH, "//div[@class='pp-text' and text()='Método de pago']")
    add_credit_card_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    link_credit_card_button = (By.XPATH, "//button[text()='Agregar']")
    search_car_modal = (By.XPATH, "//div[contains(@class, 'order-body')]")
    driver_assigned_header = (By.XPATH, "//div[contains(@class, 'order-header-title') and contains(text(), 'El conductor llegará')]")
    # CORRECCIÓN: se cambia de igualdad exacta de clase (@class='payment-picker open')
    # a contains(), ya que la clase compuesta cambia durante las transiciones de cierre.
    close_payment_modal_button = (By.XPATH, "//div[contains(@class,'payment-picker')]//button[contains(@class,'close-button')]")
    modal_overlay = (By.CLASS_NAME, "overlay")

    # 3. Tipo: By.CLASS_NAME
    blanket_and_tissues_checkbox = (By.CLASS_NAME, 'switch-input')

    # 4. Tipo: By.CSS_SELECTOR
    boton_pedir_taxi_inicial = (By.CSS_SELECTOR, "button.button.round")
    ice_cream_plus_button = (By.CSS_SELECTOR, '.counter-plus')
    ice_cream_counter_value = (By.CSS_SELECTOR, '.counter-value')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # --- MÉTODOS DE INTERACCIÓN ---
    def ingresar_direcciones(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def obtener_valor_origen(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def obtener_valor_destino(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def hacer_clic_en_pedir_taxi_inicial(self):
        self.wait.until(EC.element_to_be_clickable(self.boton_pedir_taxi_inicial)).click()

    def seleccionar_tarifa_comfort(self):
        tarifa = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff_card))
        tarifa.click()

    def abrir_modal_telefono(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_picker_button)).click()

    def ingresar_numero_telefono(self, phone):
        self.wait.until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone)
        self.driver.find_element(*self.phone_next_button).click()

    def ingresar_codigo_confirmacion_sms(self, code):
        self.wait.until(EC.visibility_of_element_located(self.sms_code_input)).send_keys(code)
        self.driver.find_element(*self.sms_confirm_button).click()

    def abrir_modal_metodos_pago(self):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_picker)).click()

    def seleccionar_agregar_tarjeta_credito(self):
        self.wait.until(EC.element_to_be_clickable(self.add_credit_card_button)).click()

    def ingresar_datos_tarjeta_y_perder_enfoque(self, number, cvv):
        campo_tarjeta = self.wait.until(EC.visibility_of_element_located(self.credit_card_number_input))
        campo_tarjeta.send_keys(number)
        campo_cvv = self.driver.find_element(*self.credit_card_cvv_input)
        campo_cvv.send_keys(cvv)
        campo_tarjeta.click()

    def click_en_vincular_tarjeta(self):
        self.wait.until(EC.element_to_be_clickable(self.link_credit_card_button)).click()

    def cerrar_modal_pago_con_x(self):
        # CORRECCIÓN: reintento activo por si el botón todavía no es clickeable
        # justo tras vincular la tarjeta (animación de confirmación en curso).
        boton_cerrar = self._click_con_reintento(self.close_payment_modal_button)
        # CORRECCIÓN: tras cerrar, espera explícitamente a que el overlay
        # de este modal desaparezca antes de continuar con el flujo.
        try:
            self.wait.until(EC.invisibility_of_element_located(self.modal_overlay))
        except TimeoutException:
            # Si el overlay no desaparece a tiempo, seguimos: el reintento
            # de agregar_dos_helados se encargará de manejar la intercepción.
            pass

    def escribir_mensaje_al_conductor(self, message):
        self.wait.until(EC.visibility_of_element_located(self.comment_input)).send_keys(message)

    def activar_manta_y_pañuelos(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self.blanket_and_tissues_checkbox))
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

    def _click_con_reintento(self, locator, intentos=6, espera=0.5):
        """
        Intenta hacer clic de forma normal varias veces; si el elemento sigue
        siendo interceptado por un overlay residual, recurre a un clic vía
        JavaScript como último recurso, ignorando el elemento superpuesto.
        """
        ultimo_error = None
        for _ in range(intentos):
            try:
                elemento = self.wait.until(EC.element_to_be_clickable(locator))
                elemento.click()
                return elemento
            except ElementClickInterceptedException as e:
                ultimo_error = e
                time.sleep(espera)

        # Último recurso: clic forzado por JavaScript
        elemento = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", elemento)
        return elemento

    def agregar_dos_helados(self):
        # Espera explícitamente a que desaparezcan overlays oscuros antes de interactuar con los helados
        try:
            self.wait.until(EC.invisibility_of_element_located(self.modal_overlay))
        except TimeoutException:
            pass  # el reintento de clic maneja la posible intercepción de todas formas

        self._click_con_reintento(self.ice_cream_plus_button)
        self._click_con_reintento(self.ice_cream_plus_button)

    def obtener_cantidad_helados(self):
        return self.wait.until(EC.visibility_of_element_located(self.ice_cream_counter_value)).text

    def confirmar_pedido_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def verificar_aparicion_modal_busqueda(self):
        return self.wait.until(EC.visibility_of_element_located(self.search_car_modal)).is_displayed()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def test_flujo_completo_pedir_taxi(self):
        page = UrbanRoutesPage(self.driver)
        try:
            self.driver.get(data.urban_routes_url)

            # 1. Configurar direcciones
            page.ingresar_direcciones(data.address_from, data.address_to)
            assert page.obtener_valor_origen() == data.address_from
            assert page.obtener_valor_destino() == data.address_to

            # Abrir panel de tarifas
            page.hacer_clic_en_pedir_taxi_inicial()

            # 2. Seleccionar tarifa Comfort
            page.seleccionar_tarifa_comfort()

            # 3. Rellenar número de teléfono
            page.abrir_modal_telefono()
            page.ingresar_numero_telefono(data.phone_number)
            sms_code = retrieve_phone_code(self.driver)
            page.ingresar_codigo_confirmacion_sms(sms_code)

            # 4. Agregar una tarjeta de crédito
            page.abrir_modal_metodos_pago()
            page.seleccionar_agregar_tarjeta_credito()
            page.ingresar_datos_tarjeta_y_perder_enfoque(data.card_number, data.card_code)
            page.click_en_vincular_tarjeta()
            page.cerrar_modal_pago_con_x()

            # 5. Escribir un mensaje para el conductor
            page.escribir_mensaje_al_conductor(data.message_for_driver)

            # 6. Pedir manta y pañuelos
            page.activar_manta_y_pañuelos()

            # 7. Pedir 2 helados
            page.agregar_dos_helados()
            assert page.obtener_cantidad_helados() == "2"

            # 8. Comprobar que aparece el modal para buscar taxi
            page.confirmar_pedido_taxi()
            assert page.verificar_aparicion_modal_busqueda() is True

        except Exception:
            # CORRECCIÓN: captura de evidencia automática en caso de fallo,
            # útil para depurar sin tener que re-ejecutar todo el flujo.
            self.driver.save_screenshot('fallo_debug.png')
            with open('fallo_debug.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            raise

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()