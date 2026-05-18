from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus import NextPageTemplate
from reportlab.platypus import Flowable
import io

# ── Colores ──────────────────────────────────────────────────────────────────
AZUL       = colors.HexColor('#1a3a5c')
DORADO     = colors.HexColor('#c9a84c')
TEXTO      = colors.HexColor('#0e0c0a')
CREMA      = colors.HexColor('#ede9e2')
BLANCO     = colors.HexColor('#f7f4ef')
GRIS_LINE  = colors.HexColor('#cccccc')
GRIS_LIGHT = colors.HexColor('#f0eeeb')

# ── Estilos ───────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['cover_title'] = ParagraphStyle(
        'cover_title', fontName='Helvetica-Bold', fontSize=36,
        textColor=BLANCO, alignment=TA_CENTER, leading=44, spaceAfter=10
    )
    s['cover_sub'] = ParagraphStyle(
        'cover_sub', fontName='Helvetica', fontSize=18,
        textColor=DORADO, alignment=TA_CENTER, leading=24, spaceAfter=6
    )
    s['cover_date'] = ParagraphStyle(
        'cover_date', fontName='Helvetica', fontSize=12,
        textColor=colors.HexColor('#adc4e0'), alignment=TA_CENTER, leading=18
    )
    s['section_title'] = ParagraphStyle(
        'section_title', fontName='Helvetica-Bold', fontSize=18,
        textColor=AZUL, spaceAfter=10, spaceBefore=6, leading=22
    )
    s['sub_title'] = ParagraphStyle(
        'sub_title', fontName='Helvetica-Bold', fontSize=13,
        textColor=DORADO, spaceAfter=6, spaceBefore=4, leading=17
    )
    s['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=17, spaceAfter=6, alignment=TA_JUSTIFY
    )
    s['body_center'] = ParagraphStyle(
        'body_center', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=17, spaceAfter=6, alignment=TA_CENTER
    )
    s['bullet'] = ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=17, spaceAfter=4,
        leftIndent=18, firstLineIndent=0
    )
    s['step'] = ParagraphStyle(
        'step', fontName='Helvetica-Bold', fontSize=11,
        textColor=AZUL, leading=17, spaceAfter=2, leftIndent=0
    )
    s['step_desc'] = ParagraphStyle(
        'step_desc', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=16, spaceAfter=10, leftIndent=28
    )
    s['qa_q'] = ParagraphStyle(
        'qa_q', fontName='Helvetica-Bold', fontSize=11,
        textColor=AZUL, leading=17, spaceAfter=2
    )
    s['qa_a'] = ParagraphStyle(
        'qa_a', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=16, spaceAfter=10, leftIndent=14
    )
    s['footer'] = ParagraphStyle(
        'footer', fontName='Helvetica', fontSize=8,
        textColor=colors.HexColor('#888888'), alignment=TA_CENTER
    )
    s['toc_entry'] = ParagraphStyle(
        'toc_entry', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=20, leftIndent=0
    )
    s['toc_title'] = ParagraphStyle(
        'toc_title', fontName='Helvetica-Bold', fontSize=18,
        textColor=AZUL, spaceAfter=16, leading=22
    )
    s['note'] = ParagraphStyle(
        'note', fontName='Helvetica-Oblique', fontSize=10,
        textColor=colors.HexColor('#555555'), leading=15, spaceAfter=6,
        leftIndent=14, backColor=GRIS_LIGHT, borderPad=6
    )
    s['tip_box'] = ParagraphStyle(
        'tip_box', fontName='Helvetica', fontSize=11,
        textColor=TEXTO, leading=17, spaceAfter=4, leftIndent=24
    )
    return s

ST = make_styles()

# ── Número de página y footer ─────────────────────────────────────────────────
def footer_canvas(canvas_obj, doc):
    canvas_obj.saveState()
    w, h = letter
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(colors.HexColor('#888888'))
    footer_text = 'Content Command Center 2.0  ©  Boxa Studio Design'
    canvas_obj.drawCentredString(w / 2, 0.5 * inch, footer_text)
    if doc.page > 1:
        canvas_obj.drawRightString(w - inch, 0.5 * inch, str(doc.page - 1))
    canvas_obj.restoreState()

