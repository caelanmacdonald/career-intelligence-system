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

│   ├── import\_target\_employers.py

│   ├── enrich\_employers.py

│   ├── check\_jobs.py

│   ├── add\_vacancy.py

│   ├── list\_vacancies.py

│   ├── add\_application.py

│   └── ...

│

├── sql/

│   ├── schema.sql

│   ├── analysis\_queries.sql

│   └── test\_queries.sql

│

├── data/

│   ├── target\_companies.csv

│   └── employer\_links.csv

│

├── README.md

└── .env

```



\---



\## Database



Current entities:



```

Target Employers

&#x20;       │

&#x20;       ▼

Vacancies

&#x20;       │

&#x20;       ▼

Applications

&#x20;       │

&#x20;       ▼

Application Events

```



\---



\## Typical Workflow



\### 1. Import employers



```powershell

python .\\python\\import\_target\_employers.py

```



\### 2. Review employers



```powershell

python .\\python\\check\_jobs.py

```



\### 3. Save vacancies



```powershell

python .\\python\\add\_vacancy.py

```



\### 4. Review vacancies



```powershell

python .\\python\\list\_vacancies.py

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

