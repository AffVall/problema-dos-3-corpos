import numpy as np
import math
import matplotlib.pyplot as plt

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
    
#PAARAMETROS
CICLOS_DE_SIMULACAO= 300
DIMENCOES_DA_MALHA= (40, 40)
GRADE = [[0 for x in range(DIMENCOES_DA_MALHA[0])]for y in range(DIMENCOES_DA_MALHA[1])]
#PARAMETROS
mercurio = corpo(0.2, 0, {'x': 12,'y': 8},'mercurio')
venus = corpo(0.2, 0, {'x': 31,'y': 29},'venus')
marte = corpo(0.2, 0, {'x': 14,'y': 38},'marte')

GRADE[mercurio.posicao['y']][mercurio.posicao['x']] = mercurio.nome
GRADE[venus.posicao['y']][venus.posicao['x']] = venus.nome
GRADE[marte.posicao['y']][marte.posicao['x']] = marte.nome

for i in range(CICLOS_DE_SIMULACAO):

    #verificar a força resultante sobre cada corpo e atualizar aceleraçao e velocidade
    #mover cada corpo de acordo com sua velocidade(move 1x velocidade por ciclo. converter a velocidade em m/s para unidade/ciclo)
    #printar a grade ou preferencialmente fazer a animaçao como os automatos celulares
    #>>talvez mover o corpo antes de verificar a força faça mais sentido fisico<<
    
for linha in GRADE:
    print(f'{linha}\n')
