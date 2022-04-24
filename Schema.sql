DROP SCHEMA IF EXISTS fuel_and_stock_price CASCADE;

Create schema fuel_and_stock_price;


drop table if exists fuel_and_stock_price.stock_price CASCADE;
drop table if exists fuel_and_stock_price.fuel_price CASCADE;
drop table if exists fuel_and_stock_price.us_info CASCADE;
drop table if exists fuel_and_stock_price.uk_info CASCADE;
drop table if exists fuel_and_stock_price.us_diff CASCADE;
drop table if exists fuel_and_stock_price.uk_diff CASCADE;


CREATE TABLE "fuel_and_stock_price.stock_price" (
  "date" varchar PRIMARY KEY,
  "uga_close" float,
  "shell_close" float,
  "uga_volume" float,
  "shell_volume" float,
  "uga_difference" float,
  "shell_difference" float
);

CREATE TABLE "fuel_and_stock_price.fuel_price" (
  "date" varchar PRIMARY KEY,
  "us_price" float,
  "uk_price" float,
  "us_price_diff" float,
  "uk_diff" float
);

CREATE TABLE "fuel_and_stock_price.us_info" (
  "date" varchar PRIMARY KEY,
  "uga_close" float,
  "uga_volume" float,
  "uga_difference" float,
  "us_price" float
);

CREATE TABLE "fuel_and_stock_price.uk_info" (
  "date" varchar PRIMARY KEY,
  "shell_close" float,
  "shell_volume" float,
  "shell_difference" float,
  "uk_price" float
);

CREATE TABLE "fuel_and_stock_price.us_diff" (
  "date" varchar PRIMARY KEY,
  "us_price_diff" float,
  "uga_difference" float
);

CREATE TABLE "fuel_and_stock_price.uk_diff" (
  "date" varchar PRIMARY KEY,
  "uk_diff" float,
  "shell_difference" float
);

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("date") REFERENCES "fuel_and_stock_price.us_diff" ("date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("date") REFERENCES "fuel_and_stock_price.fuel_price" ("date");

ALTER TABLE "fuel_and_stock_price.us_info" ADD FOREIGN KEY ("date") REFERENCES "fuel_and_stock_price.stock_price" ("date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("date") REFERENCES "fuel_and_stock_price.uk_info" ("date");

ALTER TABLE "fuel_and_stock_price.stock_price" ADD FOREIGN KEY ("date") REFERENCES "fuel_and_stock_price.uk_diff" ("date");
