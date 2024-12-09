core_path = src/py/bot_core.py
aux_path = src/py/bot_aux.py
db_helper_path = src/py/helper/db_helper.py
db_tests_path = src/py/db_helper_tests.py

compose_up:
	docker compose up --build

clean:
	docker compose down

run_listener:
	python $(core_path) xiv-database.ini xiv-discord.token

run_linter:
	pylint --rcfile pylint.toml $(core_path) $(aux_path) $(db_helper_path)

run_tests:
	pytest $(db_tests_path)

generate_backup:
	tar cvf backups/"backup-"$$(date -Idate).tar .
