"""
GUI_liquidacion.py
==================
Interfaz gráfica (GUI) de la Calculadora de Liquidación Laboral para Colombia,
construida con el framework Kivy.

Este módulo actúa como la capa de presentación (vista) del sistema. No contiene
lógica de negocio propia: delega todos los cálculos y validaciones al módulo
`logicaLiquidacion` y al módulo `errores`, ambos ubicados en `src/model/`.

Funcionalidades expuestas al usuario:
  - Ingresar fecha de inicio y fin del contrato (formato DD/MM/AAAA).
  - Ingresar el salario mensual del empleado.
  - Calcular y visualizar:
      * Días trabajados (método 360).
      * Cesantías.
      * Intereses sobre cesantías.
      * Vacaciones.
      * Prima de servicios.
      * Total de la liquidación (pago neto).
  - Consultar cada concepto de forma individual mediante botones dedicados.
  - Limpiar todos los campos y resultados con un solo clic.

Compatibilidad:
  - Python 3.8+
  - Kivy 2.x
  - Funciona en Windows, macOS y Linux siempre que Kivy esté instalado.

Ejecución:
  Desde la raíz del proyecto:
      py src/view/GUI_liquidacion.py
"""

import sys
import os

# Agrega las rutas necesarias para que Python encuentre el paquete `model`
# independientemente del directorio desde el que se ejecute el script.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp

from model import logicaLiquidacion
from model import errores


# ──────────────────────────────────────────────────────────────────────────────
# PALETA DE COLORES
# Todas las constantes de color se definen aquí en formato RGBA (0-1)
# para facilitar su mantenimiento y consistencia visual en toda la app.
# ──────────────────────────────────────────────────────────────────────────────
COLOR_FONDO_GENERAL   = (0.96, 0.97, 0.98, 1)   # Gris muy claro: fondo de la ventana
COLOR_FONDO_CABECERA  = (0.13, 0.37, 0.63, 1)   # Azul oscuro: barra de título
COLOR_FONDO_TARJETA   = (1,    1,    1,    1)    # Blanco puro: tarjetas de contenido
COLOR_PRIMARIO        = (0.13, 0.37, 0.63, 1)   # Azul principal: botones y títulos
COLOR_EXITO           = (0.10, 0.60, 0.40, 1)   # Verde: resultados positivos
COLOR_ERROR           = (0.80, 0.15, 0.15, 1)   # Rojo: mensajes de error
COLOR_ADVERTENCIA     = (0.85, 0.50, 0.10, 1)   # Naranja: advertencias inesperadas
COLOR_TEXTO_OSCURO    = (0.12, 0.12, 0.18, 1)   # Casi negro: texto principal
COLOR_TEXTO_CLARO     = (1,    1,    1,    1)    # Blanco: texto sobre fondos oscuros
COLOR_TEXTO_SUAVE     = (0.50, 0.52, 0.56, 1)   # Gris medio: etiquetas secundarias
COLOR_FONDO_RESULTADO = (0.92, 0.97, 0.93, 1)   # Verde muy claro: fila de total
COLOR_DIVISOR         = (0.88, 0.90, 0.93, 1)   # Gris claro: líneas separadoras
COLOR_BOTON_SECUNDARIO = (0.20, 0.52, 0.78, 1)  # Azul medio: botones de consulta
COLOR_BOTON_LIMPIAR   = (0.60, 0.62, 0.65, 1)   # Gris: botón limpiar


# ──────────────────────────────────────────────────────────────────────────────
# FUNCIONES DE FONDO Y UTILIDADES GRÁFICAS
# ──────────────────────────────────────────────────────────────────────────────

def _redibujar_fondo_solido(widget, color):
    """
    Borra y vuelve a dibujar un rectángulo de color sólido sobre el canvas
    `before` del widget recibido.

    Se llama cada vez que el widget cambia de posición o tamaño para que el
    fondo siempre cubra el área correcta.

    Parámetros:
        widget (Widget): El widget de Kivy al que se le aplica el fondo.
        color  (tuple) : Color en formato RGBA (valores entre 0 y 1).
    """
    widget.canvas.before.clear()
    with widget.canvas.before:
        Color(*color)
        Rectangle(pos=widget.pos, size=widget.size)


def aplicar_fondo_solido(widget, color):
    """
    Enlaza los eventos `pos` y `size` de un widget para que su fondo de color
    sólido se redibuje automáticamente ante cualquier cambio de geometría.

    Parámetros:
        widget (Widget): El widget al que se le aplicará el fondo.
        color  (tuple) : Color en formato RGBA.

    Retorna:
        Widget: El mismo widget recibido, para permitir encadenamiento.
    """
    widget.bind(
        pos=lambda w, _: _redibujar_fondo_solido(w, color),
        size=lambda w, _: _redibujar_fondo_solido(w, color),
    )
    _redibujar_fondo_solido(widget, color)
    return widget


