# Used Cars Market end-to-end Project

This repository contains a personal project focused on building an end-to-end data pipeline for used car market in Morocco. The pipeline automates data collection, cleaning, transformation, storage in an AWS RDS PostgreSQL database, and visualization through Grafana dashboard.

> [!IMPORTANT]
> Feel free to submit a PR request if you believe any changes are necessary...

## Table of Content
* [Architecture diagram](#architecture-diagram)
* [Overview](#overview)

## Architecture diagram
Will add this later...

## Overview

### 1. Data Scraping
The **data scraping** phase is managed by scripts in avito/ and moteur/
- **Web Scraping:** Used Python's BeautifulSoup to extract data from the two used car marketplaces.
- **Attributes Collected:** Scraped key attributes such as price, car_model, car_company, year, mileage, and more...

### 2. Data Cleaning & Transformation
The **data cleaning and transformation** phase is handled by functions in db/
 - **Data Cleaning:** Remove null car_companies, normalize car_company and car_model, and delete inappropriate data using SQL.
 - **Transformation:** Structure data for relational storage and ensures compatibility with PostgreSQL schema.

### 3. Data Storage
The **data storage** phase is executed by insert script in db/
 - **AWS RDS Integration:** Load cleaned and structured data into an AWS RDS PostgreSQL database.
