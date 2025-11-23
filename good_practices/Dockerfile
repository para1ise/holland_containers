# Fix 1: Фиксация версии Airflow и версии Python
FROM apache/airflow:2.7.1-python3.10

# Переключаемся на root ТОЛЬКО для установки системных зависимостей
USER root

# Fix 2: Объединение команд, отсутствие мусора, очистка apt-cache
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Fix 3: Возвращаемся к пользователю airflow для безопасности
USER airflow

WORKDIR /opt/airflow

# Fix 4: Оптимизация слоев. Сначала зависимости (меняются редко)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# DAG-файлы мы не копируем COPY, так как по заданию будем монтировать их через Volume.
# Но если бы копировали — делали бы это строго ЗДЕСЬ, в самом конце.


# Стандартная точка входа Airflow
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["standalone"]