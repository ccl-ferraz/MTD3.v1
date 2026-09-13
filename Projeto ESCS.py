#Projeto ESCS


#Variaveis
pacientes = []
fila_espera = []
pacientes_atendidos = []
contador_eventos = 0


#Metodo para cadastrar novos pacientes
def cadastrar_paciente(cpf):
    cpf_ex = False
    for i in range(len(pacientes)):
        if pacientes[i]["cpf"] == cpf:
            cpf_ex = True
            print(f'O CPF informado já possui cadastro no sistema')
            print(cpf)

        if not cpf_ex:
            cpf: str = input(f'Informe o numero do CPF: ')
            formatar_cpf(cpf)
            name: str = input(f'Informe o nome do paciente:')
            data: str = input(f'Informe a data de nascimento do paciente:')
            formatar_date(data)
            pacientes.append({"cpf": cpf, "nome": name, "data": data})
            print(cpf, name, data)

#Loop main (possibilita armazenar os Cpfs sem perde-los)
#Funcao para formatar o Cpf
def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

#Funcao para formatar a data
def formatar_date(data):
    return f"{data[:2]}/{data[2:4]}/{data[4:]}"

#Funcao Buscar Paciente
def buscar_paciente(cpf):
    paciente_encontrado = None #Variavel de controle

    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        print("Paciente encontrado com sucesso!")
        print(f"CPF: {formatar_cpf(paciente_encontrado['cpf'])} | Nome: {paciente_encontrado['nome']} | Data: {formatar_date(paciente_encontrado['data'])}")
    else:
        print("Paciente ainda nao possui cadastro!")


#Funcao para cadastro de novos pacientes
def cadastrar_paciente(cpf):
    paciente_encontrado = None #Variavel de controle

    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        print("Paciente ja possui cadastro!")
        print(f"CPF: {paciente_encontrado['cpf']} | Nome: {paciente_encontrado['nome']} | Data: {paciente_encontrado['data']}")
    else:
        nome: str = input(f'Informe o nome do paciente:')
        data: str = input(f'Informe a data de nascimento do paciente:')
        pacientes.append({"cpf": cpf, "nome": nome, "data": data})
        cpf_f = formatar_cpf(cpf)
        data_f = formatar_date(data)
        print(f"CPF: {cpf_f} | Nome: {nome} | Data: {data_f}")

#Funcao para dar entrada do paciente na fila de espera
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

def tamanho_fila_espera():
    print(f"Tamanho da fila de espera: {len(fila_espera)}")

def relatorio_dia():
    print("Relatório do dia:\n")
    print(f"Total de pacientes cadastrados: {len(pacientes)}\n")
    print(f"Total de pacientes na fila de espera: {len(fila_espera)}\n")
    print(f"Total de pacientes atendidos: {len(pacientes_atendidos)}\n")

    if pacientes_atendidos:
        atendidos_ordenados = pacientes_atendidos.copy()
        n = len(atendidos_ordenados)

        for i in range(n):
            for j in range(0, n-i-1):
                if atendidos_ordenados[j]["tempo_espera"] < atendidos_ordenados[j+1]["tempo_espera"]:
                    atendidos_ordenados[j], atendidos_ordenados[j+1] = atendidos_ordenados[j+1], atendidos_ordenados[j]
        print("\nPacientes atendidos (Tempo de espera decrescente):\n")
        for p in atendidos_ordenados:
            print(f"Nome: {p['nome']} | CPF: {formatar_cpf(p['cpf'])} | Tempo de espera: {p['tempo_espera']} eventos")



#Loop main do Codigo
while True:
    n = int(input(f'Escolha um opção abaixo:\n'
              '1 - Cadastrar CPF\n'
              '2 - Buscar CPF\n'
              '3 - Dar entrada na fila de espera\n'
              '4 - Chamar próximo paciente\n'
              '5 - Desistir da fila de espera\n'
              '6 - Tamanho da fila de espera\n'
              '7 - Relatório do dia\n'
              '8 - Encerrar\n'))
    match n :
        case 1:
            cpf: str = input(f'Informe o numero do CPF: ')
            cadastrar_paciente(cpf)
            print(f'{pacientes}')
        case 2:
            cpf: str = input(f'Informe o numero do CPF: ')
            buscar_paciente(cpf)
        case 3:
            cpf: str = input(f'Informe o numero do CPF: ')
            risco: str = input(f'Informe o nivel de risco: ')
            dar_entrada(cpf, risco)
        case 4:
            chamar_proximo()
        case 5:
            cpf: str = input(f'Informe o numero do CPF: ')
            desistir_fila(cpf)
        case 6:
            tamanho_fila_espera()
        case 7:
            relatorio_dia()
        case 8:
            break
        case _ :
            print('Opção invalida!')
            n = 0
            break