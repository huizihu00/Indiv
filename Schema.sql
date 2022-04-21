DROP SCHEMA IF EXISTS fuel_and_stock_price CASCADE;

Create schema fuel_and_stock_price;


drop table if exists stock_price CASCADE;
drop table if exists fuel_price CASCADE;
drop table if exists us_info CASCADE;
drop table if exists uk_info CASCADE;
drop table if exists us_diff CASCADE;
drop table if exists uk_diff CASCADE;

CREATE TABLE "stock_price" (
  "date" varcahr PRIMARY KEY,
  "uga_close" float,
  "shell_close" float,
  "uga_volume" float,
  "shell_volume" float,
  "uga_diff" float,
  "shell_diff" float
);

CREATE TABLE "fuel_price" (
  "date" varchar PRIMARY KEY,
  "us_fuelprice" float,
  "uk_fuelprice" float,
  "us_diff" float,
  "uk_diff" float
);

CREATE TABLE "us_info" (
  "date" varchar PRIMARY KEY,
  "uga_close" float,
  "uga_volume" float,
  "uga_diff" float,
  "us_fuelprice" float
);

CREATE TABLE "uk_info" (
  "date" varchar PRIMARY KEY,
  "shell_close" float,
  "shell_volume" float,
  "shell_diff" float,
  "uk_fuelprice" float
);

CREATE TABLE "us_diff" (
  "date" varcahr PRIMARY KEY,
  "us_diff" float,
  "uga_diff" float
);

CREATE TABLE "uk_diff" (
  "date" varcahr PRIMARY KEY,
  "uk_diff" float,
  "shell_diff" float
);

ALTER TABLE "stock_price" ADD FOREIGN KEY ("date") REFERENCES "us_diff" ("date");

ALTER TABLE "uk_diff" ADD FOREIGN KEY ("date") REFERENCES "stock_price" ("date");

ALTER TABLE "fuel_price" ADD FOREIGN KEY ("date") REFERENCES "stock_price" ("date");

ALTER TABLE "uk_info" ADD FOREIGN KEY ("date") REFERENCES "stock_price" ("date");

ALTER TABLE "us_info" ADD FOREIGN KEY ("date") REFERENCES "stock_price" ("date");
