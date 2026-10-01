#Variaveis
TAMANHO_LISTA = 150001
pacientes = [[] for _ in range(TAMANHO_LISTA)]

fila_espera = []
pacientes_atendidos = []
contador_eventos = 0
desistentes = set()  # Conjunto para armazenar CPFs de pacientes que desistiram da fila
total_desistencias = 0  # Contador global de desistências

def _sift_up(heap, index):
    """Sobe o elemento no índice `index` até sua posição correta (Min-Heap)."""
    parent = (index - 1) // 2
    # Enquanto não chegar na raiz e o nó atual for menor que o nó pai:
    while index > 0 and heap[index] < heap[parent]:
        heap[index], heap[parent] = heap[parent], heap[index]  # Troca os elementos
        index = parent
        parent = (index - 1) // 2


def _sift_down(heap, index):
    """Desce o elemento no índice `index` até sua posição correta (Min-Heap)."""
    size = len(heap)

    while True:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # Compara com o filho esquerdo
        if left < size and heap[left] < heap[smallest]:
            smallest = left

        # Compara com o filho direito
        if right < size and heap[right] < heap[smallest]:
            smallest = right

        # Se o menor não for o próprio pai, realiza a troca e continua descendo
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
        else:
            break


def heappush_custom(heap, item):
    """Equivalente a heapq.heappush em O(log n)."""
    heap.append(item)  # Adiciona ao final da lista
    _sift_up(heap, len(heap) - 1)  # Ajusta a subida


def heappop_custom(heap):
    """Equivalente a heapq.heappop em O(log n)."""
    if not heap:
        return None

    # Troca o topo (menor elemento) com o último elemento
    last_item = heap.pop()
    if heap:
        return_item = heap[0]
        heap[0] = last_item
        _sift_down(heap, 0)  # Ajusta a descida
        return return_item

    return last_item

#Funcao para formatar a data
def formatar_date(data):
    return f"{data[:2]}/{data[2:4]}/{data[4:]}"

#Funcao para formatar o Cpf
def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"



# 1 - Funcao para cadastro de novos pacientes
#Função Hash para calcular indice do cpf
def calcular_hash(cpf):
    int_cpf = int(cpf)
    indice = int_cpf % TAMANHO_LISTA
    return indice

# 1 - Funcao para cadastro de novos pacientes
def cadastrar_paciente(cpf):
    global pacientes_cadastrados, contador_eventos
    indice = calcular_hash(cpf)

    paciente_encontrado = None

    for paciente in pacientes[indice]:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        print("Paciente ja possui cadastro!")
        cpf_str = paciente_encontrado['cpf']  # Variavel de controle para formatacao
        cpf_f = formatar_cpf(cpf_str)
        data_str = paciente_encontrado['data']  # Variavel de controle para formatacao de data
        data_f = formatar_date(data_str)
        print(f"CPF: {cpf_f} | Nome: {paciente_encontrado['nome']} | Data: {data_f}")
        contador_eventos += 1
    else:
        nome: str = input(f'Informe o nome do paciente:')
        data: str = input(f'Informe a data de nascimento do paciente:')
        pacientes[indice].append({"cpf": cpf, "nome": nome, "data": data})
        cpf_f = formatar_cpf(cpf)
        data_f = formatar_date(data)
        print(f"CPF: {cpf_f} | Nome: {nome} | Data: {data_f}")
        print (f"inddice : {indice}")
        pacientes_cadastrados += 1
        contador_eventos += 1

# 2 - Funcao Buscar Paciente
def buscar_paciente(cpf):

    global contador_eventos
    indice = calcular_hash(cpf)

    paciente_encontrado = None

    for paciente in pacientes[indice]:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        print("Paciente encontrado com sucesso!")
        cpf_str = paciente_encontrado['cpf'] #Variavel de controle para formatacao de cpf
        data_str = paciente_encontrado['data'] #Variavel de controle para formatacao de data
        data_f = formatar_date(data_str)
        cpf_f = formatar_cpf(cpf_str)
        print(f"CPF: {cpf_f} | Nome: {paciente_encontrado['nome']} | Data: {data_f}")
        contador_eventos += 1
    else:
        print("Paciente ainda nao possui cadastro!")
        cadastrar_paciente(cpf)

