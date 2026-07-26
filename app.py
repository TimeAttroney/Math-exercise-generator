from flask import Flask, request, send_file, render_template, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import base64
import os
import sys
import traceback
from generador import GeneradorEjercicios

app = Flask(__name__)
app.config['DEBUG'] = True

# Inicializar el generador
try:
    generador = GeneradorEjercicios()
    print("✅ Generador inicializado correctamente")
except Exception as e:
    print(f"❌ Error al inicializar generador: {e}")
    sys.exit(1)

# Registrar fuentes para PDF


def registrar_fuentes():
    try:
        font_paths = [
            'C:/Windows/Fonts/times.ttf',
            'C:/Windows/Fonts/timesbd.ttf',
            'C:/Windows/Fonts/timesi.ttf',
            'C:/Windows/Fonts/timesbi.ttf',
            '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
            '/System/Library/Fonts/Time.ttf',
        ]

        font_registrada = False
        for path in font_paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont('TimesNewRoman', path))
                    font_registrada = True
                    print(f"✅ Fuente Times New Roman registrada desde: {path}")
                    break
                except:
                    continue

        if not font_registrada:
            print("⚠️ No se encontró Times New Roman, usando fuente por defecto")
    except Exception as e:
        print(f"❌ Error al registrar fuentes: {e}")


registrar_fuentes()


def imagen_base64_a_reportlab(imagen_base64, ancho=400, alto=60):
    try:
        if not imagen_base64:
            return None
        imagen_bytes = base64.b64decode(imagen_base64)
        buffer = io.BytesIO(imagen_bytes)
        img = Image(buffer, width=ancho, height=alto)
        return img
    except Exception as e:
        print(f"❌ Error al convertir imagen: {e}")
        return None


def crear_pdf_ejercicios(tipos, dificultad, cantidad_por_tipo, mostrar_soluciones=True):
    """Genera un PDF con ejercicios combinados"""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()

        titulo_style = ParagraphStyle(
            'Titulo',
            parent=styles['Heading1'],
            fontName='TimesNewRoman',
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.darkblue,
            leading=24
        )

        subtitulo_style = ParagraphStyle(
            'Subtitulo',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=15,
            textColor=colors.darkgreen,
            leading=18
        )

        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=6,
            leading=16
        )

        ejercicio_style = ParagraphStyle(
            'Ejercicio',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=13,
            alignment=TA_LEFT,
            spaceAfter=12,
            leading=18,
            textColor=colors.black
        )

        solucion_style = ParagraphStyle(
            'Solucion',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=11,
            alignment=TA_LEFT,
            textColor=colors.darkgreen,
            spaceAfter=15,
            leading=16,
            leftIndent=20
        )

        tipo_style = ParagraphStyle(
            'Tipo',
            parent=styles['Italic'],
            fontName='TimesNewRoman',
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.grey,
            spaceAfter=8
        )

        # Generar ejercicios combinados
        print(f"📝 Generando ejercicios combinados")
        print(f"   - Tipos: {tipos}")
        print(f"   - Dificultad: {dificultad}")
        print(f"   - Por tipo: {cantidad_por_tipo}")

        ejercicios = generador.generar_ejercicios(
            tipos, dificultad, cantidad_por_tipo)
        print(f"✅ {len(ejercicios)} ejercicios generados")

        flowables = []

        # Título
        tipos_nombres = {
            'integrales': 'Integrales',
            'derivadas': 'Derivadas',
            'limites': 'Límites',
            'fracciones': 'Fracciones Algebraicas',
            'funciones': 'Funciones',
            'extremos': 'Extremos (Máximos y Mínimos)',
            'asintotas': 'Asíntotas',
            'analisis': 'Análisis de Funciones'
        }
        tipos_str = ', '.join([tipos_nombres.get(t, t) for t in tipos])

        flowables.append(
            Paragraph(f"Hoja de Ejercicios Combinados", titulo_style))
        flowables.append(Paragraph(f"Tipos: {tipos_str}", subtitulo_style))
        flowables.append(Paragraph(
            f"Nivel: {dificultad.capitalize()}  |  {cantidad_por_tipo} ejercicios por tipo", normal_style))
        flowables.append(Spacer(1, 20))
        flowables.append(Paragraph("_"*80, normal_style))
        flowables.append(Spacer(1, 15))

        # Añadir ejercicios
        for i, ejercicio in enumerate(ejercicios, 1):
            try:
                flowables.append(
                    Paragraph(f"<b>Ejercicio {i}.</b>", ejercicio_style))

                if 'enunciado_img' in ejercicio and ejercicio['enunciado_img']:
                    enunciado_img = imagen_base64_a_reportlab(
                        ejercicio['enunciado_img'], ancho=420, alto=65)
                    if enunciado_img:
                        flowables.append(enunciado_img)
                    else:
                        flowables.append(
                            Paragraph(f"{ejercicio.get('enunciado', '')}", normal_style))
                else:
                    flowables.append(
                        Paragraph(f"{ejercicio.get('enunciado', '')}", normal_style))

                if 'tipo' in ejercicio and ejercicio['tipo']:
                    flowables.append(
                        Paragraph(f"<i>{ejercicio['tipo']}</i>", tipo_style))

                if mostrar_soluciones:
                    flowables.append(
                        Paragraph("<b>Solución:</b>", solucion_style))
                    if 'solucion_img' in ejercicio and ejercicio['solucion_img']:
                        solucion_img = imagen_base64_a_reportlab(
                            ejercicio['solucion_img'], ancho=320, alto=55)
                        if solucion_img:
                            flowables.append(solucion_img)
                        else:
                            flowables.append(
                                Paragraph(f"{ejercicio.get('solucion', '')}", normal_style))
                    else:
                        flowables.append(
                            Paragraph(f"{ejercicio.get('solucion', '')}", normal_style))
                else:
                    flowables.append(Spacer(1, 5))
                    flowables.append(
                        Paragraph("<i>Espacio para resolución:</i>", normal_style))
                    flowables.append(Spacer(1, 30))
                    flowables.append(Paragraph("."*60, normal_style))

                flowables.append(Spacer(1, 15))

                if i < len(ejercicios):
                    flowables.append(Paragraph("—"*70, normal_style))
                    flowables.append(Spacer(1, 15))

                if i % 4 == 0 and i < len(ejercicios):
                    flowables.append(PageBreak())

            except Exception as e:
                print(f"❌ Error en ejercicio {i}: {e}")
                flowables.append(
                    Paragraph(f"<b>Error en ejercicio {i}</b>", normal_style))
                flowables.append(Paragraph(str(e), normal_style))
                flowables.append(Spacer(1, 20))

        print("📄 Construyendo PDF...")
        doc.build(flowables)
        buffer.seek(0)
        print("✅ PDF generado correctamente")
        return buffer

    except Exception as e:
        print(f"❌ Error grave al generar PDF: {e}")
        traceback.print_exc()
        raise


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generar', methods=['POST'])
def generar_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        tipos = data.get('tipos', ['integrales'])
        dificultad = data.get('dificultad', 'media')
        cantidad_por_tipo = int(data.get('cantidad_por_tipo', 2))
        mostrar_soluciones = data.get('mostrar_soluciones', True)

        # Validar tipos
        tipos_validos = ['integrales', 'derivadas', 'limites',
                         'fracciones', 'funciones', 'extremos', 'asintotas', 'analisis']
        for t in tipos:
            if t not in tipos_validos:
                return jsonify({'error': f'Tipo no válido: {t}'}), 400

        print(f"\n🚀 Solicitud recibida:")
        print(f"   - Tipos: {tipos}")
        print(f"   - Dificultad: {dificultad}")
        print(f"   - Cantidad por tipo: {cantidad_por_tipo}")
        print(f"   - Mostrar soluciones: {mostrar_soluciones}")

        pdf_buffer = crear_pdf_ejercicios(
            tipos, dificultad, cantidad_por_tipo, mostrar_soluciones)

        tipos_str = '_'.join(tipos)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'ejercicios_combinados_{tipos_str}_{dificultad}.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"❌ Error en /api/generar: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/api/preview', methods=['POST'])
