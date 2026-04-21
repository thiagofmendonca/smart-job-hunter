import requests
from bs4 import BeautifulSoup
from datetime import datetime

def search_indeed(keyword, location="Remote"):
    """
    Scraper simplificado para o Indeed.
    Nota: Indeed tem proteções fortes (Cloudflare). 
    Esta versão tenta acessar a versão de busca básica.
    """
    print(f"Buscando '{keyword}' no Indeed...")
    jobs = []
    # Versão internacional/BR dependendo da keyword ou locale
    url = f"https://br.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location}&from=searchOnHP"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # O Indeed muda classes frequentemente. Seletor comum: job_seen_beacon
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards:
                title_elem = card.find('h2', class_='jobTitle')
                company_elem = card.find('span', {'data-testid': 'company-name'})
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    company = company_elem.text.strip() if company_elem else "N/A"
                    link = "https://br.indeed.com" + link_elem['href']
                    
                    jobs.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "Indeed",
                        "title": title,
                        "company": company,
                        "link": link
                    })
            print(f"Encontradas {len(jobs)} vagas no Indeed.")
        else:
            # Frequentemente cai no 403 (Forbidden) devido ao Cloudflare
            print(f"Indeed retornou status {response.status_code} (Pode ser bloqueio de bot)")
    except Exception as e:
        print(f"Falha no Indeed: {e}")
    
    return jobs
