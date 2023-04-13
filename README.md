# NLQ2SQL Natural Language Question to SQL query powered by OpenAI Large Language Models
## To get started
All commands needed to run the app in Docker containers are written down in Makefile.

1. Define environmental variable `OPENAI_API_KEY` with your OpenAI API Key (https://platform.openai.com/overview):
```
export OPENAI_API_KEY='[...]'
```
2. Run container with MySQL database:
```
make create-db
```
In Makefile, when a database is created we specify user name, its password and root's password. Change it if you need.

3. Populate MySQL database with data:
```
make populate-db
```
You will be asked for password - it's `pass`.
You may need to check what is IP of your MySQL container
 ```
 docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysql-bat
 ``` 
(it will be taken care of by Docker Composer in the next release of NLQ2SQL app)

4. Build image with Streamlit:
```
make build-streamlit-container
```
5. Run NLQ2SQL app:
```
make run-app
```
6. Visit `localhost:8501` to play with the app. 
If you encounter error realted to database conectivity - change `hostname` in `dashboard\bat-poc-cfg\db.yml` to the one you get in step 3.

## Using Azure OpenAI
* OpenAI library with Microsoft Azure endpoints: https://github.com/openai/openai-python#microsoft-azure-endpoints 
* The inference REST API endpoints for Azure OpenAI: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference