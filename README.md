# FastAPI Project Template

## Requirements

* [Docker](https://www.docker.com/).

## Local Development

* Start the stack with Docker Compose:

```bash
docker compose up -d
```

* Now you can open your browser and interact with these URLs:

* Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for 
the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker compose logs fastapi
```

If your Docker is not running in `localhost` (the URLs above wouldn't work) you would need to use the IP or domain 
where your Docker is running.
