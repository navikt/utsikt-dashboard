# Dashbord om beregninger fra Oppdragssystemet

# Run on local machine
```
cd app
streamlit run main.py
```
Obs! Working directory needs to be **/app** directory. 

# Dockerfile
To build the Dockerfile:
```
docker build -t utsikt_dashboard/test .
```

To run the Dockerfile:
```
docker run -p 8501:8501 utsikt_dashboard/test:latest 
```

### sqlfluff
Vi bruker pakka [sqlfluff](https://docs.sqlfluff.com/en/stable/index.html) for å formattere sql-koden. For å installere:

`uv add --dev sqlfluff`

For å linte sql-spørringer, kjør `sqlfluff lint app/queries`

# The app
The application has the following ingress: https://utsikt-dashboard.ansatt.dev.nav.no/