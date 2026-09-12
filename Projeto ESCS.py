#Projeto ESCS


#Variaveis
pacientes = []
fila_espera = []


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
    paciente_encontrado = None #Variavel de controle

    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        paciente_encontrado["risco"] = risco
        risco_atual = int(risco)

        print(f"Paciente {paciente_encontrado['nome']} adicionado à fila de espera com risco {risco}.")

        inserido = False
        for i in range(len(fila_espera)):
            if int(risco) < int(fila_espera[i]['risco']):  # Comparando o risco do paciente atual com os pacientes na fila
                fila_espera.insert(i, paciente_encontrado)
                inserido = True
                break

        if not inserido:
            fila_espera.append(paciente_encontrado)
            
        print(f"Fila de espera atualizada: {fila_espera}")

    else:
        print("Paciente ainda nao possui cadastro! Favor cadastrar o paciente abaixo antes de dar entrada na fila de espera.")
        cadastrar_paciente(cpf)
        




#Loop main do Codigo
while True:
    n = int(input(f'Escolha um opção abaixo:\n'
              '1 - Cadastrar CPF\n'
              '2 - Buscar CPF\n'
              '3 - Dar entrada na fila de espera\n'
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
        case 8:
            break
        case _ :
            print('Opção invalida!')
            n = 0
            break