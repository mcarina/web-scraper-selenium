import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Função para buscar no Google e extrair resultados
def buscar_google(termo):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa em segundo plano
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evita bloqueios
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # Cabeçalho de navegador comum
    service = Service(ChromeDriverManager().install())

    driver = None  # Inicializa driver para garantir que sempre seja fechado
    try:
        driver = webdriver.Chrome(service=service, options=options)

        print(f"[INFO] Buscando por: {termo}")
        driver.get("https://www.google.com/")

        # Esperar campo de pesquisa aparecer
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(termo)
        search_box.send_keys(Keys.RETURN)

        # Espera carregar os resultados
        time.sleep(3)

        # Obter HTML da página
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("div.tF2Cxc a")

        if not results:
            print("[ERRO] Nenhum resultado encontrado. O Google pode estar bloqueando.")
            return []

        # Extrair até 5 resultados
        lojas = [{"nome": result.get_text(), "link": result["href"]} for result in results[:5]]

        print(f"[INFO] {len(lojas)} resultado(s) encontrado(s).")
        return lojas

    except Exception as e:
        print(f"[ERRO] Ocorreu um erro na busca: {e}")
        return []

    finally:
        if driver:
            driver.quit()
