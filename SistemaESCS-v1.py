#Variaveis
pacientes = []
fila_espera = []
pacientes_atendidos = []
contador_eventos = 0

#Funcao para formatar a data
def formatar_date(data):
    return f"{data[:2]}/{data[2:4]}/{data[4:]}"

#Funcao para formatar o Cpf
def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"



# 1 - Funcao para cadastro de novos pacientes
def cadastrar_paciente(cpf):

    paciente_encontrado = None

    for paciente in pacientes:
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
    else:
        nome: str = input(f'Informe o nome do paciente:')
        data: str = input(f'Informe a data de nascimento do paciente:')
        pacientes.append({"cpf": cpf, "nome": nome, "data": data})
        cpf_f = formatar_cpf(cpf)
        data_f = formatar_date(data)
        print(f"CPF: {cpf_f} | Nome: {nome} | Data: {data_f}")

# 2 - Funcao Buscar Paciente
def buscar_paciente(cpf):
    paciente_encontrado = None

    for paciente in pacientes:
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
    else:
        print("Paciente ainda nao possui cadastro!")

# 3 - Funcao para dar entrada do paciente na fila de espera
def dar_entrada(cpf, risco):
    global contador_eventos

    paciente_encontrado = None #Variavel de controle
    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if not paciente_encontrado:
        print("Paciente ainda não possui cadastro. Cadastrando novo paciente...")
        cadastrar_paciente(cpf)
        # Rebusca o paciente que acabou de ser cadastrado
        for paciente in pacientes:
            if paciente["cpf"] == cpf:
                paciente_encontrado = paciente
                break

# Registra o evento de entrada e adiciona à fila
    if paciente_encontrado:
        contador_eventos += 1  # Incrementa o contador de eventos

    # Cria uma cópia para colocar na fila com as informações da consulta atual
    paciente_fila = paciente_encontrado.copy()
    paciente_fila["risco"] = risco
    paciente_fila["evento_entrada"] = (contador_eventos)  # Garante que a chave é criada

    inserido = False
    for i in range(len(fila_espera)):
        if int(risco) < int(fila_espera[i]["risco"]):
            fila_espera.insert(i, paciente_fila)
            inserido = True
            break

    if not inserido:
        fila_espera.append(paciente_fila)

    print(
        f"Paciente {paciente_fila['nome']} adicionado à fila no evento nº {contador_eventos} com risco {risco}."
    )

# 4 - Funcao para chamar proximop nome da lista de espera
def chamar_proximo():
    global contador_eventos

    if fila_espera:
        contador_eventos += 1
        proximo_paciente = fila_espera.pop(0)

        evento_entrada = proximo_paciente.get("evento_entrada", contador_eventos)
        tempo_espera_eventos = contador_eventos - evento_entrada

        proximo_paciente["tempo_espera"] = tempo_espera_eventos
        pacientes_atendidos.append(proximo_paciente)

        print(f"Chamando próximo paciente: {proximo_paciente['nome']} com risco {proximo_paciente['risco']}.\n")
        print(f"Tempo de espera do paciente: {tempo_espera_eventos} eventos.\n")

    else:
        print("Não há pacientes na fila de espera. Favor dar entrada na fila de espera antes de chamar o próximo paciente.\n")

# 5 - Funcao para remover pacientes da lista de espera
def desistir_fila(cpf):
    paciente_encontrado = None #Variavel de controle

    for paciente in fila_espera:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break
    if paciente_encontrado:
        fila_espera.remove(paciente_encontrado)
        print(f"Paciente {paciente_encontrado['nome']} removido da fila de espera com sucesso.")
    else:
        print("Paciente não encontrado na fila de espera.")


# 6 - Funcao para apresentar o tamanho da fila
def tamanho_fila_espera():
    print(f"Tamanho da fila de espera: {len(fila_espera)}")

# 7 - Funcao do relatorio do dia
def relatorio_dia():
    print("Relatório do dia:\n")
    print(f"Total de pacientes cadastrados: {len(pacientes)}\n")
    print(f"Total de pacientes na fila de espera: {len(fila_espera)}\n")
    print(f"Total de pacientes atendidos: {len(pacientes_atendidos)}\n")


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
