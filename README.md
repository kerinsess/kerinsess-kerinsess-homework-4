# Гіпотеза Колатца — Docker

Паралельне обчислення кількості кроків послідовності Колатца для чисел від 1 до N.

## Структура репозиторія

```
collatz-docker/
├── collatz.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Вимоги

- [Docker](https://docs.docker.com/get-docker/) ≥ 20.10
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.0

## Запуск

```bash
docker compose up --build
```

## Параметри

| Змінна            | За замовчуванням | Опис                         |
|-------------------|------------------|------------------------------|
| `COLLATZ_N`       | `10000000`       | Верхня межа чисел (1 … N)    |
| `COLLATZ_THREADS` | `4`              | Кількість потоків ThreadPool |

## Запуск з кастомними параметрами

```bash
docker run --rm -e COLLATZ_N=1000000 -e COLLATZ_THREADS=8 collatz-parallel
```
