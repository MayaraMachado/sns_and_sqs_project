# SNS and SQS Project

This is a study project, that still is in progress, of what you can do with AWS SNS and SQS in a Publish/Subscribe pattern. I used Django Rest Framework to build two Rest Services, that doesn't have conection and comunicate only via SNS and SQS.

## First run

1. Clone the repo
2. Create your .env file for the two DRF Services
3. Load the fixtures
4. Build and run docker containers by running

```shell
docker-compose up
```
## API Routes
### Ecommerce service

- [GET] localhost:8000/products
- [POST] localhost:8000/purchase

### Payment Gateway service

- [GET] localhost:8001/billing/<int:seller_id>

