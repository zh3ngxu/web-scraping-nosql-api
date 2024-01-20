## Goal

This project demonstrates the use of FastAPI to build an API for querying an Elasticsearch database. The Elasticsearch database is populated with data from web scraping using BeautifulSoup4.

Please create a project folder using Github Repo and implement the functionalities required in the next section.

## Project Structure

```bash
├── README.md
├── backend_api
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── data
│   ├── output.csv
├── docker-compose.yaml
├── requirements.txt
├── scripts
│   ├── es_insert_items.py
│   ├── fetch_course.py
│   └── notebook_local_dev.ipynb
└── ubuntu_sys_init.sh
```

- **scripts/:** Contains Python scripts for web scraping and Elasticsearch indexing.
  - `fetch_course.py`: Web scraping script using BeautifulSoup4 to scrpe course list from a [course website](https://hackr.io/blog/tag/courses).
  - `es_insert_items.py`: Script to index data into Elasticsearch to support FastAPI.
  - `notebook_local_dev.ipynb`: notebook for testing the web scraping locally in an interactive environment

- **data/:** Contains the data files.
  - `output.csv`: CSV file containing data scraped from the web.

- **api/:** FastAPI application folder.
  - `main.py`: FastAPI application file with API routes for querying Elasticsearch.
  - `Dockerfile`: Dockerfile to build custom Docker image and install FastAPI from a base Python image. The `fastapi-app` container will be built on top of this image
  - `requirements.txt`: dependency package by the Docker image

- **docker-compose.yml:** Docker Compose file for setting up FastAPI, Elasticsearch and Kibana containers.



## Prerequisites

- Python
- Docker
- Docker Compose

## Getting Started

1. create EC2 intance using Ubuntu image and config the system.

The `apt` package manager will install pip, and docker
```
chmod +x ubuntu_sys_init.sh
sudo ./ubuntu_sys_init.sh
```

2. Install 

https://elasticsearch-py.readthedocs.io/en/7.x/async.html?highlight=search#elasticsearch.AsyncElasticsearch.search


3. Run `docker-compose build --no-cache` to build images for docker-compose, the `fastapi-app` container will pick up the `Dockerfile` from `backend_api/`. The docker file will 

  - Use an official Python runtime as a parent image: FROM python:3.8-slim
  - Set the working directory in the container: WORKDIR /app
  - Copy the current directory contents into the container at /app: COPY . /app
  - Install any needed packages specified in requirements.txt: RUN pip install --no-cache-dir -r requirements.txt
  - Make port 8000 available to the world outside this container: EXPOSE 8000
  - Define environment variable: ENV ELASTICSEARCH_URL=http://elasticsearch:9200
  - Run app.py when the container launches: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