def _redibujar_fondo_redondeado(widget, color, radio):
    """
    Borra y vuelve a dibujar un rectángulo con esquinas redondeadas sobre el
    canvas `before` del widget.

    Parámetros:
        widget (Widget): El widget al que se le aplica el fondo.
        color  (tuple) : Color en formato RGBA.
        radio  (int)   : Radio en píxeles de las esquinas redondeadas.
    """
    widget.canvas.before.clear()
    with widget.canvas.before:
        Color(*color)
        RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radio])


def aplicar_fondo_redondeado(widget, color, radio=12):
    """
    Enlaza los eventos `pos` y `size` de un widget para que su fondo con
    esquinas redondeadas se redibuje automáticamente.

    Parámetros:
        widget (Widget): El widget al que se le aplicará el fondo redondeado.
        color  (tuple) : Color en formato RGBA.
        radio  (int)   : Radio de las esquinas en píxeles (por defecto 12).

    Retorna:
        Widget: El mismo widget recibido.
    """
    widget.bind(
        pos=lambda w, _: _redibujar_fondo_redondeado(w, color, radio),
        size=lambda w, _: _redibujar_fondo_redondeado(w, color, radio),
    )
    _redibujar_fondo_redondeado(widget, color, radio)
    return widget


# ──────────────────────────────────────────────────────────────────────────────
# FÁBRICAS DE WIDGETS REUTILIZABLES
# Funciones que construyen widgets de Kivy con estilos consistentes,
# evitando repetición de configuración en toda la interfaz.
# ──────────────────────────────────────────────────────────────────────────────

def crear_etiqueta(texto, tamanio_fuente=15, color=COLOR_TEXTO_OSCURO,
                   negrita=False, alineacion='left',
                   size_hint_y=None, alto=dp(28)):
    """
    Crea y retorna un widget `Label` de Kivy con los parámetros visuales
    estándar de la aplicación.

    Parámetros:
        texto          (str)   : Texto a mostrar en la etiqueta.
        tamanio_fuente (int)   : Tamaño de la fuente en puntos (por defecto 15).
        color          (tuple) : Color del texto en formato RGBA.
        negrita        (bool)  : True para texto en negrita.
        alineacion     (str)   : Alineación horizontal ('left', 'center', 'right').
        size_hint_y    (float) : Pista de tamaño vertical para Kivy layouts.
        alto           (float) : Altura fija del widget en píxeles de densidad.

    Retorna:
        Label: Widget de etiqueta configurado.
    """
    etiqueta = Label(
        text=texto,
        font_size=tamanio_fuente,
        color=color,
        bold=negrita,
        halign=alineacion,
        valign='middle',
        size_hint_y=size_hint_y,
        height=alto,
    )
    # Sincroniza el área de texto con el tamaño del widget para que
    # el alineado horizontal funcione correctamente.
    etiqueta.bind(size=lambda w, _: setattr(w, 'text_size', w.size))
    return etiqueta


def crear_campo_texto(sugerencia='', filtro_entrada=None, multilinea=False):
    """
    Crea y retorna un widget `TextInput` estilizado para la captura de datos
    del usuario.

    Parámetros:
        sugerencia     (str)  : Texto de marcador de posición (hint text).
        filtro_entrada (str)  : Filtro de Kivy para restringir la entrada
                                (p. ej. 'int' solo permite dígitos).
        multilinea     (bool) : True para permitir saltos de línea.

    Retorna:
        TextInput: Campo de texto configurado.
    """
    campo = TextInput(
        hint_text=sugerencia,
        multiline=multilinea,
        input_filter=filtro_entrada,
        font_size=15,
        padding=[dp(10), dp(10)],
        size_hint_y=None,
        height=dp(44),
        background_color=(1, 1, 1, 1),
        foreground_color=COLOR_TEXTO_OSCURO,
        hint_text_color=list(COLOR_TEXTO_SUAVE),
        cursor_color=list(COLOR_PRIMARIO),
    )
    return campo


def crear_boton(texto, color_fondo=COLOR_PRIMARIO,
                color_texto=COLOR_TEXTO_CLARO,
                tamanio_fuente=15, negrita=True, alto=dp(46)):
    """
    Crea y retorna un widget `Button` estilizado con los colores y tipografía
    estándar de la aplicación.

    Parámetros:
        texto          (str)   : Etiqueta visible del botón.
        color_fondo    (tuple) : Color de fondo en formato RGBA.
        color_texto    (tuple) : Color del texto en formato RGBA.
        tamanio_fuente (int)   : Tamaño de la fuente en puntos.
        negrita        (bool)  : True para texto en negrita.
        alto           (float) : Altura fija del botón en píxeles de densidad.

    Retorna:
        Button: Widget de botón configurado.
    """
    boton = Button(
        text=texto,
        font_size=tamanio_fuente,
        bold=negrita,
        color=color_texto,
        background_normal='',
        background_color=color_fondo,
        size_hint_y=None,
        height=alto,
    )
    return boton


