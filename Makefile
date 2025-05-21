build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync
migrate:
	python3 manage.py migrate
start:
	python3 manage.py runserver
ruff:
	uv run ruff check task_manager/
format:
	uv run black task_manager/
test:
	python3 manage.py test
