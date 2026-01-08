# Test av streamlit
Det som testes er:

*[ ] Deploye til dev-gvp cluster
*[ ] Henting av dev data fra BQ
*[ ] Visuliseringer av dataen

# Dockerfile
To build the Dockerfile:
```
docker build -t utsikt_dashboard/test .
```

To run the Dockerfile:
```
docker run -p 8501:8501 utsikt_dashboard/test:latest 
```