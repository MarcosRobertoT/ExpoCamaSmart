import random
from datetime import datetime

#Dados ficticios
def coletar_dados_medidos():
    batimentos = random.randint(60,100)
    respiracao = random.randint(12,20)
    temperatura = round(random.uniform(35.6,38.7),1)

    #Registrar horario da medição
    horariomed = datetime.now()#.strftime("%d/%h/%y %H:%M:%S")

    #dicionario com valores
    medicao = {
        "batimentos": batimentos,
        "respiração": respiracao,
        "temperatura": temperatura,
        "horario": horariomed
    }
    return medicao

def mostrar_dados(medicao):
    print("#### Dados Coletados #####")
    print(f'Horário da Medição: {medicao["horario"]}')
    print(f'Batimentos: {medicao["batimentos"]} BPM')
    print(f'Respiração: {medicao["respiração"]} por minuto')
    print(f'Temperatura: {medicao["temperatura"]}°C')
