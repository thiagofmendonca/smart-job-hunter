# Smart Job Hunter Bot 🤖

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)

Automação para rastreamento de vagas de emprego em diversas plataformas (LinkedIn, Indeed, etc.), focada em posições remotas de TI.

---

## 🇺🇸 English Version
This project automates the job search process by scanning multiple platforms for specific keywords like "Remote Linux Support" and "Python Automation".

### Key Features
- **Keyword-based scanning:** Targets specific roles across multiple sources.
- **Remote Filter:** Prioritizes global remote positions.
- **Export to CSV:** Automatically saves new findings.

---

## 🇧🇷 Versão em Português
Este projeto automatiza o rastreamento de vagas de emprego, buscando termos como "Suporte Linux Remoto" e "Automação Python".

### Principais Funcionalidades
- **Busca por Palavras-chave:** Varredura em múltiplas fontes.
- **Filtro de Remoto:** Prioriza posições globais remotas.
- **Exportação CSV:** Salva as novas vagas em um arquivo organizado.

---

## 🛠️ Tech Stack
- **Python 3.x**
- **Libraries:** `requests`, `beautifulsoup4`, `pandas`, `python-dotenv`

## 📁 Estrutura
- `main.py`: Motor principal.
- `scrapers/`: Módulos de extração (planejado).
- `jobs.csv`: Onde os resultados são salvos.
