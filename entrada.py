from medicao import dados_Pessoa, coletar_dados_medidos, verificarMedicoesMaisUsuario
import gspread
from google.auth import default

def iniciador():

    global usuario

    print("Escolha uma opção:")
    print("[1] - Cadastrar um novo usuário")
    print("[2] - Gerar novo cenário para o usuário atual")
    print(" ")
    print("[c] - Encerrar programa")

    while True:

        opcao = input(">Digite a opção desejada: ")
        print("----------------------------------------------")

        if opcao == "1":
            usuario = dados_Pessoa()
            print(f"\nUsuário {usuario['nome']} cadastrado com sucesso! Insira 2 do menu para gerar um cenario:\n")
        elif opcao == "2":
            if 'usuario' in globals() and usuario is not None:
                medicao = coletar_dados_medidos()
                print(f"\nGerando novo quarto para o usuário {usuario['nome']}\t")
                print(f"+Temperatura: {medicao['temperatura']} °C\t")
                print(f"+Umidade: {medicao['umidade']*100}%\t")
                print(f"+Qualidade do Ar: IQAr de {medicao['ar']}\t")
                verificarMedicoesMaisUsuario(medicao, usuario)

                print("Escolha uma opção:")
                print(" [1] - Cadastrar um novo usuário")
                print(" [2] - Gerar novo cenário para o usuário atual")
                print(" [c] - Encerrar programa")

            else:
                print("\nErro: Nenhum usuário cadastrado ainda. Por favor, escolha a opção [1] para cadastrar pela primeira vez.")

        elif opcao.lower() == "c":
            print("Fechando console, obrigado pelo uso!")
            break
        else:
            print("\nOpção inválida. Digite uma válida.")