def previsualizar():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        tipos = data.get('tipos', ['integrales'])
        dificultad = data.get('dificultad', 'media')
        # Máximo 3 para preview
        cantidad_por_tipo = min(int(data.get('cantidad_por_tipo', 2)), 3)
        mostrar_soluciones = data.get('mostrar_soluciones', True)

        print(f"\n👁️ Preview solicitado:")
        print(f"   - Tipos: {tipos}")
        print(f"   - Dificultad: {dificultad}")
        print(f"   - Cantidad por tipo: {cantidad_por_tipo}")

        ejercicios = generador.generar_ejercicios(
            tipos, dificultad, cantidad_por_tipo)

        for ej in ejercicios:
            try:
                if 'enunciado_img' in ej and ej['enunciado_img']:
                    ej['enunciado_html'] = f'<img src="data:image/png;base64,{ej["enunciado_img"]}" style="max-width: 100%;">'
                else:
                    ej['enunciado_html'] = f'<b>Enunciado:</b> {ej.get("enunciado", "")}'

                if mostrar_soluciones:
                    if 'solucion_img' in ej and ej['solucion_img']:
                        ej['solucion_html'] = f'<img src="data:image/png;base64,{ej["solucion_img"]}" style="max-width: 100%;">'
                    else:
                        ej['solucion_html'] = f'<b>Solución:</b> {ej.get("solucion", "")}'
                else:
                    ej['solucion_html'] = '<i>🔒 Solución oculta (para practicar)</i>'

            except Exception as e:
                print(f"❌ Error al procesar imagen: {e}")
                ej['enunciado_html'] = f'<b>Error al renderizar:</b> {ej.get("enunciado", "")}'
                ej['solucion_html'] = f'<b>Error al renderizar:</b> {ej.get("solucion", "")}'

        return jsonify(ejercicios)

    except Exception as e:
        print(f"❌ Error en /api/preview: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📌 Accede a http://localhost:5000")
    app.run(debug=True, port=5000)
