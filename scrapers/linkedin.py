import requests
from bs4 import BeautifulSoup
from datetime import datetime

def search_linkedin(keyword, location="Remote"):
    print(f"Buscando '{keyword}' no LinkedIn...")
    jobs = []
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards:
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                link_elem = card.find('a', class_='base-card__full-link')
                
                if title_elem and company_elem and link_elem:
                    self_link = link_elem['href']
                    jobs.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "LinkedIn",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "link": self_link
                    })
            print(f"Encontradas {len(jobs)} vagas no LinkedIn.")
        else:
            print(f"Erro LinkedIn: {response.status_code}")
    except Exception as e:
        print(f"Falha LinkedIn: {e}")
    
    return jobs
