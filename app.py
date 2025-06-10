import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# Configuração do Selenium com o Chrome
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # roda em segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()  # Use o caminho do chromedriver se necessário
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Função para extrair os dados de uma página
def extrair_dados_html(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    noticias = soup.select("li.searchResults")
    for noticia in noticias:
        titulo_tag = noticia.select_one("h2")
        data_tag = noticia.select_one("span.discreet")
        link_tag = noticia.select_one("a")

        titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""
        data = data_tag.get_text(strip=True) if data_tag else ""
        link = link_tag["href"] if link_tag else ""

        resultados.append({
            "Título": titulo,
            "Data": data,
            "Link": link
        })

    return resultados

# Função principal que percorre todas as páginas
def coletar_todas_noticias():
    url_base = "https://www.gov.br/pf/pt-br/search?origem=form&SearchableText=licita%C3%A7%C3%A3o"
    driver = iniciar_driver()
    todas_noticias = []

    # 830 resultados / 30 por página = 28 páginas (b_start:int vai de 0 até 810 de 30 em 30)
    for inicio in range(0, 831, 30):
        print(f"Coletando página com início em: {inicio}")
        url = url_base.format(inicio)
        driver.get(url)
        time.sleep(2)  # Espera o conteúdo carregar
        html = driver.page_source
        noticias = extrair_dados_html(html)
        todas_noticias.extend(noticias)

    driver.quit()
    return todas_noticias

# Execução
if __name__ == "__main__":
    noticias = coletar_todas_noticias()
    df = pd.DataFrame(noticias)
    df.to_csv("noticias_pf_licitacao.csv", index=False, encoding='utf-8-sig')
    print("Coleta finalizada! Total de notícias:", len(df))