# 3 - Funcao para dar entrada do paciente na fila de espera
def dar_entrada(cpf, risco):
    global contador_eventos
    contador_eventos += 1

    # Busca no cadastro via Tabela Hash
    indice = calcular_hash(cpf)
    paciente_encontrado = next(
        (p for p in pacientes[indice] if p["cpf"] == cpf), None
    )

    if not paciente_encontrado:
        print("Paciente ainda não possui cadastro. Cadastrando novo paciente...")
        cadastrar_paciente(cpf)
        paciente_encontrado = next((p for p in pacientes[indice] if p["cpf"] == cpf), None)
        # Rebusca o paciente que acabou de ser cadastrado

# Registra o evento de entrada e adiciona à fila
    if paciente_encontrado:
        contador_eventos += 1  # Incrementa o contador de eventos

    # Cria uma cópia para colocar na fila com as informações da consulta atual
    paciente_fila = paciente_encontrado.copy()
    paciente_fila["risco"] = int(risco)
    paciente_fila["evento_entrada"] = contador_eventos  # Garante que a chave é criada

    # Estrutura do item no heap: (Prioridade/Risco, Ordem de Chegada, Dados do Paciente)
    item_heap = (int(risco), contador_eventos, paciente_fila)

        # Insere mantendo a propriedade de heap em O(log n)
    heappush_custom(fila_espera, item_heap)

    print(
        f"Paciente {paciente_fila['nome']} adicionado à fila no evento nº {contador_eventos} com risco {risco}."
    )

# 4 - Funcao para chamar proximop nome da lista de espera
def chamar_proximo():
    global contador_eventos

    # Usamos um loop while para ir descartando desistentes até achar um paciente ativo
    while fila_espera:

        # Remove o paciente de maior prioridade (menor risco/evento) em O(log n)
        risco, evento_entrada, proximo_paciente = heappop_custom(fila_espera)
        cpf_paciente = proximo_paciente["cpf"]

        chave_desistencia = (cpf_paciente, evento_entrada)  # Verifica se o paciente desistiu

        # Se o paciente estiver no set de desistentes, simplesmente descartamos
        if chave_desistencia in desistentes:
            desistentes.remove(chave_desistencia)  # Remove do set de desistentes
            print(f"Paciente {proximo_paciente['nome']} (CPF: {cpf_paciente}) "
                f"havia desistido. Descartando da fila...")
            continue  # Continua para o próximo paciente na fila

        contador_eventos += 1
        tempo_espera_eventos = contador_eventos - evento_entrada
        proximo_paciente["tempo_espera"] = tempo_espera_eventos
        
        pacientes_atendidos.append(proximo_paciente)

        print(f"Chamando próximo paciente: {proximo_paciente['nome']} com risco {proximo_paciente['risco']}.\n")
        print(f"Tempo de espera do paciente: {tempo_espera_eventos} eventos.\n")

    else:
        print("Não há pacientes na fila de espera. Favor dar entrada na fila de espera antes de chamar o próximo paciente.\n")

# 5 - Funcao para remover pacientes da lista de espera
def desistir_fila(cpf):
    global total_desistencias
    # Registra a desistência do paciente em O(1) sem alterar o Heap diretamente.
    # 1. Verifica se o paciente existe no cadastro do sistema
    indice = calcular_hash(cpf)
    paciente_cadastro = next(
        (p for p in pacientes[indice] if p["cpf"] == cpf), None
    )

    if not paciente_cadastro:
            print("Paciente não encontrado na fila de espera.")
            return

    # 2. Busca a entrada ativa do paciente dentro da fila_espera (Heap)
    # Lembra que cada item no Heap é: (risco, evento_entrada, paciente_dicionario)
    item_fila = next(
        (item for item in fila_espera if item[2]["cpf"] == cpf), None
    )
    if not item_fila:
        print(f"Paciente {paciente_cadastro['nome']} não está na fila de espera.")
        return

    # Extrai o evento_entrada do item encontrado (segunda posição da tupla)
    evento_entrada = item_fila[1]
    chave_desistencia = (cpf, evento_entrada)
    
    if chave_desistencia in desistentes:
        print(f"O paciente {paciente_cadastro['nome']} já registrou desistência anterior.")
    else:
        desistentes.add(chave_desistencia)
        total_desistencias += 1
        print(f"O paciente {paciente_cadastro['nome']} desistiu da fila de espera.")


# 6 - Funcao para apresentar o tamanho da fila
def tamanho_fila_espera():
    print(f"Tamanho da fila de espera: {len(fila_espera)}")

