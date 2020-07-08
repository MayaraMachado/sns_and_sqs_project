run:
	docker-compose up -d

stop:
	docker-compose down

shell_ecommerce:
	docker exec -it ecommerce_container bash

shell_payment:
	docker exec -it payment_gateway_container bash

psql:
	docker exec -it postgres psql -U postgres
