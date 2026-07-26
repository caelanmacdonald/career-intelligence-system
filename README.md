\# Career Intelligence Dashboard



A Python and PostgreSQL application for managing a structured job search.



Rather than relying on spreadsheets and browser bookmarks, this project stores employers, vacancies and applications in a relational database and provides command-line tools for managing the entire application process.



\---



\## Features



\- Import Skilled Worker sponsor data into PostgreSQL

\- Curate a list of target employers

\- Track employer review history

\- Open careers pages directly from PowerShell

\- Store and manage vacancies

\- Track job applications

\- Analyse progress with SQL and Power BI (planned)



\---



\## Technology



\- Python 3

\- PostgreSQL (Neon)

\- psycopg

\- SQL

\- Power BI

\- Git \& GitHub



\---



\## Project Structure



```

career-intelligence-dashboard/



├── python/

│   ├── db.py

│   ├── import_target_employers.py

│   ├── enrich_employers.py

│   ├── check_jobs.py

│   ├── add_vacancy.py

│   ├── list_vacancies.py

│   ├── add_application.py

│   └── ...

│

├── sql/

│   ├── schema.sql

│   ├── analysis_queries.sql

│   └── test_queries.sql

│

├── data/

│   ├── target_companies.csv

│   └── employer_links.csv

│

├── README.md

└── .env

```



\---



\## Database



Current entities:



```

Target Employers

             │

             ▼

Vacancies

             │

             ▼

Applications

             │

             ▼

Application Events

```



\---



\## Typical Workflow



\### 1. Import employers



```powershell

python .\python\import_target_employers.py

```



\### 2. Review employers



```powershell

python .\python\check_jobs.py

```



\### 3. Save vacancies



```powershell

python .\python\add_vacancy.py

```



\### 4. Review vacancies



```powershell

python .\python\list_vacancies.py

```



\---



\## Planned Features



\- Automatic careers page enrichment

\- Vacancy scraping/API integration

\- Daily employer review queue

\- Power BI reporting

\- Interview tracking

\- Application success metrics

\- Email notifications

\- Skills-to-job matching



\---



\## Motivation



This project was created to solve a real problem: managing a large job search targeting UK Skilled Worker sponsor organisations.



It also serves as a portfolio project demonstrating:



\- relational database design

\- SQL

\- Python automation

\- ETL workflows

\- command-line application development

\- data modelling

\- business intelligence concepts



\---

