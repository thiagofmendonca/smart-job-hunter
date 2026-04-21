import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

class JobHunter:
    def __init__(self):
        self.jobs = []
        self.output_file = "jobs.csv"

    def search_linkedin(self, keyword, location="Remote"):
        """
        Exemplo simples de busca no LinkedIn (URL pública).
        Nota: O LinkedIn bloqueia scrapers facilmente. 
        Em um ambiente real, APIs como SerpApi são preferíveis.
        """
        print(f"Buscando '{keyword}' em '{location}' no LinkedIn...")
        # URL de busca pública simplificada
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
                    title = card.find('h3', class_='base-search-card__title').text.strip()
                    company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                    link = card.find('a', class_='base-card__full-link')['href']
                    
                    self.jobs.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "LinkedIn",
                        "title": title,
                        "company": company,
                        "link": link
                    })
                print(f"Encontradas {len(job_cards)} vagas no LinkedIn.")
            else:
                print(f"Erro ao acessar LinkedIn: Status {response.status_code}")
        except Exception as e:
            print(f"Falha no scraper do LinkedIn: {e}")

    def save_results(self):
        if not self.jobs:
            print("Nenhuma vaga encontrada para salvar.")
            return

        df = pd.DataFrame(self.jobs)
        if os.path.exists(self.output_file):
            df.to_csv(self.output_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.output_file, index=False)
        print(f"Resultados salvos em {self.output_file}")

if __name__ == "__main__":
    hunter = JobHunter()
    # Exemplo de keywords
    keywords = ["Linux Remote", "Python Automation"]
    
    for kw in keywords:
        hunter.search_linkedin(kw)
    
    hunter.save_results()
