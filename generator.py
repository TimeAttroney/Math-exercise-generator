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
            # Mapa de subtipos a funciones generadoras
            self.subtipos_map = {
                # ===== INTEGRALES =====
                'int_inmediata_potencia': self._integral_polinomica,
                'int_inmediata_log': self._integral_logaritmo,
                'int_inmediata_exp': self._integral_exponencial,
                'int_inmediata_trig': self._integral_trigonometrica,
                'int_inmediata_invtrig': self._integral_inversa_trig,
                'int_casi_potencia': self._integral_casi_potencia,
                'int_casi_log': self._integral_casi_log,
                'int_casi_exp': self._integral_casi_exp,
                'int_casi_trig': self._integral_casi_trig,
                'int_casi_invtrig': self._integral_casi_invtrig,
                'int_casi_logacot': self._integral_casi_logacot,
                'int_rac_simples': self._integral_rac_simples,
                'int_rac_multiples': self._integral_rac_multiples,
                'int_rac_grado2': self._integral_rac_grado2,
                'int_trig': self._integral_trig_especial,
                'int_partes': self._integral_por_partes,
                'int_cambio_fractrig': self._integral_cambio_fractrig,
                'int_cambio_irracional': self._integral_cambio_irracional,
                # ===== DERIVADAS =====
                'der_polinomica': self._derivada_polinomica,
                'der_trigonometrica': self._derivada_trigonometrica,
                'der_exponencial': self._derivada_exponencial,
                'der_logaritmica': self._derivada_logaritmica,
                'der_regla_cadena': self._derivada_regla_cadena,
                'der_implicita': self._derivada_implicita,
                # ===== LÍMITES =====
                'lim_infinito': self._limite_infinito,
                'lim_indeterminado': self._limite_indeterminado,
                'lim_trigonometrico': self._limite_trigonometrico,
                'lim_especial': self._limite_especial,
                # ===== FRACCIONES =====
                'frac_simplificar': self._fraccion_simplificar,
                'frac_sumar': self._fraccion_sumar,
                'frac_multiplicar': self._fraccion_multiplicar,
                'frac_division': self._fraccion_division,
                # ===== FUNCIONES =====
                'func_dominio': self._funcion_dominio,
                'func_recorrido': self._funcion_recorrido,
                'func_ceros': self._funcion_ceros,
                'func_crecimiento': self._funcion_crecimiento,
                # ===== EXTREMOS =====
                'ext_polinomico': self._extremo_polinomico,
                'ext_trigonometrico': self._extremo_trigonometrico,
                'ext_racional': self._extremo_racional,
                # ===== ASÍNTOTAS =====
                'asint_vertical': self._asintota_vertical,
                'asint_horizontal': self._asintota_horizontal,
                'asint_oblicua': self._asintota_oblicua,
                'asint_mixta': self._asintota_mixta,
                # ===== ANÁLISIS =====
                'anal_polinomico': self._analisis_polinomico,
                'anal_racional': self._analisis_racional,
                'anal_trigonometrico': self._analisis_trigonometrico
            }
            # Nombres descriptivos para cada subtipo
            self.subtipos_nombres = {
                'int_inmediata_potencia': 'Integral inmediata: Potencia',
                'int_inmediata_log': 'Integral inmediata: Logaritmo',
                'int_inmediata_exp': 'Integral inmediata: Exponencial',
                'int_inmediata_trig': 'Integral inmediata: Trigonométrica',
                'int_inmediata_invtrig': 'Integral inmediata: Inversa trigonométrica',
                'int_casi_potencia': 'Integral casi inmediata: Potencia',
                'int_casi_log': 'Integral casi inmediata: Logaritmo',
                'int_casi_exp': 'Integral casi inmediata: Exponencial',
                'int_casi_trig': 'Integral casi inmediata: Trigonométrica',
                'int_casi_invtrig': 'Integral casi inmediata: Inversa trigonométrica',
                'int_casi_logacot': 'Integral casi inmediata: Logaritmo + acotangente',
                'int_rac_simples': 'Integral racional: Raíces simples',
                'int_rac_multiples': 'Integral racional: Raíces múltiples',
                'int_rac_grado2': 'Integral racional: Factor grado 2',
                'int_trig': 'Integral trigonométrica especial',
                'int_partes': 'Integral por partes',
                'int_cambio_fractrig': 'Integral por cambio: Fracción trigonométrica',
                'int_cambio_irracional': 'Integral por cambio: Función irracional',
                'der_polinomica': 'Derivada polinómica',
                'der_trigonometrica': 'Derivada trigonométrica',
                'der_exponencial': 'Derivada exponencial',
                'der_logaritmica': 'Derivada logarítmica',
                'der_regla_cadena': 'Derivada: Regla de la cadena',
                'der_implicita': 'Derivada implícita',
                'lim_infinito': 'Límite al infinito',
                'lim_indeterminado': 'Límite con indeterminación',
                'lim_trigonometrico': 'Límite trigonométrico',
                'lim_especial': 'Límite especial (número e)',
                'frac_simplificar': 'Simplificar fracción',
                'frac_sumar': 'Suma de fracciones',
                'frac_multiplicar': 'Multiplicación de fracciones',
                'frac_division': 'División de fracciones',
                'func_dominio': 'Dominio de función',
                'func_recorrido': 'Recorrido de función',
                'func_ceros': 'Ceros de función',
                'func_crecimiento': 'Crecimiento de función',
                'ext_polinomico': 'Extremos: Polinómico',
                'ext_trigonometrico': 'Extremos: Trigonométrico',
                'ext_racional': 'Extremos: Racional',
                'asint_vertical': 'Asíntota vertical',
                'asint_horizontal': 'Asíntota horizontal',
                'asint_oblicua': 'Asíntota oblicua',
                'asint_mixta': 'Asíntotas múltiples',
                'anal_polinomico': 'Análisis: Polinómico',
                'anal_racional': 'Análisis: Racional',
                'anal_trigonometrico': 'Análisis: Trigonométrico'
            }
            print("✅ Generador inicializado con 48 subtipos de ejercicios")
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

    def generar_ejercicios_por_subtipos(self, tipos_seleccionados):
        """
        Genera ejercicios para una lista de subtipos con sus cantidades
        tipos_seleccionados: [{'id': 'int_inmediata_potencia', 'cantidad': 2}, ...]
        """
        try:
            ejercicios = []
            for item in tipos_seleccionados:
                subtipo_id = item['id']
                cantidad = item.get('cantidad', 1)

                if subtipo_id not in self.subtipos_map:
                    print(f"⚠️ Subtipo no reconocido: {subtipo_id}")
                    continue

                generador = self.subtipos_map[subtipo_id]
                nombre = self.subtipos_nombres.get(subtipo_id, subtipo_id)

                print(f"   - Generando {cantidad} de {nombre}")
                for i in range(cantidad):
                    try:
                        ejercicio = generador('media')
                        ejercicio['tipo'] = nombre
                        ejercicios.append(ejercicio)
                    except Exception as e:
                        print(f"      ❌ Error: {e}")
                        ejercicios.append(self._ejercicio_error(nombre))

            print(f"✅ {len(ejercicios)} ejercicios generados")
            return ejercicios

        except Exception as e:
            print(f"❌ Error en generar_ejercicios_por_subtipos: {e}")
            traceback.print_exc()
            raise

    # ============================================================
    # ===== FUNCIONES GENERADORAS DE EJERCICIOS =====
    # ============================================================

    # ---------- INTEGRALES INMEDIATAS ----------
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
            'enunciado_texto': 'Calcula la siguiente integral inmediata',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_logaritmo(self, dificultad):
        expr = 1/self.x
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral logarítmica',
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
            'enunciado_texto': 'Calcula la siguiente integral exponencial',
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
            'enunciado_texto': 'Calcula la siguiente integral trigonométrica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_inversa_trig(self, dificultad):
        expr = 1/(1 + self.x**2)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral (inversa trigonométrica)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- INTEGRALES CASI INMEDIATAS ----------
    def _integral_casi_potencia(self, dificultad):
        n = random.randint(1, 3)
        expr = (2*self.x + 1)**n
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (potencia)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_casi_log(self, dificultad):
        expr = 1/(2*self.x + 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (logaritmo)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_casi_exp(self, dificultad):
        expr = exp(2*self.x + 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (exponencial)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_casi_trig(self, dificultad):
        expr = sin(2*self.x + 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (trigonométrica)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_casi_invtrig(self, dificultad):
        expr = 1/(1 + (2*self.x)**2)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (inversa trigonométrica)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_casi_logacot(self, dificultad):
        expr = (2*self.x)/(1 + self.x**2)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral casi inmediata (logaritmo + acotangente)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- INTEGRALES RACIONALES ----------
    def _integral_rac_simples(self, dificultad):
        expr = 1/(self.x**2 - 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral racional (raíces simples)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_rac_multiples(self, dificultad):
        expr = 1/(self.x**3 - self.x)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral racional (raíces múltiples)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_rac_grado2(self, dificultad):
        expr = 1/(self.x**2 + 2*self.x + 2)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral racional (factor grado 2)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- OTRAS INTEGRALES ----------
    def _integral_trig_especial(self, dificultad):
        expr = sin(self.x)**2
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral trigonométrica especial',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_por_partes(self, dificultad):
        expr = self.x * exp(self.x)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral por partes',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_cambio_fractrig(self, dificultad):
        expr = 1/(sin(self.x) + cos(self.x))
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral por cambio de variable (fracción trigonométrica)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _integral_cambio_irracional(self, dificultad):
        expr = sqrt(self.x + 1)
        solucion = sp.integrate(expr, self.x)
        enunciado_latex = '\\int ' + sp.latex(expr) + ' \\, dx'
        solucion_latex = sp.latex(solucion) + ' + C'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la siguiente integral por cambio de variable (función irracional)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- DERIVADAS ----------
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
            'enunciado_texto': 'Deriva la siguiente función polinómica',
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
            'enunciado_texto': 'Deriva la siguiente función trigonométrica',
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
            'enunciado_texto': 'Deriva la siguiente función exponencial',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_logaritmica(self, dificultad):
        expr = log(self.x)
        solucion = sp.diff(expr, self.x)
        enunciado_latex = '\\frac{d}{dx}(' + sp.latex(expr) + ')'
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Deriva la siguiente función logarítmica',
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
            'enunciado_texto': 'Deriva usando la regla de la cadena',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _derivada_implicita(self, dificultad):
        expr = self.x**2 + self.y**2 - 4
        derivada = -sp.diff(expr, self.x) / sp.diff(expr, self.y)
        enunciado_latex = sp.latex(expr) + ' = 0'
        solucion_latex = sp.latex(derivada)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula la derivada implícita de la siguiente ecuación',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- LÍMITES ----------
    def _limite_infinito(self, dificultad):
        n = random.randint(1, 3)
        expr = (self.x**n + 1)/(2*self.x**n + 1)
        solucion = sp.limit(expr, self.x, oo)
        enunciado_latex = '\\lim_{x \\to \\infty} ' + sp.latex(expr)
        solucion_latex = sp.latex(solucion)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Calcula el siguiente límite al infinito',
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
            'enunciado_texto': 'Calcula el siguiente límite (indeterminación)',
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
            'enunciado_texto': 'Calcula el siguiente límite trigonométrico',
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
            'enunciado_texto': 'Calcula el siguiente límite especial (número e)',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- FRACCIONES ----------
    def _fraccion_simplificar(self, dificultad):
        n = random.randint(1, 4)
        expr = (self.x**n - 1)/(self.x - 1)
        simplificada = sp.simplify(expr)
        enunciado_latex = '\\frac{' + \
            sp.latex(self.x**n - 1) + '}{' + sp.latex(self.x - 1) + '}'
        solucion_latex = sp.latex(simplificada)
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Simplifica la siguiente fracción algebraica',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Suma las siguientes fracciones algebraicas',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Multiplica las siguientes fracciones algebraicas',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Divide las siguientes fracciones algebraicas',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- FUNCIONES ----------
    def _funcion_dominio(self, dificultad):
        expr = 1/(self.x**2 - 1)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'R \\setminus {-1, 1}',
            'enunciado_texto': 'Encuentra el dominio de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('R \\setminus {-1, 1}')
        }

    def _funcion_recorrido(self, dificultad):
        expr = self.x**2 + 1
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': '[1, \\infty)',
            'enunciado_texto': 'Determina el recorrido de la siguiente función',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Encuentra los ceros (raíces) de la siguiente función',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Estudia el crecimiento de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- EXTREMOS ----------
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Encuentra los máximos y mínimos relativos de la siguiente función polinómica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _extremo_trigonometrico(self, dificultad):
        expr = sin(self.x) + cos(self.x)
        enunciado_latex = sp.latex(expr)
        solucion_latex = 'Máximos en x = π/4 + 2kπ, Mínimos en x = 5π/4 + 2kπ'
        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Determina los extremos relativos de la siguiente función trigonométrica',
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
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Halla los extremos relativos de la siguiente función racional',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    # ---------- ASÍNTOTAS ----------
    def _asintota_vertical(self, dificultad):
        expr = 1/(self.x - 2)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'x = 2',
            'enunciado_texto': 'Encuentra la asíntota vertical de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('x = 2')
        }

    def _asintota_horizontal(self, dificultad):
        expr = (2*self.x + 1)/(self.x + 1)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'y = 2',
            'enunciado_texto': 'Encuentra la asíntota horizontal de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('y = 2')
        }

    def _asintota_oblicua(self, dificultad):
        expr = (self.x**2 + 1)/(self.x)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'y = x',
            'enunciado_texto': 'Encuentra la asíntota oblicua de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('y = x')
        }

    def _asintota_mixta(self, dificultad):
        expr = (self.x**2 - 1)/(self.x**2 - 4)
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'Verticales: x = ±2, Horizontal: y = 1',
            'enunciado_texto': 'Encuentra todas las asíntotas de la siguiente función',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('Verticales: x = ±2, Horizontal: y = 1')
        }

    # ---------- ANÁLISIS ----------
    def _analisis_polinomico(self, dificultad):
        expr = self.x**3 - 3*self.x
        derivada = sp.diff(expr, self.x)
        derivada2 = sp.diff(derivada, self.x)
        puntos_criticos = sp.solve(derivada, self.x)
        puntos_inflexion = sp.solve(derivada2, self.x)

        enunciado_latex = sp.latex(expr)
        extremos_str = ', '.join([sp.latex(p) for p in puntos_criticos])
        inflexion_str = ', '.join([sp.latex(p) for p in puntos_inflexion])
        solucion_latex = 'Extremos: ' + extremos_str + ', Inflexión: ' + inflexion_str

        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Realiza el análisis completo de la siguiente función polinómica',
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
        solucion_latex = 'Dominio: R \ {±2}, Extremos: ' + extremos_str

        return {
            'enunciado': enunciado_latex,
            'solucion': solucion_latex,
            'enunciado_texto': 'Realiza el análisis completo de la siguiente función racional',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion(solucion_latex)
        }

    def _analisis_trigonometrico(self, dificultad):
        expr = sin(self.x) + 1
        enunciado_latex = sp.latex(expr)
        return {
            'enunciado': enunciado_latex,
            'solucion': 'Dominio: R, Recorrido: [0, 2], Período: 2π',
            'enunciado_texto': 'Realiza el análisis completo de la siguiente función trigonométrica',
            'enunciado_img': self.renderizar_expresion(enunciado_latex),
            'solucion_img': self.renderizar_expresion('Dominio: R, Recorrido: [0, 2], Período: 2π')
        }

    # ===== MÉTODO DE ERROR =====
    def _ejercicio_error(self, tipo):
        return {
            'enunciado': f'Error al generar {tipo}',
            'solucion': 'Error',
            'tipo': f'{tipo} (error)',
            'enunciado_texto': f'Error al generar {tipo}',
            'enunciado_img': None,
            'solucion_img': None
        }