# 7 - Funcao do relatorio do dia
# ------------------------------------------------------------------
# FUNÇÃO AUXILIAR DO MERGE SORT (Divisão e Conquista)
# ------------------------------------------------------------------
def merge_sort_pacientes(lista):
    # Ordena a lista de pacientes recursivamente por tempo_espera (decrescente).
    # Caso base: se a lista tem 0 ou 1 elemento, já está ordenada
    if len(lista) <= 1:
        return lista

    # 1. Divisão
    meio = len(lista) // 2
    esquerda = merge_sort_pacientes(lista[:meio])
    direita = merge_sort_pacientes(lista[meio:])

    # 2. Conquista / Intercalação
    return _intercalar(esquerda, direita)


def _intercalar(esquerda, direita):
    # Combina duas sublistas ordenadas mantendo a ordem DECRESCENTE."""
    resultado = []
    i = j = 0

    # Compara o tempo_espera dos elementos das duas metades
    while i < len(esquerda) and j < len(direita):
        # Sinal de '>=' garante a ordem DECRESCENTE (maior tempo primeiro)
        if esquerda[i]["tempo_espera"] >= direita[j]["tempo_espera"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    # Anexa os elementos restantes de cada lado (se houver)
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado


# ------------------------------------------------------------------
# RELATÓRIO DO DIA UTILIZANDO O MERGE SORT
# ------------------------------------------------------------------
def relatorio_dia():
    total_cadastrados = sum(len(bucket) for bucket in pacientes)
    tamanho_real_fila = len(fila_espera) - len(desistentes)

    print("\n================ RELATÓRIO DO DIA ================")
    print(f" Total de pacientes cadastrados: {total_cadastrados}")
    print(f" Pacientes aguardando na fila : {tamanho_real_fila}")
    print(f" Total de pacientes atendidos : {len(pacientes_atendidos)}")
    print(f" Total de desistências         : {total_desistencias}")

    if pacientes_atendidos:
        # Cálculo da média
        total_tempo = sum(p["tempo_espera"] for p in pacientes_atendidos)
        media_tempo = total_tempo / len(pacientes_atendidos)
        print(f" Tempo médio de espera         : {media_tempo:.2f} eventos")

        # >>> AQUI O MERGE SORT É APLICADO <<<
        # A lista desordenada é passada para o Merge Sort, que retorna uma lista nova e ordenada
        atendidos_ordenados = merge_sort_pacientes(pacientes_atendidos)

        # Exibição dos dados organizados
        print(
            "\n--- Pacientes Atendidos (Ordenados por Maior Tempo de Espera) ---"
        )
        for pos, pac in enumerate(atendidos_ordenados, start=1):
            nome = pac["nome"]
            cpf_f = formatar_cpf(pac["cpf"])
            espera = pac["tempo_espera"]
            risco = pac["risco"]
            print(
                f"{pos}º | CPF: {cpf_f} | Nome: {nome:<20} | Risco: {risco} | Espera: {espera} eventos"
            )
    else:
        print(" Tempo médio de espera         : N/A (nenhum atendimento)")

    print("==================================================\n")


#Loop main do Codigo
while True:
    n: str = input(f'\nEscolha um opção abaixo:\n'
              '1 - Cadastrar novo paciente\n'
              '2 - Buscar paciente\n'
              '3 - Dar entrada na fila\n'
              '4 - Chamar próximo paciente\n'
              '5 - Desistir da fila de espera\n'
              '6 - Tamanho da fila de espera\n'
              '7 - Relatório do dia\n'
              '8 - Encerrar\n')
    match n :
        case "1":
            cpf: str = input(f'Informe o numero do CPF: ')
            cadastrar_paciente(cpf)
            print(f'{pacientes}')
        case "2":
            cpf: str = input(f'Informe o numero do CPF: ')
            buscar_paciente(cpf)
        case "3":
            cpf: str = input(f'Informe o numero do CPF: ')
            risco: str = input(f'Informe o nivel de risco: ')
            dar_entrada(cpf, risco)
        case "4":
            chamar_proximo()
        case "5":
            cpf: str = input(f'Informe o numero do CPF: ')
            desistir_fila(cpf)
        case "6":
            tamanho_fila_espera()
        case "7":
            relatorio_dia()
        case "8":
            break
        case _ :
            print('Opção invalida!')