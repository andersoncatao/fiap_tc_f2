import random  

# -----------------------------------------------------------------
# 1. PARÂMETROS DO PROBLEMA
# -----------------------------------------------------------------

NUM_DIAS = 7         # Quantos dias vou escalonar
TURNOS_POR_DIA = 3   # Quantos turnos existem em cada dia (ex.: 3 turnos: manhã, tarde, noite)

# Lista de funcionários; cada funcionário tem:
# - id (identificador único)
# - nome
# - disponibilidade (lista de intervalos [hora_inicial, hora_final])
# - max_horas_semana (quantidade máxima de horas que pode trabalhar na semana)
FUNCIONARIOS = [
    {"id": 0, "nome": "Ana",    "disponibilidade": [(0, 5), (8, 22)], "max_horas_semana": 40},
    {"id": 1, "nome": "Bruno",  "disponibilidade": [(6, 10), (14, 18)], "max_horas_semana": 30},
    {"id": 2, "nome": "Carla",  "disponibilidade": [(0, 12), (14, 23)], "max_horas_semana": 35},
    {"id": 3, "nome": "Diego",  "disponibilidade": [(0, 24)], "max_horas_semana": 20},
    {"id": 4, "nome": "Eliana", "disponibilidade": [(0, 24)], "max_horas_semana": 20}
]

# Turnos
# Turno 0 (Manhã):  6h - 14h
# Turno 1 (Tarde): 14h - 22h
# Turno 2 (Noite): 22h - 6h (dia seguinte, simplificado)

# Necessidade de funcionários por turno: quantos funcionários queremos em cada turno
NECESSIDADE_POR_TURNO = [2, 1, 1]  # 2 na manhã, 1 à tarde, 1 à noite

# -----------------------------------------------------------------
# 2. PARÂMETROS DO ALGORITMO GENÉTICO
# -----------------------------------------------------------------

TAMANHO_POPULACAO = 100   # Quantidade de indivíduos na população do AG
TAXA_CROSSOVER = 0.6     # Probabilidade de ocorrer crossover entre dois indivíduos
TAXA_MUTACAO = 0.1       # Probabilidade de mutar cada gene
NUM_GERACOES = 100       # Quantidade de gerações que o AG irá evoluir

# -----------------------------------------------------------------
# 3. REPRESENTAÇÃO DOS INDIVÍDUOS (CROMOSSOMO)
# -----------------------------------------------------------------

TOTAL_VAGAS_DIA = sum(NECESSIDADE_POR_TURNO)  #  2+1+1 = 4 vagas/dia

# Quantas vagas totais na semana inteira?
TAMANHO_CROMOSSOMO = NUM_DIAS * sum(NECESSIDADE_POR_TURNO)  # 7 * 4 = 28, mas vezes 3 turnos?

def gerar_individuo_aleatorio():
    """
    Gera um cromossomo aleatório:
    - Cada gene é um ID de funcionário (entre 0 e len(FUNCIONARIOS)-1).
    - O tamanho do cromossomo é TAMANHO_CROMOSSOMO.
    """
    return [
        random.randint(0, len(FUNCIONARIOS)-1) 
        for _ in range(TAMANHO_CROMOSSOMO)
    ]

# -----------------------------------------------------------------
# 4. FUNÇÃO DE REPARO: NUNCA TER O MESMO FUNCIONÁRIO NO MESMO DIA
# -----------------------------------------------------------------

def reparar_individuo(cromossomo):
    """
    Garante que um mesmo funcionário não apareça 2 vezes no mesmo dia.
    Estratégia:
      - Percorrer o cromossomo 'dia a dia'.
      - Manter um conjunto 'funcionarios_no_dia'.
      - Se encontrarmos duplicata, escolhemos outro funcionário que ainda não tenha sido escalado nesse dia.
    """
    pos = 0  # Índice para percorrer a lista 'cromossomo'
    for dia in range(NUM_DIAS):
        funcionarios_no_dia = set()  # Conjunto para rastrear quem já foi alocado neste dia
        for turno_idx in range(TURNOS_POR_DIA):
            # Para cada turno, temos NECESSIDADE_POR_TURNO[turno_idx] vagas
            num_vagas_turno = NECESSIDADE_POR_TURNO[turno_idx]
            for _ in range(num_vagas_turno):
                f_id = cromossomo[pos]
                # Verifica se esse funcionario já está no dia
                if f_id in funcionarios_no_dia:
                    # Precisamos trocar por outro funcionário que NÃO está no dia
                    tentativas = 0
                    novo_f_id = random.randint(0, len(FUNCIONARIOS)-1)
                    # Tentar achar outro f_id livre para o dia
                    while (novo_f_id in funcionarios_no_dia) and (tentativas < 100):
                        novo_f_id = random.randint(0, len(FUNCIONARIOS)-1)
                        tentativas += 1
                    # Substitui no cromossomo
                    cromossomo[pos] = novo_f_id
                    # E registra no conjunto
                    funcionarios_no_dia.add(novo_f_id)
                else:
                    # Se não estava no dia, apenas adiciona ao conjunto
                    funcionarios_no_dia.add(f_id)

                pos += 1
    return cromossomo

