import random
from datetime import datetime

#Tipo de pessoa
def dados_Pessoa():
    try:
        nome = input("Digite o seu Nome: ")
        idade = int(input("Digite a sua idade: "))
        tempIdeal = float(input(f"{nome}, Qual a faixa de temperatura você considera ideal para dormir?\nInsira o valor (em número) inicial: "))
        tempIdeal2 = float(input(f"Insira o valor (em número) final: "))
        umidadeIdeal = float(input(f"{nome}, qual faixa de umidade ideal para você dormir?\nInsira o valor em porcentagem (Exemplo: 20%,30%) inicial: ").replace("%",""))
        umidadeIdeal2 = float(input(f"Insira o valor em porcentagem (exemplo 20%, 30%) final: ").replace("%",""))

        umidadeIdeal = umidadeIdeal/100
        umidadeIdeal2 = umidadeIdeal2 / 100

        usuario = {
            "nome": nome,
            "idade": idade,
            "tempIdeal": tempIdeal,
            "tempIdeal2": tempIdeal2,
            "umidadeIdeal": umidadeIdeal,
            "umidadeIdeal2": umidadeIdeal2
        }
        print(usuario)
        return usuario

    except Exception as erro:
        print(f"Não foi possível gerar o cadastro devido ao erro: {erro}. Verificar os dados informados.")

#Dados ficticios
def coletar_dados_medidos():
    umidade = random.randint(0,100)
    ar = random.randint(0,80)
    temperatura = round(random.uniform(15,38),1)

    #Registrar horario da medição
    horariomed = datetime.now()#.strftime("%d/%h/%y %H:%M:%S")

    #dicionario com valores
    medicao = {
        "umidade": umidade/100,
        "ar": ar,
        "temperatura": temperatura,
        "horario": horariomed
    }
    print(medicao)
    return medicao


def verificarMedicoesMaisUsuario(medicao,usuario):
    #gambiarra
    controle = False

    if medicao["temperatura"] < usuario["tempIdeal"]:
        print(f'Temperatura muito baixa. Ar condicionado ajustado para a faixa de {usuario["tempIdeal"]}°C até {usuario["tempIdeal2"]}°C')
        controle = True
    if medicao["temperatura"] > usuario["tempIdeal2"]:
        print(f'Temperatura muito alta. Ar condicionado ajustado para a faixa de {usuario["tempIdeal"]}°C até {usuario["tempIdeal2"]}°C')
        controle = True
    if medicao["umidade"] < usuario["umidadeIdeal"]:
        print(f'Umidade muito baixa. Umidificador ajustado para a faixa de {usuario["umidadeIdeal"]*100}% até {usuario["umidadeIdeal2"]*100}%')
        controle = True
    if medicao["umidade"] > usuario["umidadeIdeal"]:
        print(f'Umidade muito alta. Umidificador ajustado para a faixa de {usuario["umidadeIdeal"]*100}% até {usuario["umidadeIdeal2"]*100}%')
        controle = True
    if medicao["ar"] > 50:
        print("Qualidade do Ar acima de 50. Filtro de ar ligado")
        controle = True
    if not controle:
        print("Nenhuma ação realizada. Todas as medições dentro do ideal")