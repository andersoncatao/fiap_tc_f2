# fiap_tc_f2

Escalonamento de Funcionários com Algoritmo Genético
Este repositório apresenta uma implementação de Algoritmo Genético (AG) para resolver um problema de escalonamento de funcionários (também conhecido como scheduling ou rostering). O objetivo principal é alocar funcionários em diferentes turnos ao longo de vários dias, respeitando restrições como disponibilidade, carga horária máxima semanal e garantindo que cada funcionário não seja escalado em mais de um turno no mesmo dia.

Tabela de Conteúdos
Visão Geral
Principais Funcionalidades
Estrutura do Projeto
Dependências
Como Executar
Como Funciona
Representação (Cromossomo)
Função de Fitness
Função de Reparo
Operadores Genéticos
Personalização
Referências
Licença
Visão Geral
Em empresas de diversos segmentos, como lojas de varejo, hospitais, call centers e indústrias, é fundamental criar escalas de trabalho eficientes. Alguns pontos importantes do problema são:

Disponibilidade: alguns funcionários podem trabalhar apenas em horários específicos.
Limites de Carga Horária: cada funcionário tem um número máximo de horas permitido por semana (20, 30, 40 etc.).
Cobertura Mínima: cada turno requer um número mínimo de funcionários para garantir o funcionamento adequado.
Restrições de Dupla Alocação: nenhum funcionário pode ser escalado em dois turnos no mesmo dia.
Este projeto utiliza um Algoritmo Genético que busca soluções de escalonamento satisfazendo o máximo de restrições possível e minimizando penalizações associadas a violações (como indisponibilidade ou exceder carga horária).

Principais Funcionalidades
Proibição de Alocação Dupla: uma função de reparo impede que o mesmo funcionário trabalhe em mais de um turno do mesmo dia.
Verificação de Disponibilidade: a função de fitness penaliza a alocação de funcionários em horários que eles não podem cumprir.
Carga Horária Semanal: exceder o limite de horas de um funcionário gera penalizações, forçando o AG a buscar soluções viáveis.
Código em Python: implementação clara e comentada, facilitando adaptações futuras.
Estrutura do Projeto
bash
.
├── README.md                 # Documento de apresentação do projeto
├── run_ag.py                 # Script principal com a implementação do AG
└── ...
run_ag.py: contém:
Dados dos funcionários (disponibilidade e limite de horas).
Definições dos parâmetros do AG (tamanho da população, taxas de crossover e mutação, número de gerações).
Funções de fitness, crossover, mutação, seleção e reparo.

Dependências
Python 3.7+ (ou versão mais recente).
Uso apenas de bibliotecas padrão (random, etc.).


Como Funciona
Representação (Cromossomo)
Cada cromossomo é uma lista de inteiros, onde cada inteiro representa o ID de um funcionário.
O tamanho do cromossomo depende do número de dias multiplicado pelo total de vagas necessárias por dia, conforme a soma de funcionários exigidos em cada turno.

Função de Fitness
A função de avaliação (fitness) atribui penalizações quando:
Um funcionário é escalado fora do seu horário de disponibilidade.
Um funcionário excede sua carga horária semanal.
O fitness resultante é 1 / (1 + penalizacao), de forma que quanto menor a penalização, maior o fitness.

Função de Reparo
Após a geração ou mutação dos cromossomos, a função de reparo impede que o mesmo funcionário seja alocado mais de uma vez no mesmo dia.
Se for detectado que um funcionário aparece duas vezes, é feita uma substituição por outro funcionário que ainda não tenha sido escalado nesse dia.

Operadores Genéticos
Seleção por Torneio
Seleciona indivíduos mais aptos (com maior fitness) para reprodução, mantendo algum grau de aleatoriedade.

Crossover de Um Ponto
Combina dois cromossomos (pais), trocando parte dos genes de cada um, o que gera diversidade de soluções.

Mutação
Cada gene (vaga) pode ser alterado para outro funcionário aleatório com uma pequena probabilidade, ajudando a evitar a estagnação em ótimos locais.

Personalização
Número de Dias e Turnos: modificar NUM_DIAS, TURNOS_POR_DIA e NECESSIDADE_POR_TURNO de acordo com a realidade do seu projeto.
Funcionários: atualizar a lista FUNCIONARIOS com os nomes, disponibilidades e limites de horas do seu caso específico.
Parâmetros do AG: ajustar TAMANHO_POPULACAO, TAXA_CROSSOVER, TAXA_MUTACAO e NUM_GERACOES para melhorar desempenho ou acurácia.
