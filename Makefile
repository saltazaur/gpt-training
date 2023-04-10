create-db:
	docker run --name mysql-bat \
		-e MYSQL_USER=gpt \
		-e MYSQL_PASSWORD=pass \
		-e MYSQL_ROOT_PASSWORD=pass \
		--mount type=bind,src=${PWD},dst=/data/backups \
		--rm mysql

populate-db:
	docker exec -it mysql-bat \
		mysql -u root -p -e "source /data/backups/mysqlsampledatabase.sql"

build-streamlit-container:
	docker build -t streamlit .

run-app:
	docker run --name dashboard \
		--mount type=bind,src=${PWD}/dashboard,dst=/app/ \
		-p 8501:8501 streamlit \
		streamlit run /app/app.py --server.port=8501 --server.address=0.0.0.0
