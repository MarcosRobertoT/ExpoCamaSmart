from connector import conectar

#Não rodar. Tem que atualizar a tabela
def salvar_med(dados):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """INSERT INTO medicoes (
            horario,
            batimento,
            respiracao,
            temperatura,
            origem_dados       
        )
        VALUES (%s, %s, %s, %s, %s)
        """
        valores =(
            dados["horario"],
            dados["batimentos"],
            dados["respiração"],
            dados["temperatura"],
            "SIMULAÇÃO"
        )

        cursor.execute(sql,valores)
        conexao.commit()

        print("Medição salva no banco de dados")
    except Exception:
        if conexao is not None:
            conexao.rollback()
            print("Erro no registro no banco de dados. Rollback aplicado!")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()