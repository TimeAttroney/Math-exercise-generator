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
from generator import GeneradorEjercicios

app = Flask(__name__)
app.config['DEBUG'] = True

# Inicializar el generador
try:
    generador = GeneradorEjercicios()
    print("✅ Generator initialized successfully")
except Exception as e:
    print(f"❌ Error initializing generator: {e}")
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


def crear_pdf_ejercicios(tipos_seleccionados, mostrar_soluciones=True):
    """Generate a PDF with exercises from the selected subtypes"""
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

        enunciado_texto_style = ParagraphStyle(
            'EnunciadoTexto',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=5,
            leading=16,
            textColor=colors.black
        )

        # Generate exercises
        print(
            f"📝 Generating exercises for {len(tipos_seleccionados)} subtypes")
        ejercicios = generador.generar_ejercicios_por_subtipos(
            tipos_seleccionados)
        print(f"✅ {len(ejercicios)} exercises generated")

        flowables = []

        # Título
        flowables.append(Paragraph(f"Exercise Sheet", titulo_style))
        flowables.append(
            Paragraph(f"Total: {len(ejercicios)} exercises", normal_style))
        flowables.append(Spacer(1, 20))
        flowables.append(Paragraph("_"*80, normal_style))
        flowables.append(Spacer(1, 15))

        # Add exercises
        for i, ejercicio in enumerate(ejercicios, 1):
            try:
                flowables.append(
                    Paragraph(f"<b>Exercise {i}.</b>", ejercicio_style))

                if 'enunciado_texto' in ejercicio and ejercicio['enunciado_texto']:
                    flowables.append(
                        Paragraph(f"<i>{ejercicio['enunciado_texto']}</i>", enunciado_texto_style))

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
                        Paragraph(f"<i>Type: {ejercicio['tipo']}</i>", tipo_style))

                if mostrar_soluciones:
                    flowables.append(
                        Paragraph("<b>Solution:</b>", solucion_style))
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
                        Paragraph("<i>Space for solving:</i>", normal_style))
                    flowables.append(Spacer(1, 30))
                    flowables.append(Paragraph("."*60, normal_style))

                flowables.append(Spacer(1, 15))

                if i < len(ejercicios):
                    flowables.append(Paragraph("—"*70, normal_style))
                    flowables.append(Spacer(1, 15))

                if i % 4 == 0 and i < len(ejercicios):
                    flowables.append(PageBreak())

            except Exception as e:
                print(f"❌ Error in exercise {i}: {e}")
                flowables.append(
                    Paragraph(f"<b>Error in exercise {i}</b>", normal_style))
                flowables.append(Paragraph(str(e), normal_style))
                flowables.append(Spacer(1, 20))

        print("📄 Building PDF...")
        doc.build(flowables)
        buffer.seek(0)
        print("✅ PDF generated successfully")
        return buffer

    except Exception as e:
        print(f"❌ Serious error while generating PDF: {e}")
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

        tipos = data.get('tipos', [])
        mostrar_soluciones = data.get('mostrar_soluciones', True)

        if not tipos:
            return jsonify({'error': 'No se seleccionaron subtipos'}), 400

        print(f"\n🚀 PDF request received:")
        print(f"   - Subtypes: {len(tipos)}")
        print(f"   - Show solutions: {mostrar_soluciones}")

        pdf_buffer = crear_pdf_ejercicios(tipos, mostrar_soluciones)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'MEG_{len(tipos)}exercises.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"❌ Error in /api/generate: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/api/preview', methods=['POST'])
def previsualizar():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        tipos = data.get('tipos', [])
        mostrar_soluciones = data.get('mostrar_soluciones', True)

        if not tipos:
            return jsonify({'error': 'No se seleccionaron subtipos'}), 400

        print(f"\n👁️ Preview requested:")
        print(f"   - Subtypes: {len(tipos)}")

        ejercicios = generador.generar_ejercicios_por_subtipos(tipos)

        for ej in ejercicios:
            try:
                enunciado_html = ""
                if 'enunciado_texto' in ej and ej['enunciado_texto']:
                    enunciado_html += f"<div style='font-weight: bold; color: #1a1a2e; margin-bottom: 8px;'>{ej['enunciado_texto']}</div>"

                if 'enunciado_img' in ej and ej['enunciado_img']:
                    enunciado_html += f'<img src="data:image/png;base64,{ej["enunciado_img"]}" style="max-width: 100%;">'
                else:
                    enunciado_html += f'<div>{ej.get("enunciado", "")}</div>'

                ej['enunciado_html'] = enunciado_html

                if mostrar_soluciones:
                    if 'solucion_img' in ej and ej['solucion_img']:
                        ej['solucion_html'] = f'<img src="data:image/png;base64,{ej["solucion_img"]}" style="max-width: 100%;">'
                    else:
                        ej['solucion_html'] = f'<b>Solution:</b> {ej.get("solucion", "")}'
                else:
                    ej['solucion_html'] = '<i style="color:#94a3b8;">🔒 Solution hidden (for practice)</i>'

            except Exception as e:
                print(f"❌ Error processing image: {e}")
                ej['enunciado_html'] = f'<b>Error rendering:</b> {ej.get("enunciado", "")}'
                ej['solucion_html'] = f'<b>Error rendering:</b> {ej.get("solucion", "")}'

        return jsonify(ejercicios)

    except Exception as e:
        print(f"❌ Error in /api/preview: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📌 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
