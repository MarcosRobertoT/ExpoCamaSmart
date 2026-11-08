print("Escolha uma opção:")
print("[1] - Cadastrar um novo usuário")
print("[2] - Gerar novo cenário para o usuário atual")
print(" ")
print("[c] - Encerrar programa")
print("[r] - Reabrir instruções")

while True:
  opcao = input(">Digite a opção desejada (1 ou 2): ")
  print("----------------------------------------------")

  if opcao == "1":
    usuario = dados_Pessoa()
    if usuario != None:
        print(f"\nUsuário {usuario['nome']} cadastrado com sucesso! Insira 2 do menu para gerar um cenario:\n")
    else:
        print("Erro. Não foi possivel cadastrar usuario")
  elif opcao == "2":
    if 'usuario' in globals() and usuario is not None:
        medicao = coletar_dados_medidos()
        print(f"\nGerando novo quarto para o usuário {usuario['nome']}\t")
        print(f"+Temperatura: {medicao['temperatura']} °C\t")
        print(f"+Umidade: {medicao['umidade']*100}%\t")
        print(f"+Qualidade do Ar: IQAr de {medicao['ar']}\t")
        verificarMedicoesMaisUsuario(medicao, usuario)
    else:
        print("\nErro: Nenhum usuário cadastrado ainda. Por favor, escolha a opção [1] para cadastrar pela primeira vez.")

  elif opcao.lower() == "c":
    print("Fechando console, obrigado pelo uso!")
    break
  elif opcao.lower() == "r":
    print("Escolha uma opção:")
    print(" [1] - Cadastrar um novo usuário")
    print(" [2] - Gerar novo cenário para o usuário atual")
    print("")
    print(" [r] - Reabrir instruções")
    print(" [c] - Encerrar programa")
  else:
    print("\nOpção inválida. Digite apenas 1 ou 2.")
