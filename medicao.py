import random
from datetime import datetime

# ---------- Configurações da simulação ----------
CONSUMO_KW = {"ar_condicionado": 1.0, "umidificador": 0.05, "filtro": 0.03}  # kW de cada equipamento
MIN_POR_PASSO = 10      # cada passo da simulação representa 10 minutos
PASSO_TEMP = 1.0        # °C corrigidos por passo
PASSO_UMIDADE = 0.03    # 3 pontos percentuais por passo
PASSO_AR = 5            # pontos de IQAr por passo
HORA_INICIAL_MIN = 22 * 60  # o monitoramento começa às 22:00

NOMES = {"ar_condicionado": "Ar condicionado", "umidificador": "Umidificador", "filtro": "Filtro de ar"}


def _numero(valor, campo):
    try:
        return float(str(valor).replace("%", "").replace(",", ".").strip())
    except ValueError:
        raise ValueError(f"O campo {campo} precisa ser um número.") from None


def _br(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def hora_simulada(passos):
    t = (HORA_INICIAL_MIN + passos * MIN_POR_PASSO) % 1440
    return f"{t // 60:02d}:{t % 60:02d}"


# Tipo de pessoa (antes lia com input(); agora recebe os dados do formulário)
def dados_Pessoa(nome, idade, tempIdeal, tempIdeal2, umidadeIdeal, umidadeIdeal2, arLimite=50, tarifa=0.90):
    nome = str(nome).strip()
    if not nome:
        raise ValueError("Digite o seu nome.")
    idade = int(_numero(idade, "idade"))
    tmin = _numero(tempIdeal, "temperatura inicial")
    tmax = _numero(tempIdeal2, "temperatura final")
    umin = _numero(umidadeIdeal, "umidade inicial")
    umax = _numero(umidadeIdeal2, "umidade final")
    arLimite = _numero(arLimite, "limite de ar")
    tarifa = _numero(tarifa, "tarifa")

    if idade < 0:
        raise ValueError("Digite uma idade válida.")
    if tmin > tmax:
        raise ValueError("A temperatura inicial deve ser menor ou igual à final.")
    if umin < 0 or umax > 100 or umin > umax:
        raise ValueError("A umidade deve ficar entre 0% e 100%, com a inicial menor que a final.")
    if arLimite < 0 or tarifa < 0:
        raise ValueError("Limite de ar e tarifa não podem ser negativos.")

    return {
        "nome": nome,
        "idade": idade,
        "tempIdeal": tmin,
        "tempIdeal2": tmax,
        "umidadeIdeal": umin / 100,
        "umidadeIdeal2": umax / 100,
        "arLimite": arLimite,
        "tarifa": tarifa,
        # estado do quarto (preenchido por novo_cenario)
        "medicao": None, "inicial": None, "passos": 0, "estavel": False,
        "energia": {k: 0.0 for k in CONSUMO_KW}, "log": [], "historico": [],
    }


# Dados ficticios
def coletar_dados_medidos():
    umidade = random.randint(0, 100)
    ar = random.randint(0, 80)
    temperatura = round(random.uniform(15, 38), 1)
    horariomed = datetime.now().strftime("%d/%m/%y %H:%M:%S")  # horário da medição
    return {"umidade": umidade / 100, "ar": ar, "temperatura": temperatura, "horario": horariomed}


# Diagnóstico inicial: devolve as mensagens (antes eram print)
def verificarMedicoesMaisUsuario(medicao, usuario):
    msgs = []
    faixaT = f'{_br(usuario["tempIdeal"])}°C até {_br(usuario["tempIdeal2"])}°C'
    faixaU = f'{usuario["umidadeIdeal"] * 100:.0f}% até {usuario["umidadeIdeal2"] * 100:.0f}%'
    if medicao["temperatura"] < usuario["tempIdeal"]:
        msgs.append(f"Temperatura muito baixa. Ar condicionado ajustado para a faixa de {faixaT}.")
    if medicao["temperatura"] > usuario["tempIdeal2"]:
        msgs.append(f"Temperatura muito alta. Ar condicionado ajustado para a faixa de {faixaT}.")
    if medicao["umidade"] < usuario["umidadeIdeal"]:
        msgs.append(f"Umidade muito baixa. Umidificador ajustado para a faixa de {faixaU}.")
    if medicao["umidade"] > usuario["umidadeIdeal2"]:
        msgs.append(f"Umidade muito alta. Umidificador ajustado para a faixa de {faixaU}.")
    if medicao["ar"] > usuario["arLimite"]:
        msgs.append(f'Qualidade do ar acima de {usuario["arLimite"]:g}. Filtro de ar ligado.')
    return msgs


def _log(usuario, texto, tipo):
    usuario["log"].insert(0, {"hora": hora_simulada(usuario["passos"]), "texto": texto, "tipo": tipo})
    del usuario["log"][60:]


def novo_cenario(usuario):
    m = coletar_dados_medidos()
    usuario.update(medicao=m, inicial=dict(m), passos=0, estavel=False, log=[],
                   energia={k: 0.0 for k in CONSUMO_KW})
    _log(usuario, f'Novo cenário: {_br(m["temperatura"])} °C, {m["umidade"] * 100:.0f}% de umidade, IQAr {m["ar"]}', "novo")
    for msg in verificarMedicoesMaisUsuario(m, usuario):
        _log(usuario, msg, "acao")


# Um passo da simulação: cada equipamento corrige um pouco (1 passo = MIN_POR_PASSO min)
def ajustar_passo(usuario):
    m = usuario["medicao"]
    if m is None or usuario["estavel"]:
        return
    horas = MIN_POR_PASSO / 60
    gasto = {k: 0.0 for k in CONSUMO_KW}
    msgs = []

    if m["temperatura"] < usuario["tempIdeal"]:
        m["temperatura"] = round(min(m["temperatura"] + PASSO_TEMP, usuario["tempIdeal"]), 1)
        msgs.append(f'Ar condicionado aquecendo: {_br(m["temperatura"])} °C')
        gasto["ar_condicionado"] = CONSUMO_KW["ar_condicionado"] * horas
    elif m["temperatura"] > usuario["tempIdeal2"]:
        m["temperatura"] = round(max(m["temperatura"] - PASSO_TEMP, usuario["tempIdeal2"]), 1)
        msgs.append(f'Ar condicionado resfriando: {_br(m["temperatura"])} °C')
        gasto["ar_condicionado"] = CONSUMO_KW["ar_condicionado"] * horas

    if m["umidade"] < usuario["umidadeIdeal"]:
        m["umidade"] = round(min(m["umidade"] + PASSO_UMIDADE, usuario["umidadeIdeal"]), 2)
        msgs.append(f'Umidificador aumentando a umidade: {m["umidade"] * 100:.0f}%')
        gasto["umidificador"] = CONSUMO_KW["umidificador"] * horas
    elif m["umidade"] > usuario["umidadeIdeal2"]:
        m["umidade"] = round(max(m["umidade"] - PASSO_UMIDADE, usuario["umidadeIdeal2"]), 2)
        msgs.append(f'Umidificador reduzindo a umidade: {m["umidade"] * 100:.0f}%')
        gasto["umidificador"] = CONSUMO_KW["umidificador"] * horas

    if m["ar"] > usuario["arLimite"]:
        m["ar"] = max(m["ar"] - PASSO_AR, usuario["arLimite"])
        msgs.append(f'Filtro limpando o ar: IQAr {m["ar"]:g}')
        gasto["filtro"] = CONSUMO_KW["filtro"] * horas

    if not msgs:  # tudo dentro do ideal: encerra o cenário e guarda no histórico
        usuario["estavel"] = True
        if usuario["passos"] == 0:
            _log(usuario, "Nenhuma ação realizada. Todas as medições dentro do ideal.", "ok")
        else:
            _log(usuario, f'Todas as medições dentro do ideal após {usuario["passos"] * MIN_POR_PASSO} min. Equipamentos desligados.', "ok")
        energia = dict(usuario["energia"])
        usuario["historico"].insert(0, {"horario": m["horario"], "inicial": usuario["inicial"],
                                        "passos": usuario["passos"], "energia": energia, "kwh": sum(energia.values())})
    else:
        for k, v in gasto.items():
            usuario["energia"][k] += v
        usuario["passos"] += 1
        for t in msgs:
            _log(usuario, t, "acao")


def dispositivos(usuario):
    m = usuario["medicao"]
    if m is None:
        return {}
    t, u = m["temperatura"], m["umidade"]
    return {
        "ar_condicionado": "aquecendo" if t < usuario["tempIdeal"] else "resfriando" if t > usuario["tempIdeal2"] else None,
        "umidificador": "umidificando" if u < usuario["umidadeIdeal"] else "desumidificando" if u > usuario["umidadeIdeal2"] else None,
        "filtro": "filtrando" if m["ar"] > usuario["arLimite"] else None,
    }


def serializar(usuario):
    dados = dict(usuario)
    dados["kwh"] = sum(usuario["energia"].values())
    dados["total_kwh"] = sum(h["kwh"] for h in usuario["historico"])
    dados["minutos"] = usuario["passos"] * MIN_POR_PASSO
    dados["min_por_passo"] = MIN_POR_PASSO
    dados["hora"] = hora_simulada(usuario["passos"])
    dados["dispositivos"] = dispositivos(usuario)
    return dados


# Relatório com a soma de todos os cenários concluídos do usuário
def gerar_relatorio(usuario):
    H, R = usuario["historico"], usuario["tarifa"]
    if not H:
        return {"cenarios": 0}
    soma = {k: sum(h["energia"][k] for h in H) for k in CONSUMO_KW}
    kwh = sum(soma.values())
    minutos = sum(h["passos"] for h in H) * MIN_POR_PASSO
    equipamentos = [{"nome": NOMES[k], "kwh": v, "custo": v * R, "pct": (v / kwh * 100) if kwh else 0} for k, v in soma.items()]
    i_caro = max(range(len(H)), key=lambda i: H[i]["kwh"])
    caro = {"numero": len(H) - i_caro, "kwh": H[i_caro]["kwh"], "custo": H[i_caro]["kwh"] * R}
    media = kwh / len(H)

    linhas = [f'RELATÓRIO DE GASTOS - {usuario["nome"]} ({usuario["idade"]} anos)',
              f'Faixas: {_br(usuario["tempIdeal"])} a {_br(usuario["tempIdeal2"])} °C, umidade {usuario["umidadeIdeal"] * 100:.0f}% a {usuario["umidadeIdeal2"] * 100:.0f}%, filtro acima de IQAr {usuario["arLimite"]:g}',
              f"Cenários concluídos: {len(H)}",
              f"Tempo simulado de ajuste: {minutos // 60} h {minutos % 60:02d} min ({MIN_POR_PASSO} min por passo)", ""]
    linhas += [f'{e["nome"]}: {_br(e["kwh"], 2)} kWh | R$ {_br(e["custo"], 2)} | {_br(e["pct"])}%' for e in equipamentos]
    linhas += ["", f"TOTAL: {_br(kwh, 2)} kWh | R$ {_br(kwh * R, 2)} (tarifa R$ {_br(R, 2)}/kWh)",
               f'Média por cenário: {_br(media, 2)} kWh (R$ {_br(media * R, 2)}). Cenário mais caro: nº {caro["numero"]}, com {_br(caro["kwh"], 2)} kWh (R$ {_br(caro["custo"], 2)}).',
               "", "Cenários (do mais recente ao mais antigo):"]
    for i, h in enumerate(H):
        ini = h["inicial"]
        linhas.append(f'Nº {len(H) - i} | {h["horario"]} | início {_br(ini["temperatura"])} °C, {ini["umidade"] * 100:.0f}%, IQAr {ini["ar"]} | '
                      f'{h["passos"] * MIN_POR_PASSO} min | {_br(h["kwh"], 2)} kWh | R$ {_br(h["kwh"] * R, 2)}')

    return {"cenarios": len(H), "minutos": minutos, "kwh": kwh, "custo": kwh * R, "tarifa": R,
            "equipamentos": equipamentos, "media_kwh": media, "media_custo": media * R,
            "mais_caro": caro, "texto": "\n".join(linhas)}
