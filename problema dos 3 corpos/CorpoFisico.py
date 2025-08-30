import math

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
    
    def forca_resultante(self, lista_de_corpos):
        
        forca_resultante= [0,0]
        
        for corpo in lista_de_corpos:
            campo_gravitacional= corpo.campo_gravitacional(self.posicao)
            forca_resultante[0]= forca_resultante[0] + (campo_gravitacional[0] * self.massa)
            forca_resultante[1]= forca_resultante[1] + (campo_gravitacional[1] * self.massa)
        
        return forca_resultante
