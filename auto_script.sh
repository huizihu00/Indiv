bash install_spark.sh
pip install dvc


dvc exp run -f us_fuelprice_df_checks
dvc exp run -f uk_fuelprice_df_checks
dvc exp run -f stock_price_checks
dvc exp run -f fuel_price_checks
dvc exp rum -f us_diff_checks
dvc exp rum -f us_info_checks


dvc exp show