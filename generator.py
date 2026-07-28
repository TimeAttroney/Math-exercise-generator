from sympy import Rational, symbols, sin, cos, tan, exp, log, sqrt, oo
import sympy as sp
import matplotlib.pyplot as plt
import base64
import io
import random
import matplotlib
matplotlib.use('Agg')

# ===== FONT CONFIGURATION =====
# Use Times New Roman / STIX font for math rendering
matplotlib.rcParams['mathtext.fontset'] = 'stix'  # STIX is Times-like
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = [
    'Times New Roman', 'DejaVu Serif', 'Computer Modern Roman']


class ExerciseGenerator:
    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.subtypes_map = {
            'int_inmediata_potencia': self._integral_polynomial,
            'int_inmediata_log': self._integral_logarithm,
            'int_inmediata_exp': self._integral_exponential,
            'int_inmediata_trig': self._integral_trigonometric,
            'int_inmediata_invtrig': self._integral_inverse_trig,
            'int_casi_potencia': self._integral_almost_power,
            'int_casi_log': self._integral_almost_log,
            'int_casi_exp': self._integral_almost_exp,
            'int_casi_trig': self._integral_almost_trig,
            'int_casi_invtrig': self._integral_almost_invtrig,
            'int_casi_logacot': self._integral_almost_logacot,
            'int_rac_simples': self._integral_rational_simple,
            'int_rac_multiples': self._integral_rational_multiple,
            'int_rac_grado2': self._integral_rational_degree2,
            'int_trig': self._integral_trig_special,
            'int_partes': self._integral_by_parts,
            'int_cambio_fractrig': self._integral_change_fraction_trig,
            'int_cambio_irracional': self._integral_change_irrational,
            'der_polinomica': self._derivative_polynomial,
            'der_trigonometrica': self._derivative_trigonometric,
            'der_exponencial': self._derivative_exponential,
            'der_logaritmica': self._derivative_logarithmic,
            'der_regla_cadena': self._derivative_chain_rule,
            'der_implicita': self._derivative_implicit,
            'lim_infinito': self._limit_infinity,
            'lim_indeterminado': self._limit_indeterminate,
            'lim_trigonometrico': self._limit_trigonometric,
            'lim_especial': self._limit_special,
            'frac_simplificar': self._fraction_simplify,
            'frac_sumar': self._fraction_add,
            'frac_multiplicar': self._fraction_multiply,
            'frac_division': self._fraction_divide,
            'func_dominio': self._function_domain,
            'func_recorrido': self._function_range,
            'func_ceros': self._function_zeros,
            'func_crecimiento': self._function_growth,
            'ext_polinomico': self._extreme_polynomial,
            'ext_trigonometrico': self._extreme_trigonometric,
            'ext_racional': self._extreme_rational,
            'asint_vertical': self._asymptote_vertical,
            'asint_horizontal': self._asymptote_horizontal,
            'asint_oblicua': self._asymptote_oblique,
            'asint_mixta': self._asymptote_mixed,
            'anal_polinomico': self._analysis_polynomial,
            'anal_racional': self._analysis_rational,
            'anal_trigonometrico': self._analysis_trigonometric,
        }
        self.subtypes_names = {
            'int_inmediata_potencia': 'Immediate integral: power',
            'int_inmediata_log': 'Immediate integral: logarithm',
            'int_inmediata_exp': 'Immediate integral: exponential',
            'int_inmediata_trig': 'Immediate integral: trigonometric',
            'int_inmediata_invtrig': 'Immediate integral: inverse trigonometric',
            'int_casi_potencia': 'Almost immediate integral: power',
            'int_casi_log': 'Almost immediate integral: logarithm',
            'int_casi_exp': 'Almost immediate integral: exponential',
            'int_casi_trig': 'Almost immediate integral: trigonometric',
            'int_casi_invtrig': 'Almost immediate integral: inverse trigonometric',
            'int_casi_logacot': 'Almost immediate integral: logarithm + arctangent',
            'int_rac_simples': 'Rational integral: simple roots',
            'int_rac_multiples': 'Rational integral: multiple roots',
            'int_rac_grado2': 'Rational integral: quadratic factor',
            'int_trig': 'Special trigonometric integral',
            'int_partes': 'Integration by parts',
            'int_cambio_fractrig': 'Substitution integral: trigonometric fraction',
            'int_cambio_irracional': 'Substitution integral: irrational function',
            'der_polinomica': 'Derivative: polynomial',
            'der_trigonometrica': 'Derivative: trigonometric',
            'der_exponencial': 'Derivative: exponential',
            'der_logaritmica': 'Derivative: logarithmic',
            'der_regla_cadena': 'Derivative: chain rule',
            'der_implicita': 'Derivative: implicit',
            'lim_infinito': 'Limit at infinity',
            'lim_indeterminado': 'Limit with indeterminate form',
            'lim_trigonometrico': 'Trigonometric limit',
            'lim_especial': 'Special limit (Euler number)',
            'frac_simplificar': 'Simplify fraction',
            'frac_sumar': 'Add fractions',
            'frac_multiplicar': 'Multiply fractions',
            'frac_division': 'Divide fractions',
            'func_dominio': 'Function domain',
            'func_recorrido': 'Function range',
            'func_ceros': 'Function zeros',
            'func_crecimiento': 'Function growth',
            'ext_polinomico': 'Extrema: polynomial',
            'ext_trigonometrico': 'Extrema: trigonometric',
            'ext_racional': 'Extrema: rational',
            'asint_vertical': 'Vertical asymptote',
            'asint_horizontal': 'Horizontal asymptote',
            'asint_oblicua': 'Oblique asymptote',
            'asint_mixta': 'Mixed asymptotes',
            'anal_polinomico': 'Analysis: polynomial',
            'anal_racional': 'Analysis: rational',
            'anal_trigonometrico': 'Analysis: trigonometric',
        }
        print('✅ Generator initialized with 48 exercise subtypes')

    def render_expression(self, latex_expression, size=16):
        if not latex_expression:
            return None
        fig, ax = plt.subplots(figsize=(7, 1.2))
        ax.axis('off')
        ax.text(0.5, 0.5, f'${latex_expression}$',
                fontsize=size, ha='center', va='center')
        plt.tight_layout(pad=0.1)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                    pad_inches=0.05, facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    def generate_exercises_by_subtypes(self, selected_types):
        exercises = []
        used_exercises = set()  # ← NEW: Track to prevent duplicates

        for item in selected_types:
            subtype_id = item['id']
            quantity = item.get('quantity', 1)
            if subtype_id not in self.subtypes_map:
                print(f'⚠️ Unrecognized subtype: {subtype_id}')
                continue
            generator_func = self.subtypes_map[subtype_id]
            name = self.subtypes_names.get(subtype_id, subtype_id)
            print(f'   - Generating {quantity} of {name}')

            for _ in range(quantity):
                attempts = 0
                max_attempts = 20  # Prevent infinite loop
                exercise = None

                while attempts < max_attempts:
                    try:
                        exercise = generator_func('medium')
                        exercise['type'] = name

                        # Create a unique key for this exercise
                        exercise_key = str(exercise.get(
                            'statement', '')) + str(exercise.get('statement_text', ''))

                        # If this exercise hasn't been used before, keep it
                        if exercise_key not in used_exercises:
                            used_exercises.add(exercise_key)
                            exercises.append(exercise)
                            break

                        attempts += 1
                        print(
                            f'      ⚠️ Duplicate detected, regenerating... ({attempts}/{max_attempts})')

                    except Exception as exc:
                        print(f'      ❌ Error: {exc}')
                        exercises.append(self._exercise_error(name))
                        break

                if attempts >= max_attempts:
                    print(
                        f'      ⚠️ Could not generate unique exercise after {max_attempts} attempts')
                    exercises.append(self._exercise_error(name))

        print(f'✅ {len(exercises)} exercises generated')
        return exercises

    def _exercise_error(self, name):
        return {
            'statement': 'Error generating exercise',
            'solution': 'Error generating solution',
            'statement_text': f'Could not generate the exercise for {name}',
            'statement_img': None,
            'solution_img': None,
            'type': name,
        }

    def _make_integral(self, expr, statement_text):
        solution = sp.integrate(expr, self.x)
        statement_latex = r'\int ' + sp.latex(expr) + r' \, dx'
        solution_latex = sp.latex(solution) + ' + C'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': statement_text,
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _make_derivative(self, expr, statement_text):
        solution = sp.diff(expr, self.x)
        statement_latex = sp.latex(expr)
        solution_latex = sp.latex(solution)
        return {
            'statement': f'Find the derivative of {statement_latex}',
            'solution': solution_latex,
            'statement_text': statement_text,
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _make_limit(self, expr, statement_text):
        solution = sp.limit(expr, self.x, sp.oo)
        statement_latex = r'\lim_{x \to \infty} ' + sp.latex(expr)
        solution_latex = sp.latex(solution)
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': statement_text,
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    # ===== INTEGRALS =====
    def _integral_polynomial(self, difficulty):
        # Generate random polynomial: coefficient * x^n
        n = random.randint(2, 6)
        coeff = random.randint(1, 5)
        expr = coeff * self.x**n + random.randint(-3, 3) * self.x**(n-1)
        return self._make_integral(expr, 'Calculate the following immediate integral')

    def _integral_logarithm(self, difficulty):
        expr = 1 / self.x
        return self._make_integral(expr, 'Calculate the following logarithmic integral')

    def _integral_exponential(self, difficulty):
        expr = exp(self.x)
        return self._make_integral(expr, 'Calculate the following exponential integral')

    def _integral_trigonometric(self, difficulty):
        funcs = [sin, cos]
        func = random.choice(funcs)
        expr = func(self.x)
        return self._make_integral(expr, 'Calculate the following trigonometric integral')

    def _integral_inverse_trig(self, difficulty):
        expr = 1 / (1 + self.x**2)
        return self._make_integral(expr, 'Calculate the following inverse trigonometric integral')

    def _integral_almost_power(self, difficulty):
        a = random.randint(1, 3)
        n = random.randint(2, 4)
        expr = (a * self.x + 1) ** n
        return self._make_integral(expr, 'Calculate the following almost immediate integral')

    def _integral_almost_log(self, difficulty):
        a = random.randint(1, 3)
        expr = 1 / (a * self.x + 1)
        return self._make_integral(expr, 'Calculate the following almost immediate logarithmic integral')

    def _integral_almost_exp(self, difficulty):
        a = random.randint(1, 3)
        b = random.randint(0, 3)
        expr = exp(a * self.x + b)
        return self._make_integral(expr, 'Calculate the following almost immediate exponential integral')

    def _integral_almost_trig(self, difficulty):
        a = random.randint(1, 3)
        b = random.randint(0, 3)
        expr = sin(a * self.x + b)
        return self._make_integral(expr, 'Calculate the following almost immediate trigonometric integral')

    def _integral_almost_invtrig(self, difficulty):
        a = random.randint(1, 3)
        expr = 1 / (1 + (a * self.x) ** 2)
        return self._make_integral(expr, 'Calculate the following almost immediate inverse trigonometric integral')

    def _integral_almost_logacot(self, difficulty):
        a = random.randint(1, 3)
        expr = (a * self.x) / (1 + self.x**2)
        return self._make_integral(expr, 'Calculate the following almost immediate integral with logarithm and arctangent')

    def _integral_rational_simple(self, difficulty):
        a = random.randint(2, 4)
        expr = 1 / (self.x**2 - a**2)
        return self._make_integral(expr, 'Calculate the following rational integral with simple roots')

    def _integral_rational_multiple(self, difficulty):
        a = random.randint(2, 3)
        expr = 1 / (self.x**3 - a**2 * self.x)
        return self._make_integral(expr, 'Calculate the following rational integral with multiple roots')

    def _integral_rational_degree2(self, difficulty):
        a = random.randint(1, 3)
        expr = 1 / (self.x**2 + 2 * a * self.x + 2 * a**2)
        return self._make_integral(expr, 'Calculate the following rational integral with a quadratic factor')

    def _integral_trig_special(self, difficulty):
        func = random.choice([sin, cos])
        expr = func(self.x) ** 2
        return self._make_integral(expr, 'Calculate the following special trigonometric integral')

    def _integral_by_parts(self, difficulty):
        expr = self.x * exp(self.x)
        return self._make_integral(expr, 'Calculate the following integral by parts')

    def _integral_change_fraction_trig(self, difficulty):
        expr = sin(self.x) / cos(self.x)
        return self._make_integral(expr, 'Calculate the following integral through a trigonometric substitution')

    def _integral_change_irrational(self, difficulty):
        expr = sqrt(self.x + 1)
        return self._make_integral(expr, 'Calculate the following integral with an irrational function')

    # ===== DERIVATIVES =====
    def _derivative_polynomial(self, difficulty):
        n = random.randint(2, 5)
        coeff = random.randint(1, 5)
        expr = coeff * self.x**n + random.randint(-3, 3) * self.x**(n-1)
        return self._make_derivative(expr, 'Find the derivative of the following polynomial')

    def _derivative_trigonometric(self, difficulty):
        funcs = [sin, cos, tan]
        func = random.choice(funcs)
        expr = func(self.x)
        return self._make_derivative(expr, 'Find the derivative of the following trigonometric function')

    def _derivative_exponential(self, difficulty):
        a = random.randint(1, 3)
        expr = exp(a * self.x)
        return self._make_derivative(expr, 'Find the derivative of the following exponential function')

    def _derivative_logarithmic(self, difficulty):
        a = random.randint(1, 3)
        expr = log(a * self.x**2 + 1)
        return self._make_derivative(expr, 'Find the derivative of the following logarithmic function')

    def _derivative_chain_rule(self, difficulty):
        a = random.randint(1, 3)
        n = random.randint(2, 4)
        expr = (a * self.x**2 + 1) ** n
        return self._make_derivative(expr, 'Find the derivative using the chain rule')

    def _derivative_implicit(self, difficulty):
        a = random.randint(2, 5)
        expr = self.x**2 + self.y**2 - a**2
        return self._make_derivative(expr, 'Find the implicit derivative of the following relation')

    # ===== LIMITS =====
    def _limit_infinity(self, difficulty):
        a = random.randint(1, 3)
        expr = (a * self.x + 1) / (self.x + 1)
        return self._make_limit(expr, 'Find the limit as x tends to infinity')

    def _limit_indeterminate(self, difficulty):
        a = random.randint(2, 4)
        expr = (self.x**2 - a**2) / (self.x - a)
        return self._make_limit(expr, 'Find the limit of the indeterminate form')

    def _limit_trigonometric(self, difficulty):
        expr = sin(self.x) / self.x
        return self._make_limit(expr, 'Find the trigonometric limit')

    def _limit_special(self, difficulty):
        expr = (1 + 1 / self.x) ** self.x
        return self._make_limit(expr, "Find the special limit involving Euler's number")

    # ===== FRACTIONS =====
    def _fraction_simplify(self, difficulty):
        # Generate random fractions with different values
        numerator = random.randint(4, 12)
        denominator = random.randint(2, 12)
        while denominator % 2 == 0 or denominator % 3 == 0:
            denominator = random.randint(2, 12)
        # Ensure fraction is not already simplified
        if numerator % denominator == 0:
            numerator = denominator * random.randint(2, 4)
        simplified = sp.simplify(sp.Rational(numerator, denominator))
        statement_latex = sp.latex(sp.Rational(numerator, denominator))
        solution_latex = sp.latex(simplified)
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Simplify the following fraction',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _fraction_add(self, difficulty):
        # Random fractions with different denominators
        a = random.randint(1, 5)
        b = random.randint(2, 6)
        c = random.randint(1, 5)
        d = random.randint(2, 6)
        while d == b:
            d = random.randint(2, 6)
        statement_latex = sp.latex(sp.Rational(
            a, b)) + ' + ' + sp.latex(sp.Rational(c, d))
        solution_latex = sp.latex(sp.Rational(a, b) + sp.Rational(c, d))
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Add the following fractions',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _fraction_multiply(self, difficulty):
        a = random.randint(1, 5)
        b = random.randint(2, 6)
        c = random.randint(1, 5)
        d = random.randint(2, 6)
        statement_latex = sp.latex(sp.Rational(
            a, b)) + ' \\cdot ' + sp.latex(sp.Rational(c, d))
        solution_latex = sp.latex(sp.Rational(a, b) * sp.Rational(c, d))
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Multiply the following fractions',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _fraction_divide(self, difficulty):
        a = random.randint(1, 5)
        b = random.randint(2, 6)
        c = random.randint(1, 5)
        d = random.randint(2, 6)
        statement_latex = sp.latex(sp.Rational(
            a, b)) + ' \\div ' + sp.latex(sp.Rational(c, d))
        solution_latex = sp.latex(sp.Rational(a, b) / sp.Rational(c, d))
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Divide the following fractions',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    # ===== FUNCTIONS =====
    def _function_domain(self, difficulty):
        a = random.randint(1, 4)
        statement_latex = r'\sqrt{x-' + str(a) + r'}'
        solution_latex = f'x \\ge {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the domain of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _function_range(self, difficulty):
        a = random.randint(1, 3)
        statement_latex = f'f(x)={a}x^2'
        solution_latex = 'y \\ge 0'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the range of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression('y \\ge 0'),
        }

    def _function_zeros(self, difficulty):
        a = random.randint(2, 5)
        statement_latex = f'x^2-{a**2}'
        solution_latex = f'x = \\pm {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the zeros of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _function_growth(self, difficulty):
        n = random.choice([2, 3, 5])
        statement_latex = f'f(x)=x^{n}'
        solution_latex = f'Increasing on \\mathbb{{R}}' if n % 2 == 1 else f'Decreases on (-\\infty, 0), increases on (0, \\infty)'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Determine the growth of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    # ===== EXTREMA =====
    def _extreme_polynomial(self, difficulty):
        a = random.randint(2, 5)
        statement_latex = f'f(x)=x^2-{a}x+1'
        solution_latex = f'Minimum at x = {a/2:.1f}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the extrema of the following polynomial function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _extreme_trigonometric(self, difficulty):
        statement_latex = r'f(x)=\sin(x)'
        solution_latex = r'Maximum at x = \frac{\pi}{2}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the extrema of the following trigonometric function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _extreme_rational(self, difficulty):
        a = random.randint(1, 3)
        statement_latex = f'f(x)=\\frac{{{a}x}}{{x^2+1}}'
        solution_latex = f'Maximum at x = 1' if a > 0 else f'Minimum at x = -1'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the extrema of the following rational function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    # ===== ASYMPTOTES =====
    def _asymptote_vertical(self, difficulty):
        a = random.randint(2, 5)
        statement_latex = f'f(x)=\\frac{{1}}{{x-{a}}}'
        solution_latex = f'Vertical asymptote at x = {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the vertical asymptote of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _asymptote_horizontal(self, difficulty):
        a = random.randint(2, 4)
        statement_latex = f'f(x)=\\frac{{{a}x+1}}{{x+1}}'
        solution_latex = f'Horizontal asymptote y = {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the horizontal asymptote of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _asymptote_oblique(self, difficulty):
        a = random.randint(1, 3)
        statement_latex = f'f(x)=\\frac{{x^2+{a}}}{{x}}'
        solution_latex = 'Oblique asymptote y = x'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the oblique asymptote of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _asymptote_mixed(self, difficulty):
        a = random.randint(2, 4)
        statement_latex = f'f(x)=\\frac{{x^2+1}}{{x-{a}}}'
        solution_latex = f'Vertical asymptote x = {a} and oblique asymptote y = x + {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Find the asymptotes of the following function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    # ===== ANALYSIS =====
    def _analysis_polynomial(self, difficulty):
        a = random.randint(2, 4)
        statement_latex = f'f(x)=x^2-{a**2}'
        solution_latex = f'Domain: \\mathbb{{R}}, zeros at x = \\pm {a}, minimum at x = 0'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Analyze the following polynomial function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _analysis_rational(self, difficulty):
        a = random.randint(2, 4)
        statement_latex = f'f(x)=\\frac{{1}}{{x-{a}}}'
        solution_latex = f'Domain: x \\ne {a}, vertical asymptote x = {a}'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Analyze the following rational function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression(solution_latex),
        }

    def _analysis_trigonometric(self, difficulty):
        statement_latex = r'f(x)=\sin(x)'
        solution_latex = 'Domain: \\mathbb{R}, range: [-1,1]'
        return {
            'statement': statement_latex,
            'solution': solution_latex,
            'statement_text': 'Analyze the following trigonometric function',
            'statement_img': self.render_expression(statement_latex),
            'solution_img': self.render_expression('Domain: \\mathbb{R}, range: [-1,1]'),
        }
