DROP SCHEMA IF EXISTS fuel_and_stock_price CASCADE;

Create schema fuel_and_stock_price;


drop table if exists stock_price CASCADE;
drop table if exists fuel_price CASCADE;
drop table if exists us_info CASCADE;
drop table if exists uk_info CASCADE;
drop table if exists us_diff CASCADE;
drop table if exists uk_diff CASCADE;


CREATE TABLE "stock_price" (
  "Date" varchar PRIMARY KEY,
  "uga_Close" float,
  "shell_Close" float,
  "uga_Volume" float,
  "shell_Volume" float,
  "uga_Difference" float,
  "shell_Difference" float
);

CREATE TABLE "fuel_price" (
  "Date" varchar PRIMARY KEY,
  "us_price" float,
  "uk_price" float,
  "us_price_diff" float,
  "uk_diff" float
);

CREATE TABLE "us_info" (
  "Date" varchar PRIMARY KEY,
  "uga_Close" float,
  "uga_Volume" float,
  "uga_Difference" float,
  "us_price" float
);

CREATE TABLE "uk_info" (
  "Date" varchar PRIMARY KEY,
  "shell_Close" float,
  "shell_Volume" float,
  "shell_Difference" float,
  "uk_price" float
);

CREATE TABLE "us_diff" (
  "Date" varchar PRIMARY KEY,
  "us_price_diff" float,
  "uga_Difference" float
);

CREATE TABLE "uk_diff" (
  "Date" varchar PRIMARY KEY,
  "uk_diff" float,
  "shell_Difference" float
);

ALTER TABLE "stock_price" ADD FOREIGN KEY ("Date") REFERENCES "us_diff" ("Date");

ALTER TABLE "stock_price" ADD FOREIGN KEY ("Date") REFERENCES "fuel_price" ("Date");

ALTER TABLE "us_info" ADD FOREIGN KEY ("Date") REFERENCES "stock_price" ("Date");

ALTER TABLE "stock_price" ADD FOREIGN KEY ("Date") REFERENCES "uk_info" ("Date");

ALTER TABLE "stock_price" ADD FOREIGN KEY ("Date") REFERENCES "uk_diff" ("Date");