# ── Bloque de portada (dibujado en canvas directo) ────────────────────────────
def cover_page(canvas_obj, doc):
    w, h = letter
    # Fondo azul oscuro completo
    canvas_obj.setFillColor(AZUL)
    canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)
    # Rectángulo decorativo superior
    canvas_obj.setFillColor(DORADO)
    canvas_obj.rect(0, h - 6, w, 6, fill=1, stroke=0)
    # Rectángulo decorativo inferior
    canvas_obj.rect(0, 0, w, 6, fill=1, stroke=0)
    # Franja central suave
    canvas_obj.setFillColor(colors.HexColor('#22497a'))
    canvas_obj.roundRect(inch * 0.8, h * 0.32, w - inch * 1.6, h * 0.42,
                          radius=14, fill=1, stroke=0)
    # Icono Notion (N estilizada)
    cx, cy = w / 2, h * 0.78
    canvas_obj.setFillColor(BLANCO)
    canvas_obj.setFont('Helvetica-Bold', 72)
    canvas_obj.drawCentredString(cx, cy - 26, 'N')
    # Círculo detrás del ícono
    canvas_obj.setStrokeColor(DORADO)
    canvas_obj.setLineWidth(2.5)
    canvas_obj.circle(cx, cy - 6, 54, fill=0, stroke=1)

    # Título
    canvas_obj.setFont('Helvetica-Bold', 38)
    canvas_obj.setFillColor(BLANCO)
    canvas_obj.drawCentredString(w / 2, h * 0.54, 'Content Command Center 2.0')
    # Subtítulo
    canvas_obj.setFont('Helvetica', 19)
    canvas_obj.setFillColor(DORADO)
    canvas_obj.drawCentredString(w / 2, h * 0.47, 'Guía de Configuración Rápida')
    # Línea decorativa
    canvas_obj.setStrokeColor(DORADO)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(w * 0.3, h * 0.43, w * 0.7, h * 0.43)
    # Fecha
    canvas_obj.setFont('Helvetica', 12)
    canvas_obj.setFillColor(colors.HexColor('#adc4e0'))
    canvas_obj.drawCentredString(w / 2, h * 0.38, 'Actualizado Mayo 2026')
    # Footer
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(colors.HexColor('#6688aa'))
    canvas_obj.drawCentredString(w / 2, 0.5 * inch,
                                  'Content Command Center 2.0  ©  Boxa Studio Design')

# ── Separador de sección ──────────────────────────────────────────────────────
def section_sep():
    return HRFlowable(width='100%', thickness=1, color=GRIS_LINE,
                       spaceAfter=14, spaceBefore=4)

# ── Caja de nota/tip ──────────────────────────────────────────────────────────
def tip_box(icon, text):
    data = [[Paragraph(f'{icon}  {text}', ST['tip_box'])]]
    t = Table(data, colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_LIGHT),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, GRIS_LINE),
    ]))
    return t

# ── Paso numerado ─────────────────────────────────────────────────────────────
def step_row(num, title, desc, icon=''):
    num_cell = Paragraph(f'<b>{num}</b>', ParagraphStyle(
        'num', fontName='Helvetica-Bold', fontSize=13, textColor=BLANCO,
        alignment=TA_CENTER, leading=18
    ))
    content = [
        Paragraph(f'{icon}  <b>{title}</b>' if icon else f'<b>{title}</b>', ST['step']),
        Paragraph(desc, ST['step_desc'])
    ]
    t = Table([[num_cell, content]], colWidths=[0.38 * inch, 6.12 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), AZUL),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (0, 0), 6),
        ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ('LEFTPADDING',   (0, 0), (0, 0), 0),
        ('RIGHTPADDING',  (0, 0), (0, 0), 0),
        ('TOPPADDING',    (1, 0), (1, 0), 4),
        ('BOTTOMPADDING', (1, 0), (1, 0), 4),
        ('LEFTPADDING',   (1, 0), (1, 0), 10),
        ('RIGHTPADDING',  (1, 0), (1, 0), 4),
        ('ROUNDEDCORNERS', [4]),
        ('BOX', (0, 0), (-1, -1), 0.5, GRIS_LINE),
    ]))
    return t

