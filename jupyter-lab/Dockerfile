FROM python:3.10-slim

WORKDIR /workspace

RUN pip install --no-cache-dir \
    jupyterlab \
    mlflow \
    pandas \
    scikit-learn

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]