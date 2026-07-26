import traceback
import base64
import io
import matplotlib.pyplot as plt
import random
import sympy as sp
from sympy import symbols, Integral, Derivative, Limit, sin, cos, tan, exp, log, sqrt, Rational, pi, oo, solve
import matplotlib
matplotlib.use('Agg')

# ===== CONFIGURACIÓN =====
print("📐 Usando renderizado sin LaTeX (Times New Roman)")
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman',
                              'DejaVu Serif', 'Computer Modern Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['mathtext.default'] = 'regular'


class GeneradorEjercicios:
    def __init__(self):
        try:
            self.x = symbols('x')
            self.y = symbols('y')
            self.tipos_disponibles = {
                'integrales': self.generar_integral,
                'derivadas': self.generar_derivada,
                'limites': self.generar_limite,
                'fracciones': self.generar_fraccion,
                'funciones': self.generar_funcion,
                'extremos': self.generar_extremos,
                'asintotas': self.generar_asintotas,
                'analisis': self.generar_analisis
            }
            print("✅ Generador inicializado con 8 tipos de ejercicios")
        except Exception as e:
            print(f"❌ Error al inicializar: {e}")
            raise

    def renderizar_expresion(self, expresion_latex, tamaño=16):
        """Convierte una expresión LaTeX a una imagen PNG en base64"""
        try:
            if not expresion_latex:
                return None

            fig, ax = plt.subplots(figsize=(7, 1.2))
            ax.axis('off')
            ax.text(0.5, 0.5, f'${expresion_latex}$',
                    fontsize=tamaño, ha='center', va='center')

            plt.tight_layout(pad=0.1)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                        pad_inches=0.05, facecolor='white')
            plt.close(fig)
            buf.seek(0)
            return base64.b64encode(buf.read()).decode('utf-8')
        except Exception as e:
            print(f"❌ Error al renderizar: {e}")
            return None

    # ========== TIPOS DE EJERCICIOS ==========

    def generar_integral(self, dificultad='media'):
        try:
            tipos = [
                self._integral_polinomica,
                self._integral_trigonometrica,
                self._integral_exponencial,
                self._integral_racional
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en integral: {e}")
            return self._ejercicio_error('Integral')

    def generar_derivada(self, dificultad='media'):
        try:
            tipos = [
                self._derivada_polinomica,
                self._derivada_trigonometrica,
                self._derivada_exponencial,
                self._derivada_regla_cadena,
                self._derivada_implicita
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en derivada: {e}")
            return self._ejercicio_error('Derivada')

    def generar_limite(self, dificultad='media'):
        try:
            tipos = [
                self._limite_infinito,
                self._limite_indeterminado,
                self._limite_trigonometrico,
                self._limite_especial
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en límite: {e}")
            return self._ejercicio_error('Límite')

    def generar_fraccion(self, dificultad='media'):
        try:
            tipos = [
                self._fraccion_simplificar,
                self._fraccion_sumar,
                self._fraccion_multiplicar,
                self._fraccion_division
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en fracción: {e}")
            return self._ejercicio_error('Fracción')

    def generar_funcion(self, dificultad='media'):
        try:
            tipos = [
                self._funcion_dominio,
                self._funcion_recorrido,
                self._funcion_ceros,
                self._funcion_crecimiento
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en función: {e}")
            return self._ejercicio_error('Función')

    def generar_extremos(self, dificultad='media'):
        try:
            tipos = [
                self._extremo_polinomico,
                self._extremo_trigonometrico,
                self._extremo_racional
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en extremos: {e}")
            return self._ejercicio_error('Extremos')

    def generar_asintotas(self, dificultad='media'):
        try:
            tipos = [
                self._asintota_vertical,
                self._asintota_horizontal,
                self._asintota_oblicua,
                self._asintota_mixta
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en asíntotas: {e}")
            return self._ejercicio_error('Asíntotas')

    def generar_analisis(self, dificultad='media'):
        try:
            tipos = [
                self._analisis_polinomico,
                self._analisis_racional,
                self._analisis_trigonometrico
            ]
            return random.choice(tipos)(dificultad)
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            return self._ejercicio_error('Análisis')

    # ========== INTEGRALES ==========

    def _integral_polinomica(self, dificultad):
        n = random.randint(
            1, 5) if dificultad == 'facil' else random.randint(2, 8)
        if dificultad == 'dificil':
            n = random.randint(3, 10)
        coeficiente = random.randint(1, 5)
        expr = coeficiente * self.x**n
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Integral polinómica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_trigonometrica(self, dificultad):
        funcs = [sin, cos, tan]
        func = random.choice(funcs)
        expr = func(self.x)
        if dificultad == 'dificil':
            expr = func(2*self.x) * random.choice([sin, cos])(self.x)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Integral trigonométrica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_exponencial(self, dificultad):
        if dificultad == 'facil':
            expr = exp(self.x)
        else:
            base = random.randint(2, 5)
            expr = base**self.x
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Integral exponencial',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_racional(self, dificultad):
        if dificultad == 'facil':
            expr = 1/self.x
        else:
            expr = 1/(self.x**2 + 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Integral racional',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== DERIVADAS ==========

    def _derivada_polinomica(self, dificultad):
        n = random.randint(
            1, 4) if dificultad == 'facil' else random.randint(2, 6)
        coeficiente = random.randint(1, 5)
        expr = coeficiente * self.x**n
        solucion = sp.diff(expr, self.x)
        enunciado_latex = '\\frac{d}{dx}(' + sp.latex(expr) + ')'
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Derivada polinómica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_trigonometrica(self, dificultad):
        funcs = [sin, cos, tan]
        func = random.choice(funcs)
        expr = func(self.x)
        if dificultad == 'dificil':
            expr = func(2*self.x + 1)
        solucion = sp.diff(expr, self.x)
        enunciado_latex = '\\frac{d}{dx}(' + sp.latex(expr) + ')'
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Derivada trigonométrica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_exponencial(self, dificultad):
        if dificultad == 'facil':
            expr = exp(self.x)
        else:
            expr = exp(2*self.x + 1)
        solucion = sp.diff(expr, self.x)
        enunciado_latex = '\\frac{d}{dx}(' + sp.latex(expr) + ')'
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Derivada exponencial',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_regla_cadena(self, dificultad):
        if dificultad == 'facil':
            expr = sin(self.x**2)
        else:
            expr = sin(exp(2*self.x))
        solucion = sp.diff(expr, self.x)
        enunciado_latex = '\\frac{d}{dx}(' + sp.latex(expr) + ')'
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Regla de la cadena',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_implicita(self, dificultad):
        expr = self.x**2 + self.y**2 - 4
        derivada = -sp.diff(expr, self.x) / sp.diff(expr, self.y)
        enunciado_latex = sp.latex(expr) + ' = 0'
        solucion_latex = sp.latex(derivada)
        return {
            'enunciado': 'Deriva implícitamente: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Derivada implícita',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== LÍMITES ==========

    def _limite_infinito(self, dificultad):
        n = random.randint(1, 3)
        expr = (self.x**n + 1)/(2*self.x**n + 1)
        solucion = sp.limit(expr, self.x, oo)
        enunciado_latex = '\\lim_{x \\to \\infty} ' + sp.latex(expr)
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Límite al infinito',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _limite_indeterminado(self, dificultad):
        a = random.randint(0, 3)
        if dificultad == 'facil':
            expr = (self.x**2 - 1)/(self.x - 1)
        else:
            expr = (self.x**3 - 1)/(self.x - 1)
        solucion = sp.limit(expr, self.x, a+1)
        enunciado_latex = '\\lim_{x \\to ' + str(a+1) + '} ' + sp.latex(expr)
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Límite indeterminado',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _limite_trigonometrico(self, dificultad):
        expr = sin(self.x)/self.x
        solucion = sp.limit(expr, self.x, 0)
        enunciado_latex = '\\lim_{x \\to 0} ' + sp.latex(expr)
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Límite trigonométrico',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _limite_especial(self, dificultad):
        expr = (1 + 1/self.x)**self.x
        solucion = sp.limit(expr, self.x, oo)
        enunciado_latex = '\\lim_{x \\to \\infty} ' + sp.latex(expr)
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Límite especial (e)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== FRACCIONES ==========

    def _fraccion_simplificar(self, dificultad):
        n = random.randint(1, 4)
        expr = (self.x**n - 1)/(self.x - 1)
        simplificada = sp.simplify(expr)
        enunciado_latex = '\\frac{' + \
            sp.latex(self.x**n - 1) + '}{' + sp.latex(self.x - 1) + '}'
        solucion_latex = sp.latex(simplificada)
        return {
            'enunciado': 'Simplifica: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Simplificar fracción',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _fraccion_sumar(self, dificultad):
        a, b = random.randint(1, 3), random.randint(1, 3)
        expr = a/(self.x + 1) + b/(self.x - 1)
        suma = sp.simplify(expr)
        enunciado_latex = sp.latex(a/(self.x+1)) + \
            ' + ' + sp.latex(b/(self.x-1))
        solucion_latex = sp.latex(suma)
        return {
            'enunciado': 'Calcula: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Suma de fracciones',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _fraccion_multiplicar(self, dificultad):
        a = random.randint(1, 3)
        expr = (a/(self.x+1)) * ((self.x-1)/(self.x+2))
        producto = sp.simplify(expr)
        enunciado_latex = sp.latex(a/(self.x+1)) + \
            ' \\cdot ' + sp.latex((self.x-1)/(self.x+2))
        solucion_latex = sp.latex(producto)
        return {
            'enunciado': 'Multiplica: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Multiplicación de fracciones',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _fraccion_division(self, dificultad):
        a = random.randint(1, 3)
        expr = (a/(self.x+1)) / ((self.x-1)/(self.x+2))
        division = sp.simplify(expr)
        enunciado_latex = sp.latex(a/(self.x+1)) + \
            ' \\div ' + sp.latex((self.x-1)/(self.x+2))
        solucion_latex = sp.latex(division)
        return {
            'enunciado': 'Divide: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'División de fracciones',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== FUNCIONES ==========

    def _funcion_dominio(self, dificultad):
        expr = 1/(self.x**2 - 1)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra el dominio de: ' + enunciado_latex,
            'solucion': 'R \\setminus {-1, 1}',
            'tipo': 'Dominio de función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('R \\setminus {-1, 1}')
        }

    def _funcion_recorrido(self, dificultad):
        expr = self.x**2 + 1
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra el recorrido de: ' + enunciado_latex,
            'solucion': '[1, \\infty)',
            'tipo': 'Recorrido de función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('[1, \\infty)')
        }

    def _funcion_ceros(self, dificultad):
        a, b, c = random.randint(
            1, 5), random.randint(-5, 5), random.randint(-5, 5)
        expr = a*self.x**2 + b*self.x + c
        raices = sp.solve(expr, self.x)
        enunciado_latex = sp.latex(expr)
        solucion_latex = ', '.join([sp.latex(r) for r in raices])
        return {
            'enunciado': 'Encuentra los ceros de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Ceros de función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _funcion_crecimiento(self, dificultad):
        expr = self.x**3 - 3*self.x
        derivada = sp.diff(expr, self.x)
        puntos = sp.solve(derivada, self.x)
        enunciado_latex = sp.latex(expr)
        solucion_latex = 'Crece en (-∞, ' + sp.latex(
            puntos[0]) + ') y (' + sp.latex(puntos[1]) + ', ∞)'
        return {
            'enunciado': 'Estudia el crecimiento de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Crecimiento de función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== EXTREMOS ==========

    def _extremo_polinomico(self, dificultad):
        n = random.randint(2, 3)
        expr = self.x**n - n*self.x
        derivada = sp.diff(expr, self.x)
        puntos = sp.solve(derivada, self.x)

        extremos = []
        for p in puntos:
            valor = expr.subs(self.x, p)
            extremos.append('(' + sp.latex(p) + ', ' + sp.latex(valor) + ')')

        enunciado_latex = sp.latex(expr)
        solucion_latex = ', '.join(extremos)
        return {
            'enunciado': 'Encuentra los extremos de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Extremos (polinómico)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _extremo_trigonometrico(self, dificultad):
        expr = sin(self.x) + cos(self.x)
        enunciado_latex = sp.latex(expr)
        solucion_latex = 'Maximo: x = pi/4 + 2kpi, Minimo: x = 5pi/4 + 2kpi'
        return {
            'enunciado': 'Encuentra los extremos de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Extremos (trigonométrico)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _extremo_racional(self, dificultad):
        expr = (self.x**2 + 1)/(self.x)
        derivada = sp.diff(expr, self.x)
        puntos = sp.solve(derivada, self.x)

        extremos = []
        for p in puntos:
            if p.is_real:
                valor = expr.subs(self.x, p)
                extremos.append(
                    '(' + sp.latex(p) + ', ' + sp.latex(valor) + ')')

        enunciado_latex = sp.latex(expr)
        solucion_latex = ', '.join(
            extremos) if extremos else 'No tiene extremos reales'
        return {
            'enunciado': 'Encuentra los extremos de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Extremos (racional)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ========== ASÍNTOTAS ==========

    def _asintota_vertical(self, dificultad):
        expr = 1/(self.x - 2)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra la asíntota vertical de: ' + enunciado_latex,
            'solucion': 'x = 2',
            'tipo': 'Asíntota vertical',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('x = 2')
        }

    def _asintota_horizontal(self, dificultad):
        expr = (2*self.x + 1)/(self.x + 1)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra la asíntota horizontal de: ' + enunciado_latex,
            'solucion': 'y = 2',
            'tipo': 'Asíntota horizontal',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('y = 2')
        }

    def _asintota_oblicua(self, dificultad):
        expr = (self.x**2 + 1)/(self.x)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra la asíntota oblicua de: ' + enunciado_latex,
            'solucion': 'y = x',
            'tipo': 'Asíntota oblicua',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('y = x')
        }

    def _asintota_mixta(self, dificultad):
        expr = (self.x**2 - 1)/(self.x**2 - 4)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Encuentra las asíntotas de: ' + enunciado_latex,
            'solucion': 'Verticales: x = +-2, Horizontal: y = 1',
            'tipo': 'Asíntotas (múltiples)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('Verticales: x = +-2, Horizontal: y = 1')
        }

    # ========== ANÁLISIS ==========

    def _analisis_polinomico(self, dificultad):
        expr = self.x**3 - 3*self.x
        derivada = sp.diff(expr, self.x)
        derivada2 = sp.diff(derivada, self.x)
        puntos_criticos = sp.solve(derivada, self.x)
        puntos_inflexion = sp.solve(derivada2, self.x)

        enunciado_latex = sp.latex(expr)
        extremos_str = ', '.join([sp.latex(p) for p in puntos_criticos])
        inflexion_str = ', '.join([sp.latex(p) for p in puntos_inflexion])
        solucion_latex = 'Extremos: ' + extremos_str + ', Inflexion: ' + inflexion_str

        return {
            'enunciado': 'Realiza el análisis completo de: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Análisis completo (polinómico)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _analisis_racional(self, dificultad):
        expr = (self.x**2 - 1)/(self.x**2 - 4)
        derivada = sp.diff(expr, self.x)
        puntos_criticos = sp.solve(derivada, self.x)

        enunciado_latex = sp.latex(expr)
        extremos_str = ', '.join([sp.latex(
            p) for p in puntos_criticos if p.is_real]) if puntos_criticos else 'No tiene'
        solucion_latex = 'Dominio: R \ {+-2}, Extremos: ' + extremos_str

        return {
            'enunciado': 'Analiza la función: ' + enunciado_latex,
            'solucion': solucion_latex,
            'tipo': 'Análisis (racional)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _analisis_trigonometrico(self, dificultad):
        expr = sin(self.x) + 1
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': 'Analiza la función: ' + enunciado_latex,
            'solucion': 'Dominio: R, Recorrido: [0, 2], Periodo: 2pi',
            'tipo': 'Análisis (trigonométrico)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('Dominio: R, Recorrido: [0, 2], Periodo: 2pi')
        }

    # ========== MÉTODOS AUXILIARES ==========

    def _ejercicio_error(self, tipo):
        return {
            'enunciado': 'Error al generar ' + tipo,
            'solucion': 'Error',
            'tipo': tipo + ' (error)',
            'enunciado_img': None,
            'solucion_img': None
        }

    # ========== MÉTODO PRINCIPAL ==========

    def generar_ejercicios(self, tipos_seleccionados, dificultad='media', cantidad_por_tipo=2):
        """
        Genera ejercicios de múltiples tipos combinados

        Args:
            tipos_seleccionados: Lista de tipos ('integrales', 'derivadas', etc.)
            dificultad: 'facil', 'media', 'dificil'
            cantidad_por_tipo: Número de ejercicios por tipo seleccionado
        """
        try:
            ejercicios = []

            if isinstance(tipos_seleccionados, str):
                tipos_seleccionados = [tipos_seleccionados]

            print(f"\n📝 Generando ejercicios combinados:")
            print(f"   - Tipos: {', '.join(tipos_seleccionados)}")
            print(f"   - Dificultad: {dificultad}")
            print(f"   - Por tipo: {cantidad_por_tipo}")

            for tipo in tipos_seleccionados:
                if tipo in self.tipos_disponibles:
                    generador = self.tipos_disponibles[tipo]
                    print(f"   - Generando {cantidad_por_tipo} de {tipo}...")

                    for i in range(cantidad_por_tipo):
                        try:
                            ejercicio = generador(dificultad)
                            ejercicios.append(ejercicio)
                        except Exception as e:
                            print(f"      ❌ Error en ejercicio {i+1}: {e}")
                            ejercicios.append(self._ejercicio_error(tipo))
                else:
                    print(f"   ⚠️ Tipo no reconocido: {tipo}")

            print(f"✅ {len(ejercicios)} ejercicios generados")
            return ejercicios

        except Exception as e:
            print(f"❌ Error en generar_ejercicios: {e}")
            traceback.print_exc()
            raise
