import requests
import hashlib
import os

# ===== CONFIGURAÇÕES =====
SITES_MONITORADOS = {
    "Nilson Imóveis": "https://www.nilsonimoveis.com/aluguel/apartamento/lavras/todos-os-bairros/todos-os-condominios/todas-as-opcoes/?valor_min=2.000,00&valor_max=2.500,00&pagina=1&ordenacao=desc",
    "Bertolucci Imóveis": "https://www.imobiliariabertolucci.com.br/aluguel/apartamento/lavras/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios?valorminimo=2.000,00&valormaximo=2.500,00&pagina=1",
    "Suli Imóveis": "https://www.suliimoveis.com.br/imoveis?cidade=1&tipo_imovel=2&negocio=Aluguel&bairro=0&quartos=0&banheiros=0&garagens=0&valor=2500.00&PropertyCode=",
    "Cap Paulo": "https://www.cappaulo.com.br/aluguel/apartamento/lavras/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios?valorminimo=2.000,00&valormaximo=2.500,00&pagina=1",
    "Remax Primus": "https://www.remax.com.br/listings?ListingClass=-1&TransactionTypeUID=-1&MacroPropertyTypeUIDs=2667&PriceMin=2000&PriceMax=+2500&OfficeID=86047",
    "Seu Lugar": "https://app.seulugar.imb.br/explore?city=Lavras&typeOfBusiness=LOCATION&category=RESIDENTIAL&maxPrice=3000",
    "Habitar": "https://habitarlavras.com.br/imovel?operacao=2&tipoimovel=9&imos_codigo=&empreendimento=&destaque=false&vlini=2000&vlfim=2500&exclusivo=false&cidade=2000&pais=1&filtropais=false&order=maxval&limit=9&page=0&ttpr_codigo=2",
    "Lavras Imóveis": "https://www.lavrasimoveismg.com.br/imoveis/listagem/?tipo_imovel=2&status=aluguel",
    "Lance Empreendimentos Imobiliários": "https://www.lanceempreendimentos.com.br/aluguel/apartamento/lavras/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios?valorminimo=2.000,00&valormaximo=2.500,00&areade=0&areaate=0&pagina=1",
    
}
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
ARQUIVO_ESTADO = "estado.txt"

def pegar_conteudo(url):
    r = requests.get(url, timeout=30)
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

def nome_arquivo_estado(nome_site):
    return f"estado_{nome_site.replace(' ', '_').lower()}.txt"
    
def main():
    for nome_site, url in SITES_MONITORADOS.items():
        conteudo = pegar_conteudo(url)
        hash_atual = hash_conteudo(conteudo)

        arquivo_estado = nome_arquivo_estado(nome_site)

        if os.path.exists(arquivo_estado):
            with open(arquivo_estado, "r") as f:
                hash_antigo = f.read().strip()
        else:
            hash_antigo = None

        if hash_antigo and hash_antigo != hash_atual:
            enviar_telegram(
                f"🚨 Novo imóvel detectado!\n\n"
                f"📍 {nome_site}\n"
                f"🔗 {url}"
            )

        with open(arquivo_estado, "w") as f:
            f.write(hash_atual)
            
if __name__ == "__main__":
    main()
