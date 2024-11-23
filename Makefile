up:
	docker compose --env-file env up --build -d

down:
	docker compose --env-file env down 

sh:
	docker exec -ti app bash

run-etl:
	docker exec app python src/loader/load_user_data.py

run-enrich:
	docker exec app python src/transformer/enrich_user_data.py

warehouse:
	docker exec -ti warehouse psql postgres://sdeuser:sdepassword1234@localhost:5432/warehouse

pytest:
	docker exec app pytest -p no:warnings -v /code/test
	
isort:	
	docker exec app isort /code

format:
	docker exec app python -m black -S --line-length 79 /code

type:
	docker exec app mypy --ignore-missing-imports /code

lint:
	docker exec app flake8 /code

ci: isort format type lint pytest
