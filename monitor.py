import requests
import hashlib
import os

# ===== CONFIGURAÇÕES =====
URL_MONITORADA = "https://www.nilsonimoveis.com/aluguel/apartamento/lavras/todos-os-bairros/todos-os-condominios/todas-as-opcoes/?valor_min=2.000,00&valor_max=2.500,00&pagina=1&ordenacao=desc"
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
ARQUIVO_ESTADO = "estado.txt"

def pegar_conteudo():
    r = requests.get(URL_MONITORADA, timeout=30)
    r.raise_for_status()
    return r.text

def hash_conteudo(conteudo):
    return hashlib.md5(conteudo.encode("utf-8")).hexdigest()

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload, timeout=30)

def main():
    conteudo = pegar_conteudo()
    hash_atual = hash_conteudo(conteudo)

    if os.path.exists(ARQUIVO_ESTADO):
        with open(ARQUIVO_ESTADO, "r") as f:
            hash_antigo = f.read().strip()
    else:
        hash_antigo = None

    if hash_antigo and hash_antigo != hash_atual:
        enviar_telegram(
            "🚨 Novo imóvel detectado!\n\nConfira:\n" + URL_MONITORADA
        )

    with open(ARQUIVO_ESTADO, "w") as f:
        f.write(hash_atual)
if __name__ == "__main__":
    main()
