# Dashbord om beregninger fra Oppdragssystemet

# Kjør appen lokalt
```
cd app
streamlit run main.py
```
Obs! Working directory needs to be **/app** directory. 

# Dockerfile
For å bygge Dockerfile:
```
docker build -t utsikt_dashboard/test .
```

For å kjøre Dockerfile:
```
docker run -p 8501:8501 utsikt_dashboard/test:latest 
```

### sqlfluff
Vi bruker pakka [sqlfluff](https://docs.sqlfluff.com/en/stable/index.html) for å formattere sql-koden. For å installere:

`uv add --dev sqlfluff`

For å linte sql-spørringer, kjør `sqlfluff lint app/queries`

# Applikasjonen
Applikasjonen har følgende ingress: https://utsikt-dashboard.ansatt.dev.nav.no/


---

## Henvendelser

Enten:
Spørsmål knyttet til koden eller repositoryet kan stilles som issues her på GitHub

 
### For Nav-ansatte

Interne henvendelser kan sendes via Slack i kanalen #team-utsikt.