import numpy as np
import math
import matplotlib.pyplot as plt

GRADE = [[0 for x in range(40)]for y in range(40)]
class corpo:
    GRAVIDADE = 6.67430e-11 
    def __init__(self, massa, velocidade, posicao, nome= None):
        self.nome = nome
        self.massa = float(massa)
        self.velocidade = velocidade
        self.posicao = {
            'x':posicao['x'],
            'y':posicao['y'],
        }
    def campo_gravitacional(self,ponto):
        distancia_x = self.posicao['x'] - ponto['x']
        distancia_y = self.posicao['y'] - ponto['y']
        distancia_principal = math.sqrt(distancia_x**2+distancia_y**2)
        if distancia_principal == 0:
            return (0,0)
        modulo_cg = self.GRAVIDADE * self.massa / distancia_principal**2
        cg_x = -modulo_cg * distancia_x / distancia_principal
        cg_y = -modulo_cg * distancia_y / distancia_principal
        return (cg_x,cg_y)

mercurio = corpo(0.2, 0, {'x': 12,'y': 8},'mercurio')
venus = corpo(0.2, 0, {'x': 31,'y': 29},'venus')
marte = corpo(0.2, 0, {'x': 14,'y': 38},'marte')

GRADE[mercurio.posicao['y']][mercurio.posicao['x']] = mercurio.nome
GRADE[venus.posicao['y']][venus.posicao['x']] = venus.nome
GRADE[marte.posicao['y']][marte.posicao['x']] = marte.nome


for linha in GRADE:
    print(f'{linha}\n')
