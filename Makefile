build:
	docker build -t churn-api .

run:
	docker run -d -p 10000:10000 --name churn-container churn-api

stop:
	docker stop churn-container

remove:
	docker rm churn-container

logs:
	docker logs -f churn-container