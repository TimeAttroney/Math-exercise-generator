# MEG - Math Exercise Generator

MEG is a web application built with Python and Flask that generates customized math exercise sheets and exports them as PDF files. The app combines an interactive interface with a math exercise generation engine that produces statements, solutions, and visual representations for different types of content.

## What the application does

The application allows you to:

- Select exercise categories and subtypes from a web interface.
- Define how many exercises to generate per subtype.
- Show or hide solutions in the PDF.
- Generate a preview of the exercises before downloading them.
- Export the result as a PDF ready to print or share.

## Main features

- Automatic generation of exercises for:
  - Integrals
  - Derivatives
  - Limits
  - Fractions
  - Functions
  - Extrema
  - Asymptotes
  - Function analysis
- Visual rendering of mathematical expressions using images.
- Professional PDF generation with ReportLab.
- REST API for generating PDFs and previews.

## Project structure

- app.py: Flask server, app routes, and PDF generation.
- generador.py: math exercise generation logic.
- templates/index.html: web interface for the generator.
- requirements.txt: project dependencies.
- init.bat: startup script for Windows.

## Requirements

- Python 3.8 or higher
- Dependencies listed in requirements.txt

## Installation

1. Clone or download this repository.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

1. Run the application:

```bash
python app.py
```

1. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Usage

1. In the interface, select one or more exercise categories.
2. Adjust the number of exercises per subtype.
3. Enable or disable the option to show solutions.
4. Click "Generate" to download the PDF or "Preview" to see a preview.

## Technologies used

- Flask
- ReportLab
- SymPy
- Matplotlib

## Notes

The app is designed to automatically generate math exercises in a practical format for teachers or students who need study material in PDF format.
