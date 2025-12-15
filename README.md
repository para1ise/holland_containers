# Ход работы

## Запуск манифестов

1. Применить ресурсы Postgres:
   - `kubectl apply -f k8s/postgres/postgres-configmap.yaml`
   - `kubectl apply -f k8s/postgres/postgres-secret.yaml`
   - `kubectl apply -f k8s/postgres/postgres-deployment.yaml`
   - `kubectl apply -f k8s/postgres/postgres-service.yaml`
2. Применить ресурсы Nextcloud:
   - `kubectl apply -f k8s/nextcloud/nextcloud-configmap.yaml`
   - `kubectl apply -f k8s/nextcloud/nextcloud-secret.yaml`
   - `kubectl apply -f k8s/nextcloud/nextcloud-deployment.yaml`
   - `kubectl apply -f k8s/nextcloud/nextcloud-service.yaml`

## Проверка развёртывания

- `kubectl get pods` — оба пода должны быть `Running`, у Nextcloud появятся readiness/liveness пробы.
- `kubectl describe pod postgres-...` / `kubectl describe pod nextcloud-...` — убедиться, что переменные окружения получены корректно.
- `kubectl logs deployment/nextcloud` — наблюдать автоматическую инициализацию Nextcloud.
- `kubectl get svc` — увидеть `postgres-service` и `nextcloud-service` с NodePort 30432 и 30080 соответственно.

### Доступ к веб-интерфейсу

1. Пробросить сервис: `kubectl port-forward svc/nextcloud-service 8080:80`. Перейти по адресу `http://127.0.0.1:8080/login`
2. Перейти в браузере по выданному адресу.
3. Авторизоваться логином `admin` (или указанным в ConfigMap) и паролем из `nextcloud-secret.yaml`.

## Очистка ресурсов

```
kubectl delete -f k8s/nextcloud/
kubectl delete -f k8s/postgres/
minikube stop
```

# Ответы на вопросы

1. Важен ли порядок выполнения этих манифестов? Почему?

   ```
   Да, важен. Если сначала создадать Deployment, который ссылается на еще не существующий ConfigMap или Secret, под может упасть с ошибкой и будет висеть в этом состоянии, пока не будут созданы нужные ресурсы конфигурации. Если создать Deployment до Service, то переменные окружения, связанные с сервисом (которые кубер добавляет автоматически), могут быть недоступны, хотя DNS-имя сервиса заработает сразу после его создания.
   ```

2. Что (и почему) произойдет, если отскейлить
   количество реплик postgres-deployment в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?

   ```
   Nextcloud выдаст ошибку подключения к БД или предложит заново ввести логин/пароль. Все данные, сохраненные ранее, исчезнут.
   В предоставленных примерах не используются волюмы. Данные базы данных хранятся внутри контейнера (в эфемерном хранилище). Когда будут заскейлены реплики в 0, под удаляется вместе с его файловой системой. При возвращении в 1 создается совершенно новый чистый контейнер с пустой базой данных.
   ```