# ── Filas de vistas ───────────────────────────────────────────────────────────
def vista_row(icon, name, desc):
    data = [[
        Paragraph(icon, ParagraphStyle('ic', fontSize=16, alignment=TA_CENTER, leading=18)),
        Paragraph(f'<b>{name}</b>', ST['sub_title']),
        Paragraph(desc, ST['body'])
    ]]
    t = Table(data, colWidths=[0.45 * inch, 1.7 * inch, 4.35 * inch])
    t.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (1, 0), (1, 0), 8),
        ('LINEBELOW',     (0, 0), (-1, -1), 0.5, GRIS_LINE),
    ]))
    return t

# ── Q&A ───────────────────────────────────────────────────────────────────────
def qa_block(q, a):
    return KeepTogether([
        Paragraph(f'❓ {q}', ST['qa_q']),
        Paragraph(f'→  {a}', ST['qa_a']),
    ])

# ── Documento principal ────────────────────────────────────────────────────────
def build_pdf(filename):
    doc = BaseDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=0.8 * inch,
        title='Content Command Center 2.0 – Guía de Configuración',
        author='Boxa Studio Design',
    )
    frame = Frame(inch, 0.8 * inch, letter[0] - 2 * inch,
                  letter[1] - 1.8 * inch, id='normal')
    cover_tmpl  = PageTemplate(id='cover',  frames=[frame],
                                onPage=cover_page)
    normal_tmpl = PageTemplate(id='normal', frames=[frame],
                                onPage=footer_canvas)
    doc.addPageTemplates([cover_tmpl, normal_tmpl])

    story = []

    # ── PORTADA ──────────────────────────────────────────────────────────────
    # La portada se dibuja completamente en el callback cover_page.
    # Solo cambiamos al template normal y saltamos de página.
    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())

    # ── ÍNDICE ────────────────────────────────────────────────────────────────
    story.append(Paragraph('Índice de Contenidos', ST['toc_title']))
    toc_items = [
        ('1.', '¿Qué es Content Command Center?', '2'),
        ('2.', 'Requisitos previos',              '2'),
        ('3.', 'Cómo duplicar la plantilla',      '3'),
        ('4.', 'Las 6 secciones principales',     '4'),
        ('5.', 'Agregar tu primer cliente',       '6'),
        ('6.', 'Troubleshooting',                 '7'),
        ('7.', 'Tips Pro – Características avanzadas', '8'),
        ('8.', 'Contacto y soporte',              '9'),
    ]
    toc_data = [[
        Paragraph(f'<b>{n}</b>', ST['toc_entry']),
        Paragraph(title, ST['toc_entry']),
        Paragraph(f'<b>{pg}</b>', ParagraphStyle(
            'pg', fontName='Helvetica-Bold', fontSize=11, alignment=TA_RIGHT,
            textColor=AZUL, leading=20
        ))
    ] for n, title, pg in toc_items]
    toc_table = Table(toc_data, colWidths=[0.4 * inch, 5.4 * inch, 0.7 * inch])
    toc_table.setStyle(TableStyle([
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW',  (0, 0), (-1, -1), 0.4, GRIS_LINE),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ── SECCIÓN 1 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('1. ¿Qué es Content Command Center?', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Content Command Center 2.0 es un sistema de gestión de contenido digital '
        'construido sobre Notion. Centraliza todo tu flujo de trabajo: desde la idea '
        'hasta la publicación, en un solo espacio conectado y visual.',
        ST['body']
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph('¿Para quién es?', ST['sub_title']))
    story.append(Paragraph(
        'Diseñado para creadores de contenido, agencias de marketing, community managers '
        'y estudios de diseño que gestionan múltiples clientes o marcas simultáneamente.',
        ST['body']
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph('¿Qué problema resuelve?', ST['sub_title']))
    for b in [
        '✓  Elimina el caos de manejar calendarios en hojas de cálculo separadas.',
        '✓  Conecta clientes, contenidos, estrategia y assets en una sola fuente de verdad.',
        '✓  Reduce el tiempo de coordinación con clientes mediante flujos de aprobación integrados.',
    ]:
        story.append(Paragraph(b, ST['bullet']))
    story.append(Spacer(1, 16))

    # ── SECCIÓN 2 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('2. Requisitos Previos', ST['section_title']))
    story.append(section_sep())
    for b in [
        '✓  Cuenta Notion activa (plan Free o de pago)',
        '✓  Navegador web actualizado (Chrome, Firefox, Safari o Edge)',
        '✓  Conexión a internet estable',
    ]:
        story.append(Paragraph(b, ST['bullet']))
    story.append(Spacer(1, 10))
    story.append(tip_box('ℹ️', 'No requiere instalación adicional ni plugins. Funciona '
                               '100% dentro de Notion desde el navegador o la app de escritorio.'))
    story.append(PageBreak())

    # ── SECCIÓN 3 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('3. Cómo Duplicar la Plantilla', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Sigue estos 6 pasos para tener Content Command Center 2.0 en tu workspace '
        'en menos de 2 minutos.', ST['body']
    ))
    story.append(Spacer(1, 10))

    steps = [
        ('1', 'Ir al link compartido', '🔗',
         'Abre en tu navegador el link de Notion que te fue enviado junto a esta guía. '
         'Verás la plantilla en modo "solo lectura".'),
        ('2', 'Hacer clic en "Duplicar"', '📋',
         'En la esquina superior derecha de la página, encontrarás el botón azul '
         '"Duplicar". Haz clic en él. Si no aparece, asegúrate de haber iniciado sesión en Notion.'),
        ('3', 'Seleccionar tu workspace', '🏠',
         'Un menú desplegable mostrará todos los workspaces asociados a tu cuenta. '
         'Selecciona el espacio de trabajo donde deseas guardar la plantilla.'),
        ('4', 'Esperar la duplicación', '⏳',
         'Notion procesará la copia. Este proceso puede tomar entre 20 y 60 segundos '
         'dependiendo de la velocidad de tu conexión. No cierres la ventana.'),
        ('5', 'Confirmar el popup', '✅',
         'Aparecerá un popup de confirmación. Haz clic en "Aceptar" o en el link '
         'directo a la plantilla duplicada para abrirla inmediatamente.'),
        ('6', '¡Listo para usar!', '🎉',
         'La plantilla ya está en tu cuenta con todos sus datos de ejemplo. '
         'Puedes comenzar a personalizarla de inmediato.'),
    ]
    for num, title, icon, desc in steps:
        story.append(step_row(num, title, desc, icon))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 8))
    story.append(tip_box('⚠️', 'Si el botón "Duplicar" no aparece, intenta abrir el link '
                               'en una ventana de incógnito o cierra y vuelve a iniciar sesión en Notion.'))
    story.append(PageBreak())

    # ── SECCIÓN 4 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('4. Las 6 Secciones Principales', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Al abrir la plantilla verás el Dashboard principal. Estas son las secciones '
        'que encontrarás y cómo utilizarlas:', ST['body']
    ))
    story.append(Spacer(1, 10))

    vistas = [
        ('🏠', 'Dashboard principal',
         'La página de inicio. Muestra un resumen de todo: contenidos del día, '
         'alertas activas y accesos rápidos a las secciones más usadas. '
         'Es tu punto de entrada diario.'),
        ('👥', 'Clientes',
         'Base de datos con todos tus clientes. Cada cliente tiene su perfil con '
         'redes sociales, colores de marca, estado (Activo / Onboarding / Pausado) '
         'y todos los contenidos relacionados mediante relaciones automáticas.'),
        ('📅', 'Calendario Editorial',
         'Vista de calendario donde se visualizan todas las publicaciones programadas '
         'por fecha. Filtra por cliente, plataforma o estado de producción. '
         'Soporta: Post, Reel, Story, Carrusel, Video, Thread, Newsletter y más.'),
        ('🏷️', 'Estados y Prioridades',
         'Cada pieza de contenido tiene dos flujos: Estado de producción '
         '(Idea → Guion → Redacción → Edición → Publicado) y Estado de aprobación '
         '(Esperando cliente / Aprobado / Requiere cambios). Prioridades: Alta, Media, Baja.'),
        ('📁', 'Repositorio de Assets',
         'Base de datos vinculada donde se almacenan y organizan todos los archivos '
         'multimedia: imágenes, videos, logos, tipografías. Relacionados directamente '
         'con cada pieza de contenido.'),
        ('🚨', 'Sistema de Alertas – Modo Pánico',
         'Vista especial filtrada con una fórmula automática que detecta contenidos '
         'urgentes o en crisis. Se activa automáticamente cuando una pieza cumple '
         'condiciones críticas de fecha o estado.'),
    ]
    for icon, name, desc in vistas:
        story.append(vista_row(icon, name, desc))
    story.append(PageBreak())

    # ── SECCIÓN 5 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('5. Agregar tu Primer Cliente', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Sigue estos pasos para registrar tu primer cliente y comenzar a crear '
        'contenidos asociados a él:', ST['body']
    ))
    story.append(Spacer(1, 10))

    client_steps = [
        ('1', 'Ir a la sección Clientes', '👥',
         'Desde el Dashboard, haz clic en la sección "Clientes" en el menú lateral '
         'o en el acceso rápido del Dashboard.'),
        ('2', 'Crear nuevo registro', '➕',
         'Haz clic en "+ Nuevo" en la parte superior de la tabla para crear '
         'una nueva entrada de cliente.'),
        ('3', 'Rellenar el perfil', '✏️',
         'Completa los campos: Nombre del cliente, redes sociales activas, '
         'colores de marca (hex), email de contacto y estado inicial (Onboarding).'),
        ('4', 'Guardar el perfil', '💾',
         'Cierra la ventana del registro. Los datos se guardan automáticamente '
         'en tiempo real — no hay botón de "guardar" separado en Notion.'),
        ('5', 'Verificar en el Calendario', '📅',
         'Al crear contenido y vincularlo a este cliente, aparecerá automáticamente '
         'en el Calendario Editorial con todos sus datos de perfil disponibles.'),
    ]
    for num, title, icon, desc in client_steps:
        story.append(step_row(num, title, desc, icon))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 8))
    story.append(tip_box('💡', 'Puedes agregar todos tus clientes desde el inicio antes de '
                               'comenzar a cargar contenidos. Esto hará que las relaciones y '
                               'los filtros funcionen mejor desde el primer día.'))
    story.append(PageBreak())

    # ── SECCIÓN 6 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('6. Troubleshooting', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Soluciones a los problemas más comunes al configurar la plantilla:', ST['body']
    ))
    story.append(Spacer(1, 12))

    qas = [
        ('No veo el botón "Duplicar" en la página.',
         'Asegúrate de haber iniciado sesión en tu cuenta de Notion antes de abrir '
         'el link. Si ya estás logueado, intenta recargar la página (F5) o abrirla '
         'en una ventana de incógnito.'),
        ('La plantilla dice "No tienes acceso".',
         'El link puede haber vencido o haber sido desactivado. Contacta al propietario '
         'en boxpopular@gmail.com para que reenvíe el link de acceso correcto.'),
        ('La duplicación se cortó a mitad.',
         'Esto ocurre por conexión inestable. Recarga la página, ve a tu workspace '
         'en Notion y verifica si la plantilla ya fue copiada parcialmente. Si existe, '
         'elimínala y vuelve a intentar desde el link original.'),
        ('¿Puedo usar esto con el plan gratuito de Notion?',
         'Sí, Content Command Center 2.0 funciona perfectamente con Notion Free. '
         'Todas las bases de datos, relaciones y vistas están disponibles sin costo. '
         'Solo hay límites en el almacenamiento de archivos (5 MB por archivo en Free).'),
        ('Las relaciones entre bases de datos no funcionan.',
         'Esto puede ocurrir si se editó accidentalmente el esquema al duplicar. '
         'No elimines las bases de datos del SYSTEM_BACKEND. Si algo falla, '
         'contacta soporte con una captura de pantalla del error.'),
    ]
    for q, a in qas:
        story.append(qa_block(q, a))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ── SECCIÓN 7 ─────────────────────────────────────────────────────────────
    story.append(Paragraph('7. Tips Pro – Características Avanzadas', ST['section_title']))
    story.append(section_sep())
    story.append(Paragraph(
        'Una vez que dominas lo básico, estas funciones te ayudarán a sacar el '
        'máximo provecho del sistema:', ST['body']
    ))
    story.append(Spacer(1, 10))

    tips = [
        ('🔗', 'Relaciones entre bases de datos',
         'Cada contenido está relacionado con Clientes, Plataformas, Estrategia y '
         'Assets. Puedes navegar entre entidades relacionadas con un solo clic. '
         'Evita duplicar información — todo vive conectado.'),
        ('🔍', 'Filtros automáticos personalizados',
         'Crea vistas filtradas por responsable, fecha o cliente para ver solo lo que '
         'te corresponde. Guarda los filtros como vistas separadas para acceso rápido.'),
        ('📊', 'Vista Pipeline de Producción',
         'El nuevo tablero Kanban (columnas: Idea → Guion → Redacción → Edición → '
         'Publicado) te permite arrastrar contenidos entre etapas visualmente.'),
        ('👤', 'Campo Responsable',
         'Asigna cada pieza de contenido a un miembro del equipo con el campo '
         '"Responsable". Filtra la vista HOY por tu nombre para ver solo tus tareas del día.'),
        ('⌨️', 'Keyboard shortcuts útiles en Notion',
         '/  →  Abre el menú de bloques\n'
         'Ctrl+D  →  Duplica un bloque\n'
         'Ctrl+[  →  Navegación hacia atrás\n'
         '@  →  Mencionar una página o persona\n'
         'Ctrl+Shift+H  →  Resaltar texto'),
    ]
    for icon, title, desc in tips:
        data = [[
            Paragraph(icon, ParagraphStyle('ic2', fontSize=18, alignment=TA_CENTER, leading=22)),
            [Paragraph(f'<b>{title}</b>', ST['sub_title']),
             Paragraph(desc, ST['body'])]
        ]]
        t = Table(data, colWidths=[0.45 * inch, 6.05 * inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (1, 0), (1, 0), 10),
            ('LINEBELOW', (0, 0), (-1, -1), 0.4, GRIS_LINE),
        ]))
        story.append(t)

    story.append(PageBreak())

    # ── SECCIÓN 8: CONTACTO ───────────────────────────────────────────────────
    story.append(Paragraph('8. Contacto y Soporte', ST['section_title']))
    story.append(section_sep())

    contact_data = [
        [Paragraph('📧 Email de soporte', ST['sub_title']),
         Paragraph('boxpopular@gmail.com', ST['body'])],
        [Paragraph('▶️ Video de setup', ST['sub_title']),
         Paragraph('Disponible en YouTube — busca "Content Command Center 2.0 Setup" '
                   'o solicita el link por email.', ST['body'])],
        [Paragraph('🔄 Actualizaciones', ST['sub_title']),
         Paragraph('Las actualizaciones futuras de la plantilla son completamente '
                   'gratuitas para todos los compradores.', ST['body'])],
        [Paragraph('⏱️ Tiempo de respuesta', ST['sub_title']),
         Paragraph('Respondemos consultas por email en un máximo de 48 horas hábiles.',
                   ST['body'])],
    ]
    ct = Table(contact_data, colWidths=[2.2 * inch, 4.3 * inch])
    ct.setStyle(TableStyle([
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW',  (0, 0), (-1, -1), 0.4, GRIS_LINE),
        ('BACKGROUND', (0, 0), (0, -1), GRIS_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(ct)

    story.append(Spacer(1, 20))
    story.append(Paragraph('Preguntas Frecuentes', ST['sub_title']))
    faqs = [
        ('¿Puedo compartir la plantilla con mi equipo?',
         'Sí, puedes compartirla con todos los miembros de tu workspace de Notion '
         'sin costo adicional.'),
        ('¿Funciona en móvil?',
         'Sí, Notion tiene app para iOS y Android. La plantilla es completamente '
         'funcional en dispositivos móviles.'),
        ('¿Puedo modificar la plantilla?',
         'Absolutamente. Una vez duplicada, es completamente tuya. Puedes agregar, '
         'quitar o modificar cualquier elemento.'),
    ]
    for q, a in faqs:
        story.append(qa_block(q, a))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 20))

    # Bloque final
    final_data = [[
        Paragraph(
            '🎉  <b>¡Gracias por usar Content Command Center 2.0!</b><br/><br/>'
            'Esperamos que esta herramienta transforme la forma en que gestionas '
            'tu contenido. Si tienes sugerencias o ideas para mejorarlo, escríbenos — '
            'tu feedback construye las próximas versiones.',
            ParagraphStyle('final', fontName='Helvetica', fontSize=11,
                            textColor=BLANCO, leading=18, alignment=TA_CENTER)
        )
    ]]
    ft = Table(final_data, colWidths=[6.5 * inch])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), AZUL),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [10]),
    ]))
    story.append(ft)

    doc.build(story)
    print(f'✅  PDF generado: {filename}')

if __name__ == '__main__':
    build_pdf('/home/user/organizador-diario-BOXA-STUDIO/content-command-center-setup-guide.pdf')
