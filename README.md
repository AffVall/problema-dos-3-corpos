# Problema dos 3 Corpos - Simulador

Uma simulação do clássico problema dos 3 corpos em física gravitacional, com visualização interativa e geração de vídeos.

## 📖 Descrição

Este projeto simula o movimento de até 4 corpos celestes sob a influência da gravidade mútua. A simulação calcula as trajetórias, detecta colisões e gera visualizações incluindo gráficos de trajectórias, distâncias e velocidades, além de um vídeo animado.

## 🎯 Funcionalidades

- ✅ **Simulação Física Realista**: Cálculo de forças gravitacionais entre múltiplos corpos
- ✅ **Detecção de Colisões**: Identifica quando corpos se chocam com base em seu tamanho
- ✅ **Randomização de Posições**: Opção para gerar condições iniciais aleatórias
- ✅ **Cálculo de Tamanhos Dinâmicos**: Tamanho dos corpos baseado em sua massa
- ✅ **Visualizações**: Gráficos de trajectória, distância entre corpos e velocidade
- ✅ **Video Animado**: Exporta a simulação como arquivo MP4
- ✅ **Logging Detalhado**: Sistema de logs com diferentes níveis (INFO, DEBUG, ERROR)
- ✅ **Modo Debug**: Saída verbosa para diagnóstico

## 📋 Requisitos

- Python 3.8+
- Bibliotecas: numpy, matplotlib, opencv-python

## 🚀 Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd problema-dos-3-corpos
```

2. Crie um ambiente virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Edite o arquivo `config.ini` para customizar a simulação:

```ini
[SIMULATION]
simulation_cycles = 100000000       # Número máximo de ciclos
time_step = 0.01                    # Intervalo de tempo por ciclo
randomize_positions = False         # Gerar posições aleatórias
calculate_sizes = True              # Calcular tamanho baseado em massa
debug = True                        # Modo debug
size_scale_factor = 8               # Fator de escala para tamanho
min_velocity = -0.2                 # Velocidade mínima
max_velocity = 0.2                  # Velocidade máxima
collision_distance = 1.5            # Distância de colisão (não usado)

[VISUALIZATION]
grid_width = 300                    # Largura do grid
grid_height = 300                   # Altura do grid
scale_factor = 0.1                  # Fator de escala visual
plot_dpi = 200                      # DPI dos gráficos
save_plots = True                   # Salvar gráficos
high_quality_plots = True           # Gráficos de alta qualidade

[OUTPUT]
frame_interval = 1500               # Intervalo entre frames
min_frames = 15                     # Mínimo de frames necessários
max_retries = 30                    # Tentativas máximas de retry

[MERCURY]
name = mercury
mass = 50
pos_x = 80
pos_y = 150
vel_x = 0.1
vel_y = 0.0

[MARS]
name = mars
mass = 40
pos_x = 150
pos_y = 280
vel_x = -0.05
vel_y = 0.0

[VALERIA]
name = valeria
mass = 45
pos_x = 250
pos_y = 100
vel_x = 0.0
vel_y = 0.1

[VENUS]
name = venus
mass = 35
pos_x = 200
pos_y = 200
vel_x = -0.1
vel_y = -0.05
```

## 🎮 Uso

Execute a simulação:

```bash
python main.py
```

A simulação criará um diretório `resultados_*` com:

- `trajectories.png` - Gráfico das trajetórias
- `distances.png` - Gráfico das distâncias entre corpos
- `velocity.png` - Gráfico das velocidades
- `simulation.mp4` - Vídeo animado da simulação
- `logs/simulation.log` - Arquivo de log

## 📊 Saída

### Arquivos Gerados

- **Gráficos PNG**: Visualizações estáticas das trajectórias, distâncias e velocidades
- **Vídeo MP4**: Animação da simulação com 10 FPS
- **Log de Simulação**: Registro detalhado de eventos e métricas

### Condições de Término

- ✅ **max_cycles**: Número máximo de ciclos atingido
- ✅ **collision_x_y**: Colisão entre corpos X e Y
- ✅ **boundary_exit_x**: Corpo X saiu dos limites da grid

## 🔬 Física

### Força Gravitacional

$$
F = \frac{G \cdot m_1 \cdot m_2}{r^2}
$$

Onde:

- G = 10.0 (constante gravitacional do sistema)
- m₁, m₂ = massas dos corpos
- r = distância entre corpos

### Integração Numérica

- Aceleração: `a = F / m`
- Velocidade: `v(t+dt) = v(t) + a*dt`
- Posição: `x(t+dt) = x(t) + v*dt`

### Detecção de Colisão

Dois corpos colidem quando: `distância < (tamanho₁ + tamanho₂) / 2`

## 📁 Estrutura do Projeto

```
problema-dos-3-corpos/
├── main.py                 # Função principal e simulação
├── config.py               # Gerenciador de configuração
├── phisicBodies.py         # Classe Body (corpos celestes)
├── config.ini              # Arquivo de configuração
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
└── resultados_*/           # Diretório de saída (gerado)
```

## 🐛 Troubleshooting

### "Config file not found"

Certifique-se de que `config.ini` está no mesmo diretório que `main.py`.

### "Insufficient frames"

Diminua `simulation_cycles` ou `frame_interval` no `config.ini`, ou aumente `min_frames`.

### Cores não aparecem no vídeo

Esse é um comportamento conhecido. As cores aparecem nos gráficos estáticos corretamente.

## 🤝 Contribuindo

Sinta-se livre para fazer fork, melhorar e enviar pull requests!

## 📄 Licença

Este projeto está disponível sob a licença MIT.

## 👨‍💼 Autor

Criado como projeto educacional sobre simulações físicas em Python.

---

**Última atualização**: 29 de março de 2026
