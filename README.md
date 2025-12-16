# ЛР4 — More Kubernetes (JupyterLab + MLflow)

В этой лабораторной развернута связка из **2 сервисов** в Kubernetes:

- **MLflow Tracking Server** (Deployment + Service + PVC)
- **JupyterLab** (Deployment + Service + PVC + initContainer + Secret)

JupyterLab настроен на работу с MLflow через переменную окружения `MLFLOW_TRACKING_URI` (например: `http://mlflow:5000`).

---

## Структура репозитория

- `jupyter-lab/Dockerfile` — кастомный Docker-образ для JupyterLab
- `k8s/jupyter-secret.yaml` — Secret с `JUPYTER_TOKEN`
- `k8s/jupyter-deployment.yaml` — Deployment + Service (NodePort) + PVC для Jupyter
- `k8s/mlflow-deployment.yaml` — Deployment + Service (NodePort) + PVC для MLflow

---

## Чек-лист требований ЛР4

- [x] минимум 2 Deployment: `jupyter`, `mlflow`
- [x] кастомный образ: JupyterLab собирается из `jupyter-lab/Dockerfile`
- [x] initContainer: используется в Deployment `jupyter`
- [x] volume: используются PVC для данных (`jupyter` и `mlflow`)
- [x] Secret: `jupyter-secret` (token)
- [x] Service: есть как минимум для одного сервиса (в реализации — для обоих)
- [x] Readiness/Liveness probes: настроены минимум в одном Deployment (в реализации — настроены)
- [x] labels: используются в манифестах

---

## Как запустить (Minikube)

### 1) Запуск minikube

```bash
minikube start
kubectl get nodes
```

### 2) Сборка кастомного образа JupyterLab

В манифестах используется локальный образ (например, `my-jupyter`), поэтому удобнее всего собрать образ **внутри docker-демона minikube**:

```bash
eval $(minikube docker-env)
docker build -t my-jupyter -f jupyter-lab/Dockerfile jupyter-lab
docker images | grep my-jupyter
```

> Если имя образа в вашем `k8s/jupyter-deployment.yaml` другое — используйте именно его в `docker build -t ...`.

### 3) Применение манифестов

Рекомендуемый порядок (сначала зависимости, затем приложения):

```bash
kubectl apply -f k8s/jupyter-secret.yaml
kubectl apply -f k8s/mlflow-deployment.yaml
kubectl apply -f k8s/jupyter-deployment.yaml
```

### 4) Проверка состояния

```bash
kubectl get pods
kubectl get svc
kubectl get pvc
```

Полезные команды для отладки:

```bash
kubectl describe deployment jupyter
kubectl describe deployment mlflow

kubectl logs deployment/jupyter
kubectl logs deployment/mlflow
```

---

## Как открыть сервисы

### MLflow

Если сервис создан как `NodePort`, открыть можно так:

```bash
minikube service mlflow --url
```

Откройте выданный URL в браузере.

### JupyterLab

```bash
minikube service jupyter --url
```

Если Jupyter просит токен, он берётся из Secret. Проверить токен в кластере:

```bash
kubectl get secret jupyter-secret -o jsonpath="{.data.JUPYTER_TOKEN}" | base64 -d && echo
```

---

## Очистка ресурсов

```bash
kubectl delete -f k8s/jupyter-deployment.yaml
kubectl delete -f k8s/mlflow-deployment.yaml
kubectl delete -f k8s/jupyter-secret.yaml

minikube stop
```
