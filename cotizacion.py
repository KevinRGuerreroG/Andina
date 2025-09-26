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
        # Espera implícita por el primer elemento del formulario en lugar de un sleep estático
        print("Esperando a que el formulario se cargue...")
        clic_entidad_solicitante = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Entidad solicitante')]/following-sibling::label"))
        )
        print("Formulario cargado.")

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
        fecha_fin = date.today() + relativedelta(years=2)
        clic_fecha_cotizacion = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fecha fin vigencia cotización *')]/following-sibling::label"))
        )
        clic_fecha_cotizacion.click()
        print("Se abre el panel para asignar una fecha.")

        # Encontramos el año actual en el encabezado con un XPath preciso
        current_year_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'q-date__navigation')]//div[@class='relative-position overflow-hidden flex flex-center']//span[@class='block']"))
        )
        
        while current_year_element.text != str(fecha_fin.year):
            year_chevron_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Año siguiente']"))
            )
            year_chevron_btn.click()
            time.sleep(0.5)
            current_year_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'q-date__navigation')]//div[@class='relative-position overflow-hidden flex flex-center']//span[@class='block']"))
            )
            print(f"El año actual es: {current_year_element.text}")
        print(f"El año {fecha_fin.year} ha sido seleccionado.")

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
        observaciones.send_keys("MENSAJE DE PRUEBA KRGG")
        print("Mensaje agregado en el campo de observaciones")

        # 8. Ahora vamos a dar clic en el campo Estado de documentación
        estado_documentacion_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Estado de documentación')]/following-sibling::label"))
        )
        estado_documentacion_dropdown.click()
        print("Desplegable 'Estado de documentación' abierto.")

        print("Esperando a que la opción 'EN REVISIÓN' esté disponible...")
        en_proceso = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='EN REVISIÓN']"))
        )
        en_proceso.click()
        print("Opción 'EN REVISIÓN' seleccionada.")

        # 9. Ahora vamos con el campo Origen pensión *
        origen_pension = WebDriverWait (driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Origen pensión *')]/following-sibling::label"))
        )
        origen_pension.click()
        print("Se realiza el clic en el campo Origen pensión")

        origen_invalidez = WebDriverWait (driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='INVALIDEZ']"))
        )
        origen_invalidez.click()
        print("Se seleccionó el valor INVALIDEZ")
        
        # --- INICIO DEL BLOQUE CORREGIDO Y ROBUSTO ---

        # 10. Ingresar valor en el campo "Vr. capital *"
        print("Esperando a que el campo 'Vr. capital *' sea visible...")
            
        vr_capital_locator = (By.XPATH, "//span[text()='Vr. capital *']/following-sibling::label//input")
            
        # Esperamos a que el elemento sea VISIBLE
        vr_capital_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(vr_capital_locator)
        )
            
        vr_capital_input.clear()
        vr_capital_input.send_keys("130000000")
        print("Valor agregado en 'Vr. capital *'")

    
        print("ERROR: El campo 'Vr. capital *' no se hizo visible. Guardando captura de pantalla.")
        driver.save_screenshot("error_vr_capital.png")

        # 11. Ingresar valor en el campo "Vr. pensión *"
        print("Esperando a que el campo 'Vr. pensión *' sea visible...")
        # NOTA: Confirma si este texto es "Vr. pensión *" o "Vr. pension *"
        vr_pension_locator = (By.XPATH, "//span[text()='Vr. pensión *']/following-sibling::label//input")
        vr_pension_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(vr_pension_locator)
        )
        vr_pension_input.clear()
        vr_pension_input.send_keys("1623500")
        print("Valor agregado en 'Vr. pensión *'")

        # 12. Ingresar valor en el campo "# mesadas "
        print("Esperando a que el campo '# mesadas *' sea visible...")
        mesadas_locator = (By.XPATH, "//span[text()='# mesadas *']/following-sibling::label//input")
        mesadas_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(mesadas_locator)
        )
        mesadas_input.clear()
        mesadas_input.send_keys("13")
        print("Valor agregado en '# mesadas *'")
        
         # 13. Hacer clic en el botón "Continuar" para finalizar
        print("Buscando el botón 'Continuar'...")
        continuar_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continuar']]"))
        )
        
        # Hacemos scroll por si el botón está fuera de la vista
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continuar_btn)
        time.sleep(0.5)

        continuar_btn.click()
        print("Botón 'Continuar' ha sido presionado.")




