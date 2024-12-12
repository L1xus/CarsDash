# Used Cars Market end-to-end Project

This repository contains a personal project focused on building an end-to-end data pipeline for used car market in Morocco. The pipeline automates data collection, cleaning, transformation, storage in an AWS RDS PostgreSQL database, and visualization through Grafana dashboard.

> [!IMPORTANT]
> Feel free to submit a PR request if you believe any changes are necessary...

## Table of Content
* [Architecture diagram](#architecture-diagram)
* [Overview](#overview)
    * [Data Scraping](#data_scraping)
    * [Data Cleaning & Transformation](#data_cleaning_&_transformation)
    * [Data Storage](#data_storge)
    * [Data Visualization](#data_visualization)
* [Tech Stack](#teck-stack)
* [Prerequisites](#prerequisites)
* [Run the project](#run-the-project)
* [Future Enhancements](#future_enhancements)

## Architecture diagram
Will add this later...

## Overview

### 1. Data Scraping
The **data scraping** phase is managed by scripts in avito/ and moteur/
- **Web Scraping:** Used Python's BeautifulSoup to extract data from the two used car marketplaces.
- **Attributes Collected:** Scraped key attributes such as price, car_model, car_company, year, km, and more...

### 2. Data Cleaning & Transformation
The **data cleaning and transformation** phase is handled by functions in db/
 - **Data Cleaning:** Remove null car_companies, normalize car_company and car_model, and delete inappropriate data using SQL.
 - **Transformation:** Structure data for relational storage and ensures compatibility with PostgreSQL schema.

### 3. Data Storage
The **data storage** phase is executed by insert script in db/
 - **AWS RDS Integration:** Load cleaned and structured data into an AWS RDS PostgreSQL database.

### 4. Data Visualization
The **data visualization** phase is implemented through grafana/
 - **Grafana Integration:** Configure interactive dashboard to visualize market trends, pricing... for every car_company.
 - **Grafana Cloud:** Leverage cloud-hosted service for dynamic, real-time data exploration.

## Tech Stack
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python badge">
    <img src="https://img.shields.io/badge/aws-252F3E?style=for-the-badge&logo=Amazon%20Web%20Services" alt="Amazon Cloud badge">
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker badge">
    <img src="https://img.shields.io/badge/grafana-182F9E?style=for-the-badge&logo=Grafana" alt="Grafana badge">
</div>

## Prerequisites
 - [Docker](https://docs.docker.com/get-docker/)
 - [Python 3.8+ (pip)](https://www.python.org/)
 - [docker-compose](https://docs.docker.com/compose/install/)
 - [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)

## Run the project
1. Clone the repository:
  ```
  git clone https://github.com/L1xus/CarsDash.git
  cd CarsDash
  ```
2. Run docker-compose
  ```docker-compose up --build```
3. Create the dashboard
  ```  
    cd grafana
    docker-compose up --build
  ```
4. Import the Cars Dashboard json file into grafana

## Future Enhancements
 - Add support for filtering by car_model and year.
 - Automate the process every month.
 - Enhance data quality by creating a machine learning model to filter car listings.
 - Consider a better option to make the dashboard public.
