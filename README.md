## Goal

This project demonstrates the use of FastAPI to build an API for querying an Elasticsearch database. The Elasticsearch database is populated with data from web scraping using BeautifulSoup4.

Please create a project folder using Github Repo and implement the functionalities required in the next section. You could start from scratch from hints in the `Project Structure` section or refer to the solution scripts. 

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

Files description and requirements:

- **ubuntu_sys_init.sh:** An EC2 bootstrap script to update package manager and install Docker and Pip in Ubuntu environment.

- **scripts/:** Contains Python scripts for web scraping and Elasticsearch indexing.
  - `fetch_course.py`: Web scraping script using BeautifulSoup4 to scrape course list from a [course website](https://hackr.io/blog/tag/courses). All course titles, authors, short descriptions and link should be extracted and save as `/data/output.csv`. Pagination is optional.
  - `es_insert_items.py`: Script to index data into Elasticsearch to support FastAPI. The script should read the `/data/output.csv`, create index in Elasticsearch and insert documents into the index.
  - `notebook_local_dev.ipynb`: notebook for testing the web scraping locally in an interactive environment

- **data/:** Contains the data files.
  - `output.csv`: CSV file containing data scraped from the web.

- **api/:** FastAPI application folder.
  - `main.py`: FastAPI application file with API routes for querying Elasticsearch. The route should include `/` endpoint to return a simple JSON response, and a `/search/<index>` endpoint to query elasticsearch database through additional query params. For example, `http://<EC2-IP>:8000/search/courses?query=php`
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

2. Start Docker containers
```
docker-compose build --no-cache
docker-compose up
```

Run `docker-compose build --no-cache` to build images for docker-compose, the `fastapi-app` container will pick up the `Dockerfile` from `backend_api/`. The docker file will 

  - Use an official Python runtime as a parent image: FROM python:3.8-slim
  - Set the working directory in the container: WORKDIR /app
  - Copy the current directory contents into the container at /app: COPY . /app
  - Install any needed packages specified in requirements.txt: RUN pip install --no-cache-dir -r requirements.txt
  - Make port 8000 available to the world outside this container: EXPOSE 8000
  - Define environment variable: ENV ELASTICSEARCH_URL=http://elasticsearch:9200
  - Run app.py when the container launches: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

`docker-compose up` will start 3 containers running Elasticsearch, Kibana and FastAPI.

- FastAPI will serve as backend API service to allow users to search on scraped courses
- Elasticsearch will serve as backend database to store courses info from web scraping script and support context search
- Kibana provide a Dev Tool for testing and debugging of the database

3. Start web scraping and store in database
```bash
rm data/output.csv
python3 scripts/fetch_course.py
python3 scripts/es_insert_items.py
```

The `fetch_course.py` extracts course titles, tags, authors, course_date, course_link and first 4 paragraphs for each article from https://hackr.io/blog/tag/courses website. The course link will be requested separately in a loop to extract more info.


The `es_insert_items.py` should implement functions: `create_index(index_name)`: Checks if the specified Elasticsearch index exists. If not, it creates the index and prints a message. `insert_data(index_name, csv_file_path)`: Reads data from a CSV file specified by csv_file_path and inserts each row as a document into the Elasticsearch index specified by index_name.

4. Test the API endpoint
Edit the EC2 instance security group to allow port 8000, 5601 from your IP. Then browse the URL link `http://<your-ec2-ip>:8000/` to see if there's response message return. Then test the URL `http://<EC2-IP>:8000/search/courses?query=<any keyword>`. This will execute the `search_index()` function in the `backend_api/main.py`. This function eefines a `/search/{index}` endpoint that accepts two path parameters: index (the Elasticsearch index to search) and query (the search query). It tries to execute a search query against the specified Elasticsearch index using the provided query string. If successful, returns the search result as a JSON response with a status code of 200.
If an exception occurs (e.g., Elasticsearch server connection issues), returns an error message as a JSON response with a status code of 500. Please refer to this [doc](https://elasticsearch-py.readthedocs.io/en/7.x/async.html?highlight=search#elasticsearch.AsyncElasticsearch.search) to get more details about how to use `search` in the elasticsearch python library.

The searched keywork in the `query` parmater might not return any doc from Elasticsearch due to the small document collection size. Please browse the Kibana Dev Tool `http://<EC2-IP>:5601/app/kibana#/dev_tools/` to find the all documents using the DSL query `GET courses/_search?size=10`

The `http://<EC2-IP>:8000/docs` provides an out-of-box doc webpage.

## Next Steps
Here's some more diretions to work on when you finish this lab:
- Use another static website to scrape data from pull data from any one within the [public api](https://github.com/public-apis/public-apis)
- Enhance the API functionality by increasing the number of endpoints or enhance the logic of the API request. Enrich the doc
- Add CICD for the project for automated testing and deployment using Github Actions and Terraform
- Add schedule on the web scarping script to make it automated and run on regular basis