# Copyright (C) 2026 Thiago Faria Mendonça
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import os
from urllib.parse import urlparse, urlunparse
from scrapers.linkedin import search_linkedin
from scrapers.indeed import search_indeed
from scrapers.nerdin import search_nerdin

class JobHunter:
    def __init__(self):
        self.all_jobs = []
        self.output_file = "jobs.csv"

    def clean_url(self, url):
        """
        Remove parâmetros de rastreamento das URLs para evitar duplicatas 'falsas'.
        Ex: .../view/123?refId=abc -> .../view/123
        """
        parsed = urlparse(url)
        # Mantém apenas o esquema, netloc e path (remove query e fragmentos)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    def run(self, keywords):
        for kw in keywords:
            self.all_jobs.extend(search_linkedin(kw))
            self.all_jobs.extend(search_indeed(kw))
            self.all_jobs.extend(search_nerdin(kw))

        # Limpar URLs de todas as vagas encontradas nesta rodada
        for job in self.all_jobs:
            job['link'] = self.clean_url(job['link'])

        self.save_results()

    def save_results(self):
        if not self.all_jobs:
            print("Nenhuma vaga encontrada para salvar.")
            return

        new_df = pd.DataFrame(self.all_jobs)
        
        if os.path.exists(self.output_file):
            existing_df = pd.read_csv(self.output_file)
            # Garante que as URLs existentes também estejam limpas (caso o CSV seja antigo)
            existing_df['link'] = existing_df['link'].apply(self.clean_url)
            
            # Combina e remove duplicatas baseadas no link limpo
            # keep='first' mantém a data da primeira vez que a vaga foi vista
            combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['link'], keep='first')
            
            new_records = len(combined_df) - len(existing_df)
            print(f"✨ {new_records} novas vagas únicas adicionadas.")
            final_df = combined_df
        else:
            final_df = new_df.drop_duplicates(subset=['link'], keep='first')
            print(f"📁 Criado novo arquivo com {len(final_df)} vagas únicas.")
        
        final_df.to_csv(self.output_file, index=False)
        print(f"📊 Total acumulado no banco de dados: {len(final_df)} vagas.")

if __name__ == "__main__":
    hunter = JobHunter()
    target_keywords = ["Linux", "Python Automation", "Suporte Técnico"]
    hunter.run(target_keywords)