#------------------------------------SEGUNDA SECCIÓN DE LA CREACIÓN DE COTIZACIÓN ------------------------------------
        #-----------DATOS BASICOS-----------        

        # 1. Tipo de identificación
        tipo_documento_locator = (By.XPATH, "//span[text()='Tipo identificación *']/following-sibling::label")
        print("Esperando a que cargue la segunda parte del formulario...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(tipo_documento_locator)
        )
        print("Segunda parte del formulario cargada.")

        # Paso B: Hacer scroll para que el elemento sea visible y no quede debajo del header.
        tipo_documento_element = driver.find_element(*tipo_documento_locator)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tipo_documento_element)
        time.sleep(0.5)

        # Seleccionamos Tipo de identificación
        tipo_documento_element.click()
        print("Se selecciona el campo TIPO DE DOCUMENTO")

        # Acá seleccionaremos el tipo de documento CEDULA CIUDADANIA
        c_c = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[text()='CÉDULA CIUDADANIA']"))
        )
        c_c.click()
        print("Se ha seleccionado CEDULA DE CIUDADANÍA")


        # 2. Ahora vamos a agregar el # de documento
        print("Buscando el campo '# identificación *'...")
        numero_id_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='# identificación *']/following-sibling::label//input"))
        )
        numero_id_input.clear()
        numero_id_input.send_keys("123456789") # <-- Escribe aquí el número que necesites
        print("Número de identificación ingresado.")


        # 3. Ahora vamos a agregar la fecha de expedición del documento
        
        # Abre el calendario
        fecha_exp_doc = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Fecha expedición documento']/following-sibling::label"))
        )
        fecha_exp_doc.click()
        print("Se abre el panel para asignar una fecha.")

        # Definimos el objetivo y herramientas
        fecha_objetivo = date(2014, 11, 14)
        meses_a_numero = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        # Bucle principal para ajustar Año y Mes
        print(f"Buscando la fecha: {fecha_objetivo.strftime('%B de %Y')}...")
        
        # Localizadores de lectura
        year_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[2]")
        month_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[1]")
        
        # --- AÑADIMOS BOTONES PARA NAVEGAR HACIA ADELANTE ---
        prev_year_btn_locator = (By.XPATH, "//button[@aria-label='Año anterior']")
        next_year_btn_locator = (By.XPATH, "//button[@aria-label='Año siguiente']")
        prev_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes anterior']")
        next_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes siguiente']")
        
        while True:
            # Leemos el estado actual del calendario
            year_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(year_locator))
            month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(month_locator))
            current_year = int(year_element.text)
            current_month = meses_a_numero[month_element.text.lower()]
            
            # Condición de salida: si ya llegamos, rompemos el bucle
            if current_year == fecha_objetivo.year and current_month == fecha_objetivo.month:
                print(f"Mes y año correctos encontrados: {month_element.text} de {current_year}")
                break

            # Lógica de decisión bidireccional
            element_to_wait_for = None # Para saber qué elemento debe refrescarse
            btn_locator_to_click = None

            if current_year > fecha_objetivo.year:
                btn_locator_to_click = prev_year_btn_locator
                element_to_wait_for = year_element
            elif current_year < fecha_objetivo.year:
                btn_locator_to_click = next_year_btn_locator
                element_to_wait_for = year_element
            # Si los años son iguales, ajustamos el mes
            elif current_month > fecha_objetivo.month:
                btn_locator_to_click = prev_month_btn_locator
                element_to_wait_for = month_element
            elif current_month < fecha_objetivo.month:
                btn_locator_to_click = next_month_btn_locator
                element_to_wait_for = month_element

            # Ejecutamos el clic y la espera
            if btn_locator_to_click and element_to_wait_for:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator_to_click)).click()
                WebDriverWait(driver, 10).until(EC.staleness_of(element_to_wait_for))
            else:
                # Si no hay ninguna acción que tomar, salimos para evitar un bucle infinito
                print("Error de lógica, saliendo del bucle.")
                break

        # SELECCIONAR EL DÍA
        print(f"Seleccionando el día {fecha_objetivo.day}...")
        day_locator = (By.XPATH, f"//div[contains(@class, 'q-date__calendar-days')]//button[.//span[text()='{fecha_objetivo.day}']]")
        day_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(day_locator))
        driver.execute_script("arguments[0].click();", day_element)
        
        print(f"Fecha completa seleccionada: {fecha_objetivo.strftime('%d de %B de %Y')}")

        # --- FIN DE LA LÓGICA DE NAVEGACIÓN FINAL ---

        # 4. Ahora vamos a digitar Primer nombre *
        print("Buscando el campo '# identificación *'...")
        Primer_nombre = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Primer nombre *']/following-sibling::label//input"))
        )
        Primer_nombre.clear()
        Primer_nombre.send_keys("KEVIN")
        print("Nombre registrado.")

        # 5. Ahora vamos a digitar Segundo nombre
        print("Vamos a digitar el segundo nombre")
        Segundo_nombre = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located ((By.XPATH, "//span[text()='Segundo nombre']/following-sibling::label//input"))
        )
        Segundo_nombre.clear()
        Segundo_nombre.send_keys("REINALDO")
        print("Segundo nombre registrado")

        # 6. Ahora vamos a agregar el Primer apellido *
        print("Vamos a digitar el Primer apellido *")
        Primer_apellido = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located ((By.XPATH, "//span[text()='Primer apellido *']/following-sibling::label//input"))
        )
        Primer_apellido.clear()
        Primer_apellido.send_keys("Guerrero")
        print("Apellido registrado")

        # 7. Ahora vamos a agregar el Segundo apellido
        print("Vamos  digitar el segundo apellido")
        Segundo_apellido = WebDriverWait (driver, 15).until(
            EC.visibility_of_element_located ((By.XPATH, "//span[text()='Segundo apellido']/following-sibling::label//input"))
        )
        Segundo_apellido.clear()
        Segundo_apellido.send_keys("Garcia")
        print("Segundo apellido registrado")


        # 8. Fecha de nacimiento
        objetivo_nacimiento = date(1960, 11, 1)

        # PASO A: HACER SCROLL Y ABRIR EL CALENDARIO
        fecha_nac_locator = (By.XPATH, "//span[text()='Fecha de nacimiento *']/following-sibling::label")
        fecha_nac_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(fecha_nac_locator))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fecha_nac_element)
        time.sleep(0.5)
        fecha_nac_element.click()
        print("Calendario de Fecha de Nacimiento abierto.")

        # PASO B: ABRIR LA VISTA DE AÑOS
        print("Abriendo la vista de selección de año...")
        year_view_button_locator = (By.XPATH, "(//div[contains(@class, 'q-menu') and not(contains(@style, 'display: none'))]//div[contains(@class, 'q-date__navigation')]//button[.//span[@class='block']])[2]")
        year_view_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(year_view_button_locator))
        year_view_button.click()
        time.sleep(0.5)

        # --- INICIO DE LA LÓGICA CORREGIDA ---
        
        print(f"Buscando el año {objetivo_nacimiento.year}...")
        
        año_objetivo_locator = (By.XPATH, f"//div[@class='q-date__years-content']//span[text()='{objetivo_nacimiento.year}']")
        flecha_anterior_decada_locator = (By.XPATH, "//button[@aria-label='Anterior 20 años']")
        
        for i in range(10):
            try:
                # Intenta encontrar el año objetivo. Si lo encuentra, salimos del bucle.
                # Usamos una espera muy corta (1 segundo) para no perder tiempo.
                WebDriverWait(driver, 1).until(EC.visibility_of_element_located(año_objetivo_locator))
                print(f"Año {objetivo_nacimiento.year} encontrado en la vista.")
                break
            except TimeoutException:
                # Si no lo encuentra, es normal. Hacemos clic para retroceder.
                print(f"Intento {i+1}: El año {objetivo_nacimiento.year} no es visible. Retrocediendo 20 años...")
                flecha_anterior = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(flecha_anterior_decada_locator))
                flecha_anterior.click()
                # Pausa simple para la animación. Es menos "inteligente" pero más fiable en este caso.
                time.sleep(0.5)
        else:
            raise Exception(f"No se pudo encontrar el año {objetivo_nacimiento.year} después de 10 intentos.")

        # --- FIN DE LA LÓGICA CORREGIDA ---

        # PASO D: SELECCIONAR EL AÑO ENCONTRADO
        print(f"Seleccionando el año {objetivo_nacimiento.year}...")
        año_a_seleccionar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(año_objetivo_locator)
        )
        año_a_seleccionar.click()
        
        # PASO E: NAVEGAR AL MES CORRECTO
        meses_a_numero = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        
        month_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[1]")
        prev_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes anterior']")
        next_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes siguiente']")
        
        while True:
            month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(month_locator))
            current_month_num = meses_a_numero[month_element.text.lower()]
            
            if current_month_num == objetivo_nacimiento.month:
                print(f"Mes correcto encontrado: {month_element.text}")
                break
            
            if current_month_num > objetivo_nacimiento.month:
                btn_to_click_locator = prev_month_btn_locator
            else:
                btn_to_click_locator = next_month_btn_locator
            
            btn_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_to_click_locator))
            btn_to_click.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(month_element))
            
        # PASO F: SELECCIONAR EL DÍA
        print(f"Seleccionando el día {objetivo_nacimiento.day}...")
        day_locator = (By.XPATH, f"//div[contains(@class, 'q-date__calendar-days')]//button[.//span[text()='{objetivo_nacimiento.day}']]")
        day_to_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(day_locator))
        day_to_select.click()
        
        print(f"Fecha de Nacimiento seleccionada: {objetivo_nacimiento.strftime('%d de %B de %Y')}")



        # # Definimos el objetivo y herramientas
        # fecha_objetivo = date(2014, 11, 14)
        # meses_a_numero = {
        #     'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        #     'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        # }






        # # 3. Ahora vamos a agregar la fecha de expedición del documento
        
        # # Abre el calendario
        # fecha_exp_doc = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Fecha expedición documento']/following-sibling::label"))
        # )
        # fecha_exp_doc.click()
        # print("Se abre el panel para asignar una fecha.")

        # # Definimos el objetivo y herramientas
        # fecha_objetivo = date(2014, 11, 14)
        # meses_a_numero = {
        #     'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        #     'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        # }

        # # Bucle principal para ajustar Año y Mes
        # print(f"Buscando la fecha: {fecha_objetivo.strftime('%B de %Y')}...")
        
        # # Localizadores de lectura
        # year_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[2]")
        # month_locator = (By.XPATH, "(//div[contains(@class, 'q-date__navigation')]//button//span[@class='block'])[1]")
        
        # # --- AÑADIMOS BOTONES PARA NAVEGAR HACIA ADELANTE ---
        # prev_year_btn_locator = (By.XPATH, "//button[@aria-label='Año anterior']")
        # next_year_btn_locator = (By.XPATH, "//button[@aria-label='Año siguiente']")
        # prev_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes anterior']")
        # next_month_btn_locator = (By.XPATH, "//button[@aria-label='Mes siguiente']")
        
        # while True:
        #     # Leemos el estado actual del calendario
        #     year_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(year_locator))
        #     month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(month_locator))
        #     current_year = int(year_element.text)
        #     current_month = meses_a_numero[month_element.text.lower()]
            
        #     # Condición de salida: si ya llegamos, rompemos el bucle
        #     if current_year == fecha_objetivo.year and current_month == fecha_objetivo.month:
        #         print(f"Mes y año correctos encontrados: {month_element.text} de {current_year}")
        #         break

        #     # Lógica de decisión bidireccional
        #     element_to_wait_for = None # Para saber qué elemento debe refrescarse
        #     btn_locator_to_click = None

        #     if current_year > fecha_objetivo.year:
        #         btn_locator_to_click = prev_year_btn_locator
        #         element_to_wait_for = year_element
        #     elif current_year < fecha_objetivo.year:
        #         btn_locator_to_click = next_year_btn_locator
        #         element_to_wait_for = year_element
        #     # Si los años son iguales, ajustamos el mes
        #     elif current_month > fecha_objetivo.month:
        #         btn_locator_to_click = prev_month_btn_locator
        #         element_to_wait_for = month_element
        #     elif current_month < fecha_objetivo.month:
        #         btn_locator_to_click = next_month_btn_locator
        #         element_to_wait_for = month_element

        #     # Ejecutamos el clic y la espera
        #     if btn_locator_to_click and element_to_wait_for:
        #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator_to_click)).click()
        #         WebDriverWait(driver, 10).until(EC.staleness_of(element_to_wait_for))
        #     else:
        #         # Si no hay ninguna acción que tomar, salimos para evitar un bucle infinito
        #         print("Error de lógica, saliendo del bucle.")
        #         break

        # # SELECCIONAR EL DÍA
        # print(f"Seleccionando el día {fecha_objetivo.day}...")
        # day_locator = (By.XPATH, f"//div[contains(@class, 'q-date__calendar-days')]//button[.//span[text()='{fecha_objetivo.day}']]")
        # day_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(day_locator))
        # driver.execute_script("arguments[0].click();", day_element)
        
        # print(f"Fecha completa seleccionada: {fecha_objetivo.strftime('%d de %B de %Y')}")

        # # --- FIN DE LA LÓGICA DE NAVEGACIÓN FINAL ---








        print("Proceso de cotización finalizado.")
        time.sleep(5)    
    except TimeoutException:
        print("Se agotó el tiempo de espera. El elemento no se encontró o no era clickeable.")
    except Exception as e:
        print(f"Ocurrió un error en el proceso de cotización: {e}")

#     finally:
#         # Cierra el navegador al final
#         driver.quit()
# else:
#     print("No se pudo completar el login. Saliendo del script.")