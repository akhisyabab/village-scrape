CREATE DATABASE village_scrape_prod;
CREATE DATABASE village_scrape_dev;
CREATE DATABASE village_scrape_test;

--CREATE USER villagescrapeuser WITH password 'villagescrapepassword';
GRANT ALL PRIVILEGES ON database village_scrape_dev to villagescrapeuser;
ALTER USER villagescrapeuser SUPERUSER;
