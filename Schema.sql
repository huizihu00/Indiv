DROP SCHEMA IF EXISTS fuel_and_stock_price CASCADE;

Create schema fuel_and_stock_price;


drop table if exists fuel_and_stock_price.stock_price CASCADE;
drop table if exists fuel_and_stock_price.fuel_price CASCADE;
drop table if exists fuel_and_stock_price.us_info CASCADE;
drop table if exists fuel_and_stock_price.uk_info CASCADE;
drop table if exists fuel_and_stock_price.us_diff CASCADE;
drop table if exists fuel_and_stock_price.uk_diff CASCADE;


CREATE TABLE "fuel_and_stock_price.stock_price" (
  "Date" varchar PRIMARY KEY,
  "uga_Close" float,
  "shell_Close" float,
  "uga_Volume" float,
  "shell_Volume" float,
  "uga_Difference" float,
  "shell_Difference" float
);

CREATE TABLE "fuel_and_stock_price.fuel_price" (
  "Date" varchar PRIMARY KEY,
  "us_price" float,
  "uk_price" float,
  "us_price_diff" float,
  "uk_diff" float
);

CREATE TABLE "fuel_and_stock_price.us_info" (
  "Date" varchar PRIMARY KEY,
  "uga_Close" float,
  "uga_Volume" float,
  "uga_Difference" float,
  "us_price" float
);

CREATE TABLE "fuel_and_stock_price.uk_info" (
  "Date" varchar PRIMARY KEY,
  "shell_Close" float,
  "shell_Volume" float,
  "shell_Difference" float,
  "uk_price" float
);

CREATE TABLE "fuel_and_stock_price.us_diff" (
  "Date" varchar PRIMARY KEY,
  "us_price_diff" float,
  "uga_Difference" float
);

CREATE TABLE "fuel_and_stock_price.uk_diff" (
  "Date" varchar PRIMARY KEY,
  "uk_diff" float,
  "shell_Difference" float
);

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("Date") REFERENCES "fuel_and_stock_price.us_diff" ("Date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("Date") REFERENCES "fuel_and_stock_price.fuel_price" ("Date");

ALTER TABLE "fuel_and_stock_price.us_info" ADD FOREIGN KEY ("Date") REFERENCES "fuel_and_stock_price.stock_price" ("Date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("Date") REFERENCES "fuel_and_stock_price.uk_info" ("Date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("Date") REFERENCES "fuel_and_stock_price.uk_diff" ("Date");
