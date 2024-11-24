compose_up:
	docker compose up --build

clean:
	docker compose down

run_listener:
	python ./src/py/bot-core.py xiv-database.ini xiv-discord.token