# -----------------------------------------------------------------
# 5. FUNÇÃO DE FITNESS: AVALIA O "QUÃO BOA" É A SOLUÇÃO
# -----------------------------------------------------------------

def calcular_fitness(cromossomo):
    """
    Avalia o quão boa é a escala, atribuindo penalizações:
      - Se o funcionário estiver fora de disponibilidade
      - Se exceder a carga horária semanal
    Quanto maior o fitness, melhor (menor penalização).
    """
    # Decodificar o cromossomo em algo do tipo escalonamento[dia][turno] = lista de f_ids
    escalonamento = []
    pos = 0
    for dia in range(NUM_DIAS):
        turnos_dia = []
        for turno_idx in range(TURNOS_POR_DIA):
            vagas = []
            for _ in range(NECESSIDADE_POR_TURNO[turno_idx]):
                vagas.append(cromossomo[pos])
                pos += 1
            turnos_dia.append(vagas)
        escalonamento.append(turnos_dia)

    # Calcular penalizacoes e total de horas de cada funcionario
    penalizacao = 0
    horas_por_func = [0] * len(FUNCIONARIOS)

    for dia in range(NUM_DIAS):
        for turno_idx in range(TURNOS_POR_DIA):
            # Obtem lista de funcionarios no turno atual
            funcionarios_no_turno = escalonamento[dia][turno_idx]
            # Verifica disponibilidade, soma horas etc.
            for f_id in funcionarios_no_turno:
                duracao_turno = 8  # (8 horas)

                # Verifica disponibilidade (simplificada) de cada turno
                if turno_idx == 0:  # Manhã (6-14h)
                    # Se não houver nenhum intervalo que cubra (6 -> 14)
                    if not any(6 >= disp[0] and 14 <= disp[1] for disp in FUNCIONARIOS[f_id]["disponibilidade"]):
                        penalizacao += 5
                elif turno_idx == 1:  # Tarde (14-22h)
                    if not any(14 >= disp[0] and 22 <= disp[1] for disp in FUNCIONARIOS[f_id]["disponibilidade"]):
                        penalizacao += 5
                else:  # Noite (22-6h)
                    # Dividimos em 22-24 e 0-6
                    if not any(22 >= disp[0] and 24 <= disp[1] for disp in FUNCIONARIOS[f_id]["disponibilidade"]):
                        penalizacao += 5
                    if not any(0 >= disp[0] and 6 <= disp[1] for disp in FUNCIONARIOS[f_id]["disponibilidade"]):
                        penalizacao += 5

                # Soma as horas trabalhadas no total
                horas_por_func[f_id] += duracao_turno

    # Verifica se algum funcionário excedeu sua carga horária semanal
    for f_id, horas in enumerate(horas_por_func):
        max_horas = FUNCIONARIOS[f_id]["max_horas_semana"]
        if horas > max_horas:
            excedente = horas - max_horas
            penalizacao += 2 * excedente

    # Converter a penalizacao em fitness.
    # Fitness maior => melhor. Se penalizacao=0 => fitness=1, caso contrário < 1.
    fitness = 1 / (1 + penalizacao)
    return fitness

# -----------------------------------------------------------------
# 6. OPERAÇÕES GENÉTICAS: SELEÇÃO, CROSSOVER E MUTAÇÃO
# -----------------------------------------------------------------

def selecao_torneio(populacao, k=2):
    """
    Seleciona 1 indivíduo via torneio de tamanho k.
    """
    candidatos = random.sample(populacao, k)  # escolhe k aleatórios
    vencedor = max(candidatos, key=lambda ind: ind["fitness"])
    return vencedor

