import numpy as np
import matplotlib.pyplot as plt
from CorpoFisico import corpo


    
#PAARAMETROS
CICLOS_DE_SIMULACAO= 300
DIMENCOES_DA_MALHA= (30, 30)
GRADE = [[0 for x in range(DIMENCOES_DA_MALHA[0])]for y in range(DIMENCOES_DA_MALHA[1])]
#PARAMETROS
mercurio = corpo(0.2, 0, {'x': 12,'y': 8},'mercurio')
venus = corpo(0.2, 0, {'x': 3,'y': 29},'venus')
marte = corpo(0.2, 0, {'x': 14,'y': 29},'marte')

GRADE[mercurio.posicao['y']][mercurio.posicao['x']] = mercurio.nome
GRADE[venus.posicao['y']][venus.posicao['x']] = venus.nome
GRADE[marte.posicao['y']][marte.posicao['x']] = marte.nome

for i in range(CICLOS_DE_SIMULACAO):

    #verificar a força resultante sobre cada corpo e atualizar aceleraçao e velocidade
    #mover cada corpo de acordo com sua velocidade(move 1x velocidade por ciclo. converter a velocidade em m/s para unidade/ciclo)
    #printar a grade ou preferencialmente fazer a animaçao como os automatos celulares
    #>>talvez mover o corpo antes de verificar a força faça mais sentido fisico<<
    0
    
for linha in GRADE:
    print(f'{linha}\n')
