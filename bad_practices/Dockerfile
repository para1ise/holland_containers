# Bad Practice 1: Использование тега latest - apache/airflow - может обновиться и всё...
FROM apache/airflow:latest

# Bad Practice 2: Запуск и работа от root (нарушение безопасности)
USER root

# Bad Practice 3:
RUN apt-get update
RUN apt-get install -y vim git nano


# При первой сборке всё работает. Но при повторной сборке Docker может использовать кэшированный слой с apt-get update (если Dockerfile не менялся).
# Тогда apt-get install выполнится на основе устаревшего списка пакетов, и установка может упасть (если пакет обновился), или ты получишь устаревшую версию пакета.


# Bad Practice4: Копируем DAG-файлы перед установкой зависимостей
COPY dags/ /opt/airflow/dags/

# Теперь, если мы поменяем хоть одну букву в любом DAG-файле,
# Docker сбросит кэш на этом этапе, и pip install будет выполняться ЗАНОВО.
# Это очень долго и бессмысленно.
# Плохо: пытаемся перейти в папку, но следующая команда COPY забудет об этом
RUN cd /opt/airflow
COPY requirements.txt .
# (Файл скопируется не туда, куда думал автор, или в дефолтную папку)
RUN pip install -r requirements.txt


# Оставляем пользователя root (опасно для рантайма)
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["standalone"]