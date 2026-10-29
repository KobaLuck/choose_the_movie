# Choose the Movie

Веб-приложение для мнений о фильмах: случайный выбор, добавление отзывов, REST API и изображения из Dropbox.

**Python · Flask · SQLAlchemy · aiohttp**

## Быстрый старт

```bash
git clone https://github.com/KobaLuck/choose_the_movie.git
cd choose_the_movie
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app opinions_app shell
# В открывшейся оболочке: from opinions_app import db; db.create_all()
# Затем exit()
flask --app opinions_app run
```

В Windows PowerShell окружение активируется командой `.venv\Scripts\Activate.ps1`.

Создайте `.env`: `DATABASE_URI=sqlite:///opinions.db`, `SECRET_KEY` — ваш случайный ключ. `DROPBOX_TOKEN` нужен только для загрузки изображений. API: `/api/opinions/` и `/api/get-random-opinion/`.

## Структура

- `settings.py` — исходный код.

---

[Никита Казанцев](https://github.com/KobaLuck) · [Все публичные проекты](https://github.com/KobaLuck?tab=repositories)
