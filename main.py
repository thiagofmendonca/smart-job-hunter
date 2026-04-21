import pandas as pd
import os
from scrapers.linkedin import search_linkedin
from scrapers.indeed import search_indeed
from scrapers.nerdin import search_nerdin

class JobHunter:
    def __init__(self):
        self.all_jobs = []
        self.output_file = "jobs.csv"

    def run(self, keywords):
        for kw in keywords:
            # Busca em todas as fontes
            self.all_jobs.extend(search_linkedin(kw))
            self.all_jobs.extend(search_indeed(kw))
            self.all_jobs.extend(search_nerdin(kw))

        self.save_results()

    def save_results(self):
        if not self.all_jobs:
            print("Nenhuma vaga encontrada para salvar.")
            return

        df = pd.DataFrame(self.all_jobs)
        
        # Remover duplicatas baseadas no link
        if os.path.exists(self.output_file):
            old_df = pd.read_csv(self.output_file)
            df = pd.concat([old_df, df]).drop_duplicates(subset=['link'], keep='first')
        
        df.to_csv(self.output_file, index=False)
        print(f"Total de {len(df)} vagas únicas salvas em {self.output_file}")

if __name__ == "__main__":
    hunter = JobHunter()
    # Keywords focadas no seu perfil
    target_keywords = ["Linux", "Python Automation", "Suporte Técnico"]
    
    hunter.run(target_keywords)
