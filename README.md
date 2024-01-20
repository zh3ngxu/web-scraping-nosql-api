<div  align='center'><img src='https://s3.amazonaws.com/weclouddata/images/logos/wcd_logo_new_2.png' width='15%'></div >
<p style="font-size:30px;text-align:center"><b>API project using bs4 fastAPI and Elasticsearch</b></p>
<p style="font-size:20px;text-align:center"><b><font color='#F39A54'>Data Engineering Diploma</font></b></p>
<p style="font-size:15px;text-align:center">Content developed by: WeCloudData Academy</p>

## Goal

This project demonstrates the use of FastAPI to build an API for querying an Elasticsearch database. The Elasticsearch database is populated with data from web scraping using BeautifulSoup4.

## Project Structure

- **scripts/:** Contains Python scripts for web scraping and Elasticsearch indexing.
  - `web_scraping_script.py`: Web scraping script using BeautifulSoup4.
  - `elasticsearch_indexing_script.py`: Script to index data into Elasticsearch.

- **data/:** Contains the data files.
  - `output.csv`: CSV file containing data scraped from the web.

- **api/:** FastAPI application folder.
  - `main.py`: FastAPI application file with API routes for querying Elasticsearch.

- **docker-compose.yml:** Docker Compose file for setting up FastAPI and Elasticsearch containers.

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