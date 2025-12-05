# ЛР 2: Apache Airflow в Docker Compose

Репозиторий содержит минимальную, но полностью рабочую конфигурацию **Apache Airflow + PostgreSQL** на базе Docker Compose, соответствующую всем требованиям лабораторной работы.



---

## Содержимое репозитория

| Файл | Назначение |
|------|-----------|
| `docker-compose.yml` | Оркестрация трёх сервисов: `postgres`, `airflow-init`, `airflow-webserver` |
| `.env` | Хранение всех переменных окружения |
| `Dockerfile` | Сборка кастомного образа Airflow |
| `README.md` | Данный файл — описание и ответы на контрольные вопросы |

---
---
## Запуск проекта
docker-compose up -d
---

## Описание docker-compose.yml

Конфигурация включает:

- **3 сервиса**:
  - `postgres` — база данных (PostgreSQL 14)
  - `airflow-init` — одноразовый init-контейнер для инициализации БД и создания админа
  - `airflow-webserver` — основное приложение Airflow
- **Автоматическая сборка** образа из `Dockerfile` (`build: .`)
- **Жёсткое именование контейнеров** через `container_name`
- **Зависимости запуска**:
  - `airflow-init` запускается только после `postgres` с условием `service_healthy`
  - `airflow-webserver` запускается только после успешного завершения `airflow-init`
- **Volume** `postgres-db-volume` для сохранения данных БД между перезапусками
- **Проброс порта** `8080:8080` — веб-интерфейс доступен на хосте
- **Команда `command`** в `airflow-init` — выполняет `airflow db init` и создаёт пользователя
- **Healthcheck** для `postgres` (`pg_isready`) и `webserver` (`curl /health`)
- **Все переменные окружения** вынесены в `.env`
- **Явная пользовательская сеть** `airflow-network`

Также для `airflow-webserver` заданы **ограничения по памяти**:
```yaml
mem_limit: 1g
mem_reservation: 512m
```

---
## Ответы на вопросы:
1.Можно ли ограничивать ресурсы (например, память или CPU) для сервисов в docker-compose.yml? Если нет, то почему, 
если да, то как?
Ответ: Да, можно. Docker Compose поддерживает ограничение ресурсов через специальные параметры в конфигурации сервиса, например как у нас:
mem_limit: 1g         
mem_reservation: 512m  

2. Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные?
Ответ: docker-compose up -d <service_name> 
---
