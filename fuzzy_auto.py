import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt  # Agregar esta línea

# Definir variables de entrada y salida difusa
v = ctrl.Antecedent(np.arange(0, 121, 1), 'velocidad')  # Rango de velocidad de 0 a 120 km/h
d = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')  # Rango de distancia de 0 a 100 metros
c = ctrl.Consequent(np.arange(-10, 11, 1), 'control')  # Rango de ajuste de velocidad de -10 a 10

# Definir las funciones de membresía para velocidad
v['baja'] = fuzz.trapmf(v.universe, [0, 0, 30, 40])
v['moderada'] = fuzz.trimf(v.universe, [30, 50, 70])
v['alta'] = fuzz.trapmf(v.universe, [60, 80, 120, 120])

# Definir las funciones de membresía para distancia
d['cerca'] = fuzz.trapmf(d.universe, [0, 0, 5, 10])
d['moderada'] = fuzz.trimf(d.universe, [5, 15, 25])
d['lejos'] = fuzz.trapmf(d.universe, [20, 30, 50, 50])

# Definir las funciones de membresía para el control de velocidad
c['reducir'] = fuzz.trimf(c.universe, [-10, -5, 0])
c['mantener'] = fuzz.trimf(c.universe, [-5, 0, 5])
c['aumentar'] = fuzz.trapmf(c.universe, [0, 10, 20, 20])

# Visualización de las funciones de membresía
v.view()
d.view()
c.view()

# Definir las reglas difusas
rule1 = ctrl.Rule(v['alta'] & d['cerca'], c['reducir'])
rule2 = ctrl.Rule(v['alta'] & d['moderada'], c['reducir'])
rule3 = ctrl.Rule(v['alta'] & d['lejos'], c['mantener'])
rule4 = ctrl.Rule(v['moderada'] & d['moderada'], c['reducir'])
rule5 = ctrl.Rule(v['moderada'] & d['moderada'], c['reducir'])
rule6 = ctrl.Rule(v['moderada'] & d['lejos'], c['mantener'])
rule7 = ctrl.Rule(v['baja'] & d['cerca'], c['mantener'])
rule8 = ctrl.Rule(v['baja'] & d['moderada'], c['mantener'])
rule9 = ctrl.Rule(v['baja'] & d['lejos'], c['aumentar'])

# Crear el sistema de control difuso
sistema_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
controlador = ctrl.ControlSystemSimulation(sistema_control)

# Asignar valores a las variables de entrada
controlador.input['velocidad'] = 75  # Ejemplo de velocidad
controlador.input['distancia'] = 30  # Ejemplo de distancia al obstáculo

# Computar el sistema de control difuso
controlador.compute()

# Obtener el valor de salida (ajuste de velocidad)
print("Ajuste de velocidad:", controlador.output['control'])

# Visualización de la distribución de salida
c.view(sim=controlador)

plt.show()
