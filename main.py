from medicao import coletar_dados_medidos, dados_Pessoa, verificarMedicoesMaisUsuario
from repositorio import salvar_med

def main():
    pessoa = dados_Pessoa()

    dados = coletar_dados_medidos()

    verificarMedicoesMaisUsuario(dados,pessoa)

    #mostrar_dados(dados)
    #salvar_med(dados)

if __name__ == "__main__":
    main()