def crossover_um_ponto(pai, mae):
    
    if random.random() < TAXA_CROSSOVER:
        ponto_corte = random.randint(1, TAMANHO_CROMOSSOMO - 1)
        filho1 = pai["cromossomo"][:ponto_corte] + mae["cromossomo"][ponto_corte:]
        filho2 = mae["cromossomo"][:ponto_corte] + pai["cromossomo"][ponto_corte:]
        return filho1, filho2
    else:
        # Sem crossover, apenas clonamos
        return pai["cromossomo"][:], mae["cromossomo"][:]

def mutacao(cromossomo):
    """
    Realiza a mutação do cromossomo
    """
    
    for i in range(len(cromossomo)):
        if random.random() < TAXA_MUTACAO:
            cromossomo[i] = random.randint(0, len(FUNCIONARIOS)-1)
    return cromossomo

# -----------------------------------------------------------------
# 7. LOOP PRINCIPAL DO ALGORITMO GENÉTICO
# -----------------------------------------------------------------

def algoritmo_genetico():
    """
    Conduz o fluxo do Algoritmo Genético:
      1. Geração da população inicial (aleatória + reparo).
      2. Avaliação (fitness).
      3. Loop de gerações:
         - Seleção (torneio)
         - Crossover
         - Mutação
         - Reparo
         - Cálculo de fitness
      4. Retorna o melhor indivíduo encontrado
    """
    # 1) GERA POPULAÇÃO INICIAL
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        genes = gerar_individuo_aleatorio()    # Gera cromossomo aleatório
        genes = reparar_individuo(genes)       # Reparo para evitar duplicatas no mesmo dia
        fit = calcular_fitness(genes)          # Calcula o fitness inicial
        populacao.append({"cromossomo": genes, "fitness": fit})

    # 2) EVOLUÇÃO
    for geracao in range(NUM_GERACOES):
        nova_populacao = []
        # Gera novos indivíduos até preencher a nova população
        while len(nova_populacao) < TAMANHO_POPULACAO:
            # Seleciona pai e mãe via torneio
            pai = selecao_torneio(populacao)
            mae = selecao_torneio(populacao)
            # Faz crossover
            filho1_genes, filho2_genes = crossover_um_ponto(pai, mae)
            # Faz mutação
            filho1_genes = mutacao(filho1_genes)
            filho2_genes = mutacao(filho2_genes)
            # Repara para garantir que não haja funcionário duplicado no mesmo dia
            filho1_genes = reparar_individuo(filho1_genes)
            filho2_genes = reparar_individuo(filho2_genes)
            # Calcula o fitness dos filhos
            f1_fit = calcular_fitness(filho1_genes)
            f2_fit = calcular_fitness(filho2_genes)
            # Coloca na nova população
            nova_populacao.append({"cromossomo": filho1_genes, "fitness": f1_fit})
            nova_populacao.append({"cromossomo": filho2_genes, "fitness": f2_fit})

        # Substituímos a população antiga pela nova
        populacao = nova_populacao

        # A cada 10 gerações, podemos imprimir o melhor fitness para acompanhar
        if geracao % 10 == 0:
            melhor = max(populacao, key=lambda ind: ind["fitness"])
            print(f"Geração {geracao}: Melhor Fitness = {melhor['fitness']:.4f}")

    # 3) Encontra e retorna o melhor indivíduo final
    melhor_individuo = max(populacao, key=lambda ind: ind["fitness"])
    return melhor_individuo

# -----------------------------------------------------------------
# 8. EXECUÇÃO PRINCIPAL
# -----------------------------------------------------------------

if __name__ == "__main__":
    # Executa o AG e obtém o melhor indivíduo
    melhor = algoritmo_genetico()
    print("\nMelhor fitness encontrado:", melhor["fitness"])

    # Decodifica o cromossomo do melhor indivíduo e exibe em forma de escalonamento
    cromossomo = melhor["cromossomo"]
    pos = 0
    for dia in range(NUM_DIAS):
        print(f"\nDia {dia+1}:")
        for turno_idx in range(TURNOS_POR_DIA):
            vagas_turno = []
            for _ in range(NECESSIDADE_POR_TURNO[turno_idx]):
                f_id = cromossomo[pos]  # Obtém o funcionário alocado para esta vaga
                vagas_turno.append(FUNCIONARIOS[f_id]["nome"])  # Adiciona nome para exibir
                pos += 1
            print(f"  Turno {turno_idx} -> {vagas_turno}")
