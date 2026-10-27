from medicao import mostrar_dados, coletar_dados_medidos
from repositorio import salvar_med

def main():

    dados = coletar_dados_medidos()

    mostrar_dados(dados)
    salvar_med(dados)

if __name__ == "__main__":
    main()