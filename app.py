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
from generator import ExerciseGenerator

app = Flask(__name__, template_folder=os.path.dirname(__file__))
app.config['DEBUG'] = True

# Initialize the generator
try:
    generator = ExerciseGenerator()
    print("✅ Generator initialized successfully")
except Exception as e:
    print(f"❌ Error initializing generator: {e}")
    sys.exit(1)

# Register fonts for PDF


def register_fonts():
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

        font_registered = False
        for path in font_paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont('TimesNewRoman', path))
                    font_registered = True
                    print(f"✅ Times New Roman font registered from: {path}")
                    break
                except Exception:
                    continue

        if not font_registered:
            print("⚠️ Times New Roman not found, using the default font")
    except Exception as e:
        print(f"❌ Error registering fonts: {e}")


register_fonts()


def image_base64_to_reportlab(image_base64, width=400, height=60):
    try:
        if not image_base64:
            return None
        image_bytes = base64.b64decode(image_base64)
        buffer = io.BytesIO(image_bytes)
        img = Image(buffer, width=width, height=height)
        return img
    except Exception as e:
        print(f"❌ Error converting image: {e}")
        return None


def create_exercise_pdf(selected_types, show_solutions=True):
    """Generate a PDF with exercises from the selected subtypes"""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'Title',
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

        exercise_style = ParagraphStyle(
            'Exercise',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=13,
            alignment=TA_LEFT,
            spaceAfter=12,
            leading=18,
            textColor=colors.black
        )

        solution_style = ParagraphStyle(
            'Solution',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=11,
            alignment=TA_LEFT,
            textColor=colors.darkgreen,
            spaceAfter=15,
            leading=16,
            leftIndent=20
        )

        type_style = ParagraphStyle(
            'Type',
            parent=styles['Italic'],
            fontName='TimesNewRoman',
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.grey,
            spaceAfter=8
        )

        statement_text_style = ParagraphStyle(
            'StatementText',
            parent=styles['Normal'],
            fontName='TimesNewRoman',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=5,
            leading=16,
            textColor=colors.black
        )

        print(f"📝 Generating exercises for {len(selected_types)} subtypes")
        exercises = generator.generate_exercises_by_subtypes(selected_types)
        print(f"✅ {len(exercises)} exercises generated")

        flowables = []

        flowables.append(Paragraph("Exercise Sheet", title_style))
        flowables.append(
            Paragraph(f"Total: {len(exercises)} exercises", normal_style))
        flowables.append(Spacer(1, 20))
        flowables.append(Paragraph("_" * 80, normal_style))
        flowables.append(Spacer(1, 15))

        for i, exercise in enumerate(exercises, 1):
            try:
                flowables.append(
                    Paragraph(f"<b>Exercise {i}.</b>", exercise_style))

                if 'statement_text' in exercise and exercise['statement_text']:
                    flowables.append(
                        Paragraph(f"<i>{exercise['statement_text']}</i>", statement_text_style))

                if 'statement_img' in exercise and exercise['statement_img']:
                    statement_img = image_base64_to_reportlab(
                        exercise['statement_img'], width=420, height=65)
                    if statement_img:
                        flowables.append(statement_img)
                    else:
                        flowables.append(
                            Paragraph(f"{exercise.get('statement', '')}", normal_style))
                else:
                    flowables.append(
                        Paragraph(f"{exercise.get('statement', '')}", normal_style))

                if 'type' in exercise and exercise['type']:
                    flowables.append(
                        Paragraph(f"<i>Type: {exercise['type']}</i>", type_style))

                if show_solutions:
                    flowables.append(
                        Paragraph("<b>Solution:</b>", solution_style))
                    if 'solution_img' in exercise and exercise['solution_img']:
                        solution_img = image_base64_to_reportlab(
                            exercise['solution_img'], width=320, height=55)
                        if solution_img:
                            flowables.append(solution_img)
                        else:
                            flowables.append(
                                Paragraph(f"{exercise.get('solution', '')}", normal_style))
                    else:
                        flowables.append(
                            Paragraph(f"{exercise.get('solution', '')}", normal_style))
                else:
                    flowables.append(Spacer(1, 5))
                    flowables.append(
                        Paragraph("<i>Space for solving:</i>", normal_style))
                    flowables.append(Spacer(1, 30))
                    flowables.append(Paragraph("." * 60, normal_style))

                flowables.append(Spacer(1, 15))

                if i < len(exercises):
                    flowables.append(Paragraph("—" * 70, normal_style))
                    flowables.append(Spacer(1, 15))

                if i % 4 == 0 and i < len(exercises):
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
    return render_template('index_meg.html')


@app.route('/api/generate', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        selected_types = data.get('types', [])
        show_solutions = data.get('show_solutions', True)

        if not selected_types:
            return jsonify({'error': 'No subtypes selected'}), 400

        print(f"\n🚀 PDF request received:")
        print(f"   - Subtypes: {len(selected_types)}")
        print(f"   - Show solutions: {show_solutions}")

        pdf_buffer = create_exercise_pdf(selected_types, show_solutions)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'MEG_{len(selected_types)}exercises.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"❌ Error in /api/generate: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/api/preview', methods=['POST'])
def preview():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        selected_types = data.get('types', [])
        show_solutions = data.get('show_solutions', True)

        if not selected_types:
            return jsonify({'error': 'No subtypes selected'}), 400

        print(f"\n👁️ Preview requested:")
        print(f"   - Subtypes: {len(selected_types)}")

        exercises = generator.generate_exercises_by_subtypes(selected_types)

        for exercise in exercises:
            try:
                statement_html = ""
                if 'statement_text' in exercise and exercise['statement_text']:
                    statement_html += f"<div style='font-weight: bold; color: #1a1a2e; margin-bottom: 8px;'>{exercise['statement_text']}</div>"

                if 'statement_img' in exercise and exercise['statement_img']:
                    statement_html += f'<img src="data:image/png;base64,{exercise["statement_img"]}" style="max-width: 100%;">'
                else:
                    statement_html += f'<div>{exercise.get("statement", "")}</div>'

                exercise['statement_html'] = statement_html

                if show_solutions:
                    if 'solution_img' in exercise and exercise['solution_img']:
                        exercise['solution_html'] = f'<img src="data:image/png;base64,{exercise["solution_img"]}" style="max-width: 100%;">'
                    else:
                        exercise['solution_html'] = f'<b>Solution:</b> {exercise.get("solution", "")}'
                else:
                    exercise[
                        'solution_html'] = '<i style="color:#94a3b8;">🔒 Solution hidden (for practice)</i>'

            except Exception as e:
                print(f"❌ Error processing image: {e}")
                exercise['statement_html'] = f'<b>Error rendering:</b> {exercise.get("statement", "")}'
                exercise['solution_html'] = f'<b>Error rendering:</b> {exercise.get("solution", "")}'

        return jsonify(exercises)

    except Exception as e:
        print(f"❌ Error in /api/preview: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📌 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
