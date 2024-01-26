FROM jupyter/base-notebook:python-3.9.7
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r  requirements.txt
COPY . .

USER root
COPY start-notebook.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-notebook.sh
USER $NB_USER

ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