def crear_linea_divisora():
    """
    Crea y retorna un widget delgado (1 dp de alto) que actúa como línea
    divisora visual entre secciones, con el color `COLOR_DIVISOR`.

    Retorna:
        Widget: Línea horizontal separadora.
    """
    linea = Widget(size_hint_y=None, height=dp(1))

    def _redibujar_linea(w):
        """Redibuja la línea cuando el widget cambia de geometría."""
        w.canvas.clear()
        with w.canvas:
            Color(*COLOR_DIVISOR)
            Rectangle(pos=w.pos, size=w.size)

    linea.bind(
        pos=lambda w, _: _redibujar_linea(w),
        size=lambda w, _: _redibujar_linea(w),
    )
    return linea


def mostrar_popup(titulo, mensaje, color=COLOR_ERROR):
    """
    Muestra una ventana emergente (Popup) con un título, un mensaje y un botón
    para cerrarla. Se usa tanto para errores como para mostrar resultados
    individuales de cada concepto de liquidación.

    El color del título y del botón varía según el tipo de mensaje:
        - COLOR_ERROR     → errores de validación.
        - COLOR_EXITO     → resultados calculados correctamente.
        - COLOR_ADVERTENCIA → errores inesperados del sistema.
        - COLOR_PRIMARIO  → información general (p. ej. días trabajados).

    Parámetros:
        titulo  (str)  : Título del popup (breve).
        mensaje (str)  : Cuerpo del mensaje (puede contener saltos de línea).
        color   (tuple): Color RGBA que identifica el tipo de mensaje.
    """
    # Contenedor principal del popup con fondo blanco
    contenido = BoxLayout(
        orientation='vertical',
        padding=dp(20),
        spacing=dp(14),
    )
    aplicar_fondo_solido(contenido, COLOR_FONDO_TARJETA)

    # Icono según el tipo de mensaje
    icono = '✖' if color == COLOR_ERROR else ('✔' if color == COLOR_EXITO else 'ℹ')

    contenido.add_widget(crear_etiqueta(
        f'{icono}  {titulo}',
        tamanio_fuente=17,
        color=color,
        negrita=True,
        alineacion='center',
        alto=dp(32),
    ))
    contenido.add_widget(crear_linea_divisora())

    # Etiqueta con el mensaje principal
    etiqueta_mensaje = Label(
        text=mensaje,
        font_size=14,
        color=COLOR_TEXTO_OSCURO,
        halign='center',
        valign='middle',
        size_hint_y=1,
    )
    etiqueta_mensaje.bind(size=lambda w, _: setattr(w, 'text_size', w.size))
    contenido.add_widget(etiqueta_mensaje)

    # Botón para cerrar el popup
    boton_cerrar = crear_boton('Cerrar', color_fondo=color, alto=dp(42))
    contenido.add_widget(boton_cerrar)

    popup = Popup(
        title='',
        content=contenido,
        size_hint=(0.85, 0.45),
        separator_height=0,
        background='',
        background_color=(0, 0, 0, 0),
    )
    boton_cerrar.bind(on_release=popup.dismiss)
    popup.open()


def crear_fila_resultado(texto_etiqueta, color_valor=COLOR_TEXTO_OSCURO):
    """
    Crea una fila horizontal compuesta por una etiqueta descriptiva a la
    izquierda y una etiqueta de valor numérico a la derecha.

    Se utiliza para mostrar cada concepto de la liquidación en la sección
    de resultados (p. ej. 'Cesantías:' → '$ 1.458.250,00').

    Parámetros:
        texto_etiqueta (str)   : Nombre del concepto (columna izquierda).
        color_valor    (tuple) : Color RGBA del valor numérico.

    Retorna:
        tuple: (BoxLayout fila, Label etiqueta_valor)
            - La fila lista para agregar a un layout padre.
            - La referencia al Label del valor para actualizarlo después.
    """
    fila = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(32),
    )
    fila.add_widget(crear_etiqueta(
        texto_etiqueta,
        tamanio_fuente=13,
        color=COLOR_TEXTO_SUAVE,
        alineacion='left',
    ))
    etiqueta_valor = crear_etiqueta(
        '—',
        tamanio_fuente=14,
        color=color_valor,
        negrita=True,
        alineacion='right',
    )
    fila.add_widget(etiqueta_valor)
    return fila, etiqueta_valor


