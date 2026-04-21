import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def search_nerdin(keyword):
    """
    Scraper final para o Nerdin.com.br usando o atributo onclick do vaga-card.
    """
    print(f"Buscando '{keyword}' no Nerdin...")
    jobs = []
    url = f"https://www.nerdin.com.br/vagas.php?busca_vaga={keyword.replace(' ', '+')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # As vagas estão em divs com a classe vaga-card
            cards = soup.find_all('div', class_='vaga-card')
            
            for card in cards:
                # 1. Extrair link do atributo onclick="window.location.href='vaga_emprego/vaga-...'"
                onclick = card.get('onclick', '')
                match = re.search(r"window\.location\.href='(.*?)'", onclick)
                if not match:
                    continue
                
                rel_link = match.group(1)
                link = "https://www.nerdin.com.br/" + rel_link

                # 2. Extrair Título (Geralmente no primeiro h5 ou h2)
                title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                title = title_elem.get_text(strip=True) if title_elem else "Título não encontrado"

                # 3. Extrair Empresa
                # Procurando por classes comuns como vaga-empresa ou card-text
                company_elem = card.find(class_='vaga-empresa')
                if not company_elem:
                    company_elem = card.find('p', class_='card-text')
                
                company = "Empresa não informada"
                if company_elem:
                    # O Nerdin as vezes coloca ícones e textos extras, pegamos o texto limpo
                    company = company_elem.get_text(strip=True).split('|')[0]

                jobs.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "Nerdin",
                    "title": title,
                    "company": company,
                    "link": link
                })
            
            print(f"Encontradas {len(jobs)} vagas no Nerdin.")
        else:
            print(f"Erro Nerdin: {response.status_code}")
    except Exception as e:
        print(f"Falha no Nerdin: {e}")
    
    return jobs
