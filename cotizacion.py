import time
from datetime import date
from dateutil.relativedelta import relativedelta
# Importamos la función de login desde el otro archivo
from automatizacion import login_and_get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Llama a la función de login para obtener un driver ya autenticado
driver = login_and_get_driver()

# Agregamos la lógica para calcular la fecha de fin
today = date.today()
fecha_fin = today + relativedelta(years=2)
print(f"La fecha de finalización será: {fecha_fin}")

if driver:
    print("Login exitoso. Iniciando proceso de cotización...")
    try:
        #Paso 1: Esperar y hacer clic en el botón desplegable "Suscripción y Cotización"
        suscripcion_cotizacion_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Suscripción y cotización')]"))
        )
        suscripcion_cotizacion_btn.click()
        print("Botón 'Suscripción y Cotización' ha dado clic")

        #Paso 2: Esperar y hacer clic en el botón "Crear Cotización"
        crear_cotización_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Crear Cotización')]"))
        )
        crear_cotización_link.click()
        print("Botón 'Crear Cotización'ha dado clic")


        # --- AQUÍ SE EMPIEZA A LLENAR EL FORMULARIO ---
        time.sleep(3) # Pausa de 3 segundos para que el formulario se cargue
        print("Pausa de 3 segundos para la carga del formulario.")

        #Paso 3: Dará clic en el label "Entidad Solicitante"
        clic_entidad_solicitante = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Entidad solicitante')]/following-sibling::label"))
        )
        # Re-aplicar el zoom al 67%
        driver.execute_script("document.body.style.zoom='67%'")
        print("Zoom re-aplicado a 67%.")

        clic_entidad_solicitante.click()
        print("Label desplegado")

        # 4. Esperar a que las opciones aparezcan y hacer clic en 'COLFONDOS'
        colfondos_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='COLFONDOS']"))
        )
        colfondos_option.click()
        print("Opción 'COLFONDOS' seleccionada.")

        # 5. Aquí ingresará los datos de "Tipo Solicitud de Cotización"
        clic_tipo_solicitud_cotizacion = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Tipo solicitud de cotización *')]/following-sibling::label"))
        )
        clic_tipo_solicitud_cotizacion.click()
        print("Clic en el campo 'Tipo Solicitud de Cotización")

        #Aquí agregaremos 1 de las 3 opciones que aparecen
        cotizacion_cambio_modalidad =WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='COTIZACION CAMBIO MODALIDAD']"))
        )
        cotizacion_cambio_modalidad.click()
        print("Se agrega una opción de esta lista desplegable")

        # 6. Aquí vamos a agregar una "Fecha Fin Vigencia Cotización" usando la navegación del calendario
        clic_fecha_cotizacion = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fecha fin vigencia cotización *')]/following-sibling::label"))
        )
        clic_fecha_cotizacion.click()
        print("Se abre el panel para asignar una fecha.")

        # Encontramos el año actual en el encabezado con un XPath preciso
        current_year_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'q-date__navigation')]//div[@class='relative-position overflow-hidden flex flex-center']//span[@class='block']"))
        )
        
        # Usamos un bucle para hacer clic hasta que el año sea el correcto
        while current_year_element.text != str(fecha_fin.year):
            year_chevron_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Año siguiente']"))
            )
            year_chevron_btn.click()
            time.sleep(0.5) # Pausa corta para que el calendario se actualice
            
            # Re-encontrar el elemento del año para comprobar el texto en la siguiente iteración
            current_year_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'q-date__navigation')]//div[@class='relative-position overflow-hidden flex flex-center']//span[@class='block']"))
            )
            
            print(f"El año actual es: {current_year_element.text}")
            
        print(f"El año {fecha_fin.year} ha sido seleccionado.")

        # Ahora que el año es correcto, hacemos clic en el día
        fecha_fin_day = str(fecha_fin.day)
        dia_final = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'q-date__calendar-days')]//span[text()='{fecha_fin_day}']"))
        )
        dia_final.click()
        print(f"Día '{fecha_fin_day}' seleccionado.")

        # 7. Vamos a agregar contenido en el campo "OBSERVACIONES"
        observaciones = WebDriverWait (driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Observaciones']/following-sibling::label//textarea"))
        )

        #Aquí veremos el mensaje en ese campo
        observaciones.send_keys("MENSAJE DE PRUEBA KRGG")
        print("Mensaje agregado en el campo de observaciones")

        # 8. Ahora vamos a dar clic en el campo Estado de documentación
        estado_documentacion_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Estado de documentación')]/following-sibling::label"))
        )
        estado_documentacion_dropdown.click()
        print("Desplegable 'Estado de documentación' abierto.")

            # Ahora, esperamos a que la opción 'EN REVISIÓN' sea visible y Clickeable.
        print("Esperando a que la opción 'EN REVISIÓN' esté disponible...")
        en_proceso = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='EN REVISIÓN']"))
        )
        en_proceso.click()
        print("Opción 'EN REVISIÓN' seleccionada.")


        print("Proceso de cotización finalizado.")
        time.sleep(5) # Pausa para ver los resultados
    
    except TimeoutException:
        print("Se agotó el tiempo de espera. El elemento no se encontró o no era clickeable.")
    except Exception as e:
        print(f"Ocurrió un error en el proceso de cotización: {e}")

    finally:
        # Cierra el navegador al final
        driver.quit()
else:
    print("No se pudo completar el login. Saliendo del script.")