def formatear_pesos(valor):
    """
    Formatea un número flotante como una cadena de texto que representa pesos
    colombianos, usando punto (.) como separador de miles y coma (,) como
    separador decimal.

    Ejemplo:
        formatear_pesos(1458250.75) → '$ 1.458.250,75'

    Parámetros:
        valor (float): Valor numérico a formatear.

    Retorna:
        str: Cadena con el valor formateado en pesos colombianos.
    """
    # 1. Formatea con separador de miles ',' y dos decimales '.'
    # 2. Reemplaza ',' → 'X' de forma temporal para evitar colisiones.
    # 3. Reemplaza '.' → ',' (separador decimal colombiano).
    # 4. Reemplaza 'X' → '.' (separador de miles colombiano).
    return f'$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


# ──────────────────────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

class LiquidacionLayout(BoxLayout):
    """
    Layout raíz de la aplicación. Organiza la interfaz en dos grandes bloques:
        1. Cabecera (header): título y subtítulo de la app.
        2. Cuerpo (body)   : área scrolleable con las tarjetas de entrada,
                             resultados y acciones.

    Hereda de BoxLayout con orientación vertical.
    """

    def __init__(self, **kwargs):
        """
        Inicializa el layout principal, establece el color de fondo de la
        ventana y construye los bloques de la interfaz.
        """
        super().__init__(orientation='vertical', **kwargs)
        Window.clearcolor = COLOR_FONDO_GENERAL
        aplicar_fondo_solido(self, COLOR_FONDO_GENERAL)

        self._construir_cabecera()
        self._construir_cuerpo()

    # ── Cabecera ──────────────────────────────────────────────────────────────

    def _construir_cabecera(self):
        """
        Construye la barra superior de la aplicación con el nombre del sistema
        y una línea descriptiva sobre la normativa aplicada.

        Agrega el bloque directamente al layout raíz (self).
        """
        cabecera = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            padding=[dp(20), dp(12)],
        )
        aplicar_fondo_solido(cabecera, COLOR_FONDO_CABECERA)

        cabecera.add_widget(crear_etiqueta(
            'Calculadora de Liquidación Laboral',
            tamanio_fuente=20,
            color=COLOR_TEXTO_CLARO,
            negrita=True,
            alineacion='center',
            alto=dp(34),
        ))
        self.add_widget(cabecera)

    # ── Cuerpo ────────────────────────────────────────────────────────────────

    def _construir_cuerpo(self):
        """
        Construye el área principal scrolleable de la aplicación.

        Crea un `ScrollView` que contiene un `BoxLayout` vertical con las tres
        tarjetas de la interfaz:
            1. Tarjeta de datos de entrada.
            2. Tarjeta de resultados.
            3. Tarjeta de botones de consulta individual.

        Agrega el bloque directamente al layout raíz (self).
        """
        area_scroll = ScrollView(size_hint=(1, 1))
        contenedor_tarjetas = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(16), dp(16)],
            spacing=dp(14),
        )
        # Permite que el contenedor crezca verticalmente según su contenido
        contenedor_tarjetas.bind(minimum_height=contenedor_tarjetas.setter('height'))

        contenedor_tarjetas.add_widget(self._construir_tarjeta_datos())
        contenedor_tarjetas.add_widget(self._construir_tarjeta_resultados())
        contenedor_tarjetas.add_widget(self._construir_tarjeta_acciones())

        # Espacio en blanco al final para mejor experiencia en móvil
        contenedor_tarjetas.add_widget(Widget(size_hint_y=None, height=dp(20)))

        area_scroll.add_widget(contenedor_tarjetas)
        self.add_widget(area_scroll)

    # ── Tarjeta: datos de entrada ─────────────────────────────────────────────

    def _construir_tarjeta_datos(self):
        """
        Construye la tarjeta de entrada de datos del empleado.

        Contiene:
            - Campo de texto para la fecha de inicio del contrato.
            - Campo de texto para la fecha de fin del contrato.
            - Campo de texto numérico para el salario mensual.
            - Botón principal '⚡ Calcular liquidación'.

        Los campos se almacenan como atributos de instancia
        (`self.campo_fecha_inicio`, `self.campo_fecha_fin`,
        `self.campo_salario`) para que los métodos de cálculo puedan leerlos.

        Retorna:
            BoxLayout: Tarjeta de entrada lista para agregar al cuerpo.
        """
        tarjeta = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(16), dp(14)],
            spacing=dp(8),
        )
        aplicar_fondo_redondeado(tarjeta, COLOR_FONDO_TARJETA)

        tarjeta.add_widget(crear_etiqueta(
            'Datos del empleado',
            tamanio_fuente=16,
            negrita=True,
            color=COLOR_PRIMARIO,
            alto=dp(30),
        ))
        tarjeta.add_widget(crear_linea_divisora())
        tarjeta.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # ── Fecha de ingreso ──
        tarjeta.add_widget(crear_etiqueta(
            'Fecha de ingreso  (DD/MM/AAAA)',
            tamanio_fuente=13,
            color=COLOR_TEXTO_SUAVE,
        ))
        self.campo_fecha_inicio = crear_campo_texto(sugerencia='Ej: 01/01/2024')
        tarjeta.add_widget(self.campo_fecha_inicio)

        tarjeta.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # ── Fecha de retiro ──
        tarjeta.add_widget(crear_etiqueta(
            'Fecha de retiro  (DD/MM/AAAA)',
            tamanio_fuente=13,
            color=COLOR_TEXTO_SUAVE,
        ))
        self.campo_fecha_fin = crear_campo_texto(sugerencia='Ej: 31/12/2024')
        tarjeta.add_widget(self.campo_fecha_fin)

        tarjeta.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # ── Salario ──
        tarjeta.add_widget(crear_etiqueta(
            'Salario mensual (SMMLV o superior, sin puntos)',
            tamanio_fuente=13,
            color=COLOR_TEXTO_SUAVE,
        ))
        self.campo_salario = crear_campo_texto(
            sugerencia='Ej: 1750905',
            filtro_entrada='int',   # Solo permite dígitos enteros
        )
        tarjeta.add_widget(self.campo_salario)

        tarjeta.add_widget(Widget(size_hint_y=None, height=dp(6)))

        # ── Botón calcular ──
        boton_calcular = crear_boton(
            'Calcular liquidación',
            color_fondo=COLOR_PRIMARIO,
            alto=dp(50),
        )
        boton_calcular.bind(on_release=self._calcular_liquidacion)
        tarjeta.add_widget(boton_calcular)

        tarjeta.bind(minimum_height=tarjeta.setter('height'))
        return tarjeta

    # ── Tarjeta: resultados ───────────────────────────────────────────────────

    def _construir_tarjeta_resultados(self):
        """
        Construye la tarjeta que muestra los resultados detallados de la
        liquidación después de presionar el botón 'Calcular'.

        Crea una fila por cada concepto de liquidación y una fila resaltada
        para el total. Las referencias a los Labels de valor se almacenan como
        atributos de instancia para ser actualizadas por `_calcular_liquidacion`.

        Atributos de instancia creados:
            self.etiqueta_dias       : Label para los días trabajados.
            self.etiqueta_cesantias  : Label para el valor de cesantías.
            self.etiqueta_intereses  : Label para los intereses sobre cesantías.
            self.etiqueta_vacaciones : Label para el valor de vacaciones.
            self.etiqueta_prima      : Label para el valor de prima de servicios.
            self.etiqueta_total      : Label para el total de la liquidación.

        Retorna:
            BoxLayout: Tarjeta de resultados lista para agregar al cuerpo.
        """
        tarjeta = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(16), dp(14)],
            spacing=dp(6),
        )
        aplicar_fondo_redondeado(tarjeta, COLOR_FONDO_TARJETA)

        tarjeta.add_widget(crear_etiqueta(
            'Resultados',
            tamanio_fuente=16,
            negrita=True,
            color=COLOR_PRIMARIO,
            alto=dp(30),
        ))
        tarjeta.add_widget(crear_linea_divisora())

        # Filas individuales por concepto
        fila_dias, self.etiqueta_dias = crear_fila_resultado('Días trabajados (método 360):')
        tarjeta.add_widget(fila_dias)

        fila_ces, self.etiqueta_cesantias = crear_fila_resultado('Cesantías:')
        tarjeta.add_widget(fila_ces)

        fila_int, self.etiqueta_intereses = crear_fila_resultado('Intereses sobre cesantías:')
        tarjeta.add_widget(fila_int)

        fila_vac, self.etiqueta_vacaciones = crear_fila_resultado('Vacaciones:')
        tarjeta.add_widget(fila_vac)

        fila_pri, self.etiqueta_prima = crear_fila_resultado('Prima de servicios:')
        tarjeta.add_widget(fila_pri)

        tarjeta.add_widget(crear_linea_divisora())

        # ── Fila de total (resaltada) ──
        fila_total = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(44),
            padding=[dp(4), 0],
        )
        aplicar_fondo_redondeado(fila_total, COLOR_FONDO_RESULTADO, radio=8)

        fila_total.add_widget(crear_etiqueta(
            'TOTAL LIQUIDACIÓN:',
            tamanio_fuente=15,
            negrita=True,
            color=COLOR_EXITO,
            alineacion='left',
        ))
        self.etiqueta_total = crear_etiqueta(
            '$ —',
            tamanio_fuente=17,
            color=COLOR_EXITO,
            negrita=True,
            alineacion='right',
        )
        fila_total.add_widget(self.etiqueta_total)
        tarjeta.add_widget(fila_total)

        tarjeta.bind(minimum_height=tarjeta.setter('height'))
        return tarjeta

    # ── Tarjeta: botones de consulta individual ───────────────────────────────

    def _construir_tarjeta_acciones(self):
        """
        Construye la tarjeta con los botones de consulta individual de cada
        concepto de liquidación y el botón para limpiar el formulario.

        Botones disponibles:
            - Ver días trabajados
            - Ver cesantías
            - Ver intereses sobre cesantías
            - Ver vacaciones
            - Ver prima de servicios
            - Limpiar (reinicia todos los campos y resultados)

        Retorna:
            BoxLayout: Tarjeta de acciones lista para agregar al cuerpo.
        """
        tarjeta = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(16), dp(14)],
            spacing=dp(8),
        )
        aplicar_fondo_redondeado(tarjeta, COLOR_FONDO_TARJETA)

        tarjeta.add_widget(crear_etiqueta(
            'Acciones',
            tamanio_fuente=16,
            negrita=True,
            color=COLOR_PRIMARIO,
            alto=dp(30),
        ))
        tarjeta.add_widget(crear_linea_divisora())
        tarjeta.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # Cuadrícula de 2 columnas para los botones
        cuadricula_botones = GridLayout(
            cols=2,
            size_hint_y=None,
            spacing=dp(10),
            height=dp(106),
        )

        # ── Botón: días trabajados ──
        boton_dias = crear_boton(
            'Ver días trabajados',
            color_fondo=COLOR_BOTON_SECUNDARIO,
            alto=dp(46),
        )
        boton_dias.bind(on_release=self._mostrar_dias_trabajados)
        cuadricula_botones.add_widget(boton_dias)

        # ── Botón: cesantías ──
        boton_cesantias = crear_boton(
            'Ver cesantías',
            color_fondo=COLOR_BOTON_SECUNDARIO,
            alto=dp(46),
        )
        boton_cesantias.bind(on_release=self._mostrar_cesantias)
        cuadricula_botones.add_widget(boton_cesantias)

        # ── Botón: intereses ──
        boton_intereses = crear_boton(
            'Ver intereses',
            color_fondo=COLOR_BOTON_SECUNDARIO,
            alto=dp(46),
        )
        boton_intereses.bind(on_release=self._mostrar_intereses)
        cuadricula_botones.add_widget(boton_intereses)

        # ── Botón: vacaciones ──
        boton_vacaciones = crear_boton(
            'Ver vacaciones',
            color_fondo=COLOR_BOTON_SECUNDARIO,
            alto=dp(46),
        )
        boton_vacaciones.bind(on_release=self._mostrar_vacaciones)
        cuadricula_botones.add_widget(boton_vacaciones)

        # ── Botón: prima ──
        boton_prima = crear_boton(
            'Ver prima',
            color_fondo=COLOR_BOTON_SECUNDARIO,
            alto=dp(46),
        )
        boton_prima.bind(on_release=self._mostrar_prima)
        cuadricula_botones.add_widget(boton_prima)

        # ── Botón: limpiar ──
        boton_limpiar = crear_boton(
            'Limpiar',
            color_fondo=COLOR_BOTON_LIMPIAR,
            alto=dp(46),
        )
        boton_limpiar.bind(on_release=self._limpiar_formulario)
        cuadricula_botones.add_widget(boton_limpiar)

        tarjeta.add_widget(cuadricula_botones)
        tarjeta.bind(minimum_height=tarjeta.setter('height'))
        return tarjeta

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS DE LÓGICA DE INTERFAZ
    # Estos métodos leen los campos, invocan el modelo y actualizan la vista.
    # No modifican ninguna regla de negocio: solo coordinan la GUI con el modelo.
    # ──────────────────────────────────────────────────────────────────────────

    def _leer_y_validar_entradas(self):
        """
        Lee los tres campos de entrada (fecha inicio, fecha fin, salario),
        los valida delegando en el modelo de lógica y retorna los valores
        listos para el cálculo.

        Lanza las excepciones definidas en `errores.py` si algún dato es
        inválido, para que el método llamante pueda capturarlas y mostrar
        el mensaje apropiado al usuario.

        Retorna:
            tuple: (dias_trabajados: int, salario: int)
                - dias_trabajados: días entre las dos fechas (método 360).
                - salario        : salario mensual en pesos colombianos.

        Lanza:
            errores.ErrorFechaFormatoIncorrecto : fecha vacía o mal formateada.
            errores.ErrorFechaIncorrecta        : fecha fin anterior a fecha inicio.
            errores.ErrorSalarioNoEntero        : salario vacío o no numérico.
            errores.ErrorSalarioMenorDeCero     : salario igual o menor a cero.
        """
        fecha_inicio = self.campo_fecha_inicio.text.strip()
        fecha_fin    = self.campo_fecha_fin.text.strip()
        texto_salario = self.campo_salario.text.strip()

        # Verificación de campos vacíos antes de llamar al modelo
        if not fecha_inicio or not fecha_fin:
            raise errores.ErrorFechaFormatoIncorrecto()
        if not texto_salario:
            raise errores.ErrorSalarioNoEntero()

        # Calcula los días trabajados (delega validación de fechas al modelo)
        dias_trabajados = logicaLiquidacion.calcular_tiempo_trabajado_dias(
            fecha_inicio, fecha_fin
        )

        # Convierte el texto del salario a entero
        try:
            salario = int(texto_salario)
        except ValueError:
            raise errores.ErrorSalarioNoEntero()

        # Valida que el salario cumpla las reglas de negocio
        logicaLiquidacion.validar_salario(salario)

        return dias_trabajados, salario

    def _calcular_liquidacion(self, *_):
        """
        Método enlazado al botón '⚡ Calcular liquidación'.

        Orquesta el flujo completo:
            1. Lee y valida las entradas del usuario.
            2. Calcula cada concepto de liquidación usando el modelo.
            3. Actualiza las etiquetas de resultado en la tarjeta de resultados.
            4. En caso de error, muestra un popup descriptivo al usuario.

        Los cálculos delegan completamente en `logicaLiquidacion`:
            - calcular_cesantias
            - calcular_interes_cesantias
            - calcular_vacaciones
            - calcular_prima_servicios
            - calcular_pago_neto
        """
        try:
            dias_trabajados, salario = self._leer_y_validar_entradas()

            # ── Cálculo de cada concepto ──────────────────────────────────────
            valor_cesantias  = logicaLiquidacion.calcular_cesantias(salario, dias_trabajados)
            valor_intereses  = logicaLiquidacion.calcular_interes_cesantias(valor_cesantias, dias_trabajados)
            valor_vacaciones = logicaLiquidacion.calcular_vacaciones(salario, dias_trabajados)
            valor_prima      = logicaLiquidacion.calcular_prima_servicios(salario, dias_trabajados)

            # Suma de todos los conceptos para obtener el pago neto total
            valor_total = logicaLiquidacion.calcular_pago_neto(
                valor_cesantias,
                valor_intereses,
                valor_vacaciones,
                valor_prima,
            )

            # ── Actualización de la tarjeta de resultados ─────────────────────
            self.etiqueta_dias.text       = str(dias_trabajados)
            self.etiqueta_cesantias.text  = formatear_pesos(valor_cesantias)
            self.etiqueta_intereses.text  = formatear_pesos(valor_intereses)
            self.etiqueta_vacaciones.text = formatear_pesos(valor_vacaciones)
            self.etiqueta_prima.text      = formatear_pesos(valor_prima)
            self.etiqueta_total.text      = formatear_pesos(valor_total)

        except (
            errores.ErrorFechaFormatoIncorrecto,
            errores.ErrorFechaIncorrecta,
            errores.ErrorSalarioNoEntero,
            errores.ErrorSalarioMenorDeCero,
        ) as error_validacion:
            mostrar_popup('Error de entrada', str(error_validacion), color=COLOR_ERROR)

        except Exception as error_inesperado:
            mostrar_popup('Error inesperado', str(error_inesperado), color=COLOR_ADVERTENCIA)

    def _mostrar_dias_trabajados(self, *_):
        """
        Método enlazado al botón 'Ver días trabajados'.

        Lee y valida las fechas ingresadas, calcula los días trabajados con el
        método 360 y muestra el resultado en un popup informativo.

        En caso de error de validación, muestra el mensaje de error en un popup.
        """
        try:
            dias_trabajados, _ = self._leer_y_validar_entradas()

            mostrar_popup(
                'Días trabajados',
                f'Total días (método 360):\n\n{dias_trabajados} días',
                color=COLOR_PRIMARIO,
            )
        except Exception as error:
            mostrar_popup('Error', str(error), color=COLOR_ERROR)

    def _mostrar_cesantias(self, *_):
        """
        Método enlazado al botón 'Ver cesantías'.

        Calcula el valor de las cesantías según la fórmula:
            cesantías = salario × días / 360

        Muestra el resultado en un popup informativo.
        En caso de error de validación, muestra el mensaje de error en un popup.
        """
        try:
            dias_trabajados, salario = self._leer_y_validar_entradas()

            # Cesantías = Salario × días trabajados / 360
            valor_cesantias = logicaLiquidacion.calcular_cesantias(salario, dias_trabajados)

            mostrar_popup(
                'Cesantías',
                f'Salario × días / 360\n\n{formatear_pesos(valor_cesantias)}',
                color=COLOR_EXITO,
            )
        except Exception as error:
            mostrar_popup('Error', str(error), color=COLOR_ERROR)

    def _mostrar_intereses(self, *_):
        """
        Método enlazado al botón 'Ver intereses'.

        Calcula primero las cesantías y luego los intereses sobre ellas:
            intereses = cesantías × días × 12% / 360

        Muestra el resultado en un popup informativo.
        En caso de error de validación, muestra el mensaje de error en un popup.
        """
        try:
            dias_trabajados, salario = self._leer_y_validar_entradas()

            # Primero se calculan las cesantías base
            valor_cesantias = logicaLiquidacion.calcular_cesantias(salario, dias_trabajados)

            # Luego los intereses sobre las cesantías (tasa anual del 12%)
            valor_intereses = logicaLiquidacion.calcular_interes_cesantias(
                valor_cesantias, dias_trabajados
            )

            mostrar_popup(
                'Intereses sobre cesantías',
                f'Cesantías × días × 12% / 360\n\n{formatear_pesos(valor_intereses)}',
                color=COLOR_EXITO,
            )
        except Exception as error:
            mostrar_popup('Error', str(error), color=COLOR_ERROR)

    def _mostrar_vacaciones(self, *_):
        """
        Método enlazado al botón 'Ver vacaciones'.

        Calcula el valor de las vacaciones según la fórmula:
            vacaciones = salario × días / 720

        Muestra el resultado en un popup informativo.
        En caso de error de validación, muestra el mensaje de error en un popup.
        """
        try:
            dias_trabajados, salario = self._leer_y_validar_entradas()

            # Vacaciones = Salario × días trabajados / 720
            valor_vacaciones = logicaLiquidacion.calcular_vacaciones(salario, dias_trabajados)

            mostrar_popup(
                'Vacaciones',
                f'Salario × días / 720\n\n{formatear_pesos(valor_vacaciones)}',
                color=COLOR_EXITO,
            )
        except Exception as error:
            mostrar_popup('Error', str(error), color=COLOR_ERROR)

    def _mostrar_prima(self, *_):
        """
        Método enlazado al botón 'Ver prima'.

        Calcula el valor de la prima de servicios según la fórmula:
            prima = salario × días / 360

        Muestra el resultado en un popup informativo.
        En caso de error de validación, muestra el mensaje de error en un popup.
        """
        try:
            dias_trabajados, salario = self._leer_y_validar_entradas()

            # Prima de servicios = Salario × días trabajados / 360
            valor_prima = logicaLiquidacion.calcular_prima_servicios(salario, dias_trabajados)

            mostrar_popup(
                'Prima de servicios',
                f'Salario × días / 360\n\n{formatear_pesos(valor_prima)}',
                color=COLOR_EXITO,
            )
        except Exception as error:
            mostrar_popup('Error', str(error), color=COLOR_ERROR)

    def _limpiar_formulario(self, *_):
        """
        Método enlazado al botón 'Limpiar'.

        Restablece todos los campos de entrada a cadena vacía y todas las
        etiquetas de resultado al valor inicial '—' (o '$ —' para el total),
        dejando la interfaz lista para ingresar nuevos datos.
        """
        # Limpia los campos de entrada
        self.campo_fecha_inicio.text = ''
        self.campo_fecha_fin.text    = ''
        self.campo_salario.text      = ''

        # Restablece las etiquetas de resultado al estado inicial
        for etiqueta in (
            self.etiqueta_dias,
            self.etiqueta_cesantias,
            self.etiqueta_intereses,
            self.etiqueta_vacaciones,
            self.etiqueta_prima,
        ):
            etiqueta.text = '—'

        self.etiqueta_total.text = '$ —'


# ──────────────────────────────────────────────────────────────────────────────
# APLICACIÓN KIVY
# ──────────────────────────────────────────────────────────────────────────────

class LiquidacionApp(App):
    """
    Clase principal de la aplicación Kivy.

    Configura el título de la ventana, el tamaño inicial (útil en escritorio)
    y retorna el layout raíz `LiquidacionLayout` como widget raíz de la app.
    """

    def build(self):
        """
        Método requerido por Kivy. Se ejecuta al iniciar la aplicación.

        Establece:
            - Título de la ventana del sistema operativo.
            - Tamaño inicial de la ventana (420 × 780 px, similar a móvil).

        Retorna:
            LiquidacionLayout: Layout raíz con toda la interfaz construida.
        """
        self.title = 'Calculadora de Liquidación Laboral · Colombia'
        Window.size = (420, 780)
        return LiquidacionLayout()


# Punto de entrada cuando el script se ejecuta directamente
if __name__ == '__main__':
    LiquidacionApp().run()