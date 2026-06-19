FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.14-dev AS builder

COPY requirements.txt .

USER root

RUN python3 -m venv .venv
ENV PATH=/.venv/bin:$PATH
RUN source .venv/bin/activate
RUN pip3 install -r requirements.txt


FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.14 AS runner

COPY . .

COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"


EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

WORKDIR /app


ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]