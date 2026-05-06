# Calculadora-de-liquidaci-n-


## Colaboradores
- Sebastian Aristizabal Aristizabal

- Cesar Luis Velasquez Botero

- Yojan Esteban Salazar Osorio

- Camilo Gómez

---

## Descripción

Este proyecto implementa un sistema en Python para calcular la **liquidación laboral** de un empleado en Colombia.

Permite calcular:

* Cesantías
* Intereses sobre cesantías
* Prima de servicios
* Vacaciones
* Pago total (liquidación)

El sistema se compone de:

* Un módulo de lógica (`logicaLiquidacion.py`)
* Pruebas automatizadas (`test_pruebasCalculos.py`)
* Una interfaz por consola (`interfazLiquidacion.py`)
* Una interfaz gráfica (`GUI_liquidación.py`)

La aplicación valida datos de entrada como:

* Salario (debe ser numérico y mayor a 0)
* Fechas (formato correcto y coherencia entre ingreso/retiro)

---


### Ejecución

- Prerrequisitos: Clonar el repositorio en un ambiente establecido e instalar las dependencias.

### Instalar dependencias

```bash
pip install kivy
```

### Ejecutar la interfaz gráfica (GUI)

Ubicados en la carpeta raíz del proyecto, ejecute:

```bash
py src/view/GUI_liquidacion.py
```

### Ejecutar la interfaz por consola

Ubicados en la carpeta raíz del proyecto, ejecute:

```bash
py src/view/interfazLiquidacion.py
```

### Ejecutar las pruebas unitarias

Ubicados en la carpeta raíz del proyecto, ejecute:

```bash
py test/test_pruebasCalculos.py
```

---

## Arquitectura

El proyecto está dividido en cuatro componentes principales:

---

### 1. Lógica (`logicaLiquidacion.py`)

Contiene todos los cálculos:

* `validar_salario`
* `calcular_tiempo_trabajado_dias`
* `calcular_cesantias`
* `calcular_interes_cesantias`
* `calcular_vacaciones`
* `calcular_prima_servicios`
* `calcular_pago_neto`

También define excepciones personalizadas:

* `ErrorSalario`
* `ErrorFecha`

---

### 2. Interfaz por consola (`interfazLiquidacion.py`)

Permite interacción por consola con el usuario:

Funciones:

* `ingreso_fechas()`

  * Solicita fechas y calcula días trabajados

* `ingreso_salario()`

  * Solicita salario y lo valida

Incluye un ciclo `while` que mantiene el programa en ejecución.

---

### 3. Interfaz gráfica (`GUI_liquidacion.py`)

Permite interacción visual con el usuario mediante ventanas construidas con Kivy.

Clase principal:

* `LiquidacionApp`
  * Punto de entrada de la aplicación Kivy. Configura el título y tamaño de la ventana.

* `LiquidacionLayout`
  * Layout raíz que organiza toda la interfaz. Contiene:

    * `_construir_cabecera()`
      * Barra superior con el título y subtítulo del sistema.

    * `_construir_cuerpo()`
      * Área scrolleable que aloja las tres tarjetas de la interfaz.

    * `_construir_tarjeta_datos()`
      * Campos de entrada: fecha de inicio, fecha de retiro y salario. Botón principal de cálculo.

    * `_construir_tarjeta_resultados()`
      * Muestra los resultados: días trabajados, cesantías, intereses, vacaciones, prima y total.

    * `_construir_tarjeta_acciones()`
      * Botones para consultar cada concepto individualmente y limpiar el formulario.

    * `_leer_y_validar_entradas()`
      * Lee los campos del formulario y delega la validación al modelo.

    * `_calcular_liquidacion()`
      * Orquesta el cálculo completo y actualiza la tarjeta de resultados.

    * `_mostrar_dias_trabajados()`, `_mostrar_cesantias()`, `_mostrar_intereses()`, `_mostrar_vacaciones()`, `_mostrar_prima()`
      * Calculan y muestran cada concepto en un popup individual.

    * `_limpiar_formulario()`
      * Restablece todos los campos y resultados a su estado inicial.

Funciones auxiliares (module-level):

* `crear_etiqueta()`, `crear_campo_texto()`, `crear_boton()`
  * Fábricas de widgets reutilizables con estilos consistentes.

* `aplicar_fondo_solido()`, `aplicar_fondo_redondeado()`
  * Aplican fondos de color a los layouts de Kivy.

* `mostrar_popup()`
  * Ventana emergente genérica para errores y resultados individuales.

* `formatear_pesos()`
  * Formatea valores numéricos como pesos colombianos (p. ej. `$ 1.458.250,75`).

---

### 4. Pruebas (`test_pruebasCalculos.py`)

Incluye pruebas con `unittest` para:

* Cálculos correctos
* Casos límite
* Manejo de errores
* Validación de datos

## Estructura

```
Calculadora-de-liquidaci-n-/
│
├── src/
│   └── model/
│   │   └── logicaLiquidacion.py
│   │   └── errores.py
│   │   └── __init__.py
│   │
│   └── view/
│       └── interfazLiquidacion.py
│       └── GUI_liquidacion.py
│
├── test/
│   └── test_pruebasCalculos.py
│   └── __init__.py
│
└── README.md
```

---