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

        usuario = {
            "nome": nome,
            "idade": idade,
            "tempIdeal": tempIdeal,
            "tempIdeal2": tempIdeal2,
            "umidadeIdeal": umidadeIdeal,
            "umidadeIdeal2": umidadeIdeal2
        }
        return usuario

    except Exception as erro:
        print(f"Não foi possível gerar o cadastro devido ao erro: {erro}. Verificar os dados informados.")

#Dados ficticios
def coletar_dados_medidos():
    umidade = random.randint(0,100)
    ar = random.randint(0,80)
    temperatura = round(random.uniform(15,38),1)

    #Registrar horario da medição
    horariomed = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    #dicionario com valores
    medicao = {
        "umidade": umidade,
        "ar": ar,
        "temperatura": temperatura,
        "horario": horariomed
    }
    return medicao


def verificarMedicoesMaisUsuario(medicao,usuario):
    #gambiarra
    controle = False

    if medicao["temperatura"] < usuario["tempIdeal"]:
        diferencaA = round(usuario["tempIdeal"] - medicao["temperatura"], 1)
        print(f'=Temperatura muito baixa. Aquecendo a sala em {diferencaA}°C, para ficar numa temperatura de {usuario["tempIdeal"]}°C até {usuario["tempIdeal2"]}°C')
        controle = True
    elif medicao["temperatura"] > usuario["tempIdeal2"]:
        diferencaA = round(medicao["temperatura"] - usuario["tempIdeal2"], 1)
        print(f'=Temperatura muito alta. Resfriando a sala em {diferencaA}°C, para ficar numa temperatura de {usuario["tempIdeal"]}°C até {usuario["tempIdeal2"]}°C')
        controle = True
    if medicao["umidade"] < usuario["umidadeIdeal"]:
        diferencaB = round(usuario["umidadeIdeal"] - medicao["umidade"], 1)
        print(f'=Umidade muito baixa. Umidificador ligado, ajustado em {diferencaB}, para a faixa de {usuario["umidadeIdeal"]}% até {usuario["umidadeIdeal2"]}%')
        controle = True
    elif medicao["umidade"] > usuario["umidadeIdeal2"]:
        diferencaB = round(medicao["umidade"] - usuario["umidadeIdeal2"], 1)
        print(f'=Umidade muito alta. Desumidificador ligado, ajustado em {diferencaB}, para a faixa de {usuario["umidadeIdeal"]}% até {usuario["umidadeIdeal2"]}%')
        controle = True
    if medicao["ar"] > 50:
        diferencaC = round(medicao["ar"] - 50, 1)
        print(f'=IQAr superior a 50 detectado. Ligando filtro de ar para reter poluentes. Expectativa: abaixar por, no minimo {diferencaC}IQAr.')
        controle = True
    if not controle:
        print("=Nenhuma ação realizada. Todas as medições dentro do ideal")
