-- Average price of a car_company by announcement_year
SELECT car_company, EXTRACT(YEAR FROM announcement_date) AS announcement_year, AVG(price) AS avg_price FROM cars
WHERE price IS NOT NULL
GROUP BY car_company, announcement_year
ORDER BY avg_price DESC;


-- Get EVG price of Honda in 2024
SELECT AVG(price) AS avg_price FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024;

-- Get AVG km of Honda in 2024
SELECT AVG(km) AS avg_km FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024;

-- Get Total listed Hondas in 2024
SELECT COUNT(*) FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024;

-- Get Total price of all Hondas in 2024
SELECT SUM(price) AS total_price FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024;

-- Get Total listed Hondas per month in 2024
SELECT TO_CHAR(announcement_date, 'Mon') AS month, COUNT(*) AS total_cars FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024
GROUP BY TO_CHAR(announcement_date, 'Mon'), TO_CHAR(announcement_date, 'MM')
ORDER BY TO_CHAR(announcement_date, 'MM')::INTEGER;

-- Get top 10 car_models of listed Hondas in 2024
SELECT car_model, COUNT(*) AS total_cars FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024
GROUP BY car_model
ORDER BY total_cars DESC
LIMIT 10;

-- Get the most expnasive and cheapest Honda price in 2024
SELECT MAX(price) AS highest_price, MIN(price) AS lowest_price FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024;

-- Get Average Price of Hondas per month in 2024
SELECT TO_CHAR(announcement_date, 'Mon') AS month, AVG(price) AS avg_price FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024
GROUP BY TO_CHAR(announcement_date, 'Mon'), TO_CHAR(announcement_date, 'MM')
ORDER BY TO_CHAR(announcement_date, 'MM')::INTEGER;

-- Get Highest and Lowest price for Honda in 2024
SELECT car_model, MAX(price) AS highest_price, MIN(price) AS lowest_price FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024 AND price IS NOT NULL
GROUP BY car_model
ORDER BY highest_price DESC
LIMIT 10;

-- Get Locations of the most Honda listings in 2024
SELECT location, COUNT(*) AS total_listed FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024
GROUP BY location
ORDER BY total_listed DESC;

-- Get Honda transmisissions in 2024
SELECT transmission, COUNT(*) AS total_cars FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024
GROUP BY transmission;

-- Get Honda feuls in 2024
SELECT fuel, COUNT(*) FROM cars
WHERE car_company = 'Honda' AND EXTRACT(YEAR FROM announcement_date) = 2024 AND fuel IS NOT NULL
GROUP BY fuel;
