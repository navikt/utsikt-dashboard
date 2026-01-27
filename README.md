# Test av streamlit
Det som testes er:

* Deploye til dev-gvp cluster :white_check_mark:

* Henting av dev data fra BQ

* Visuliseringer av dataen

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

# The app
The application has the following ingress: https://utsikt-dashboard.ansatt.dev.nav.no/