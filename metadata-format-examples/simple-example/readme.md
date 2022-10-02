# Files in this folder

This folder contains the following files:
 * this readme file, which describes the original set up for the example and a proposal for a standardized hub representation
 * a corresponding proposed Hub metadata file, which encodes the model output tasks and task ids
 * TODO: some sample R code that could be used to work with the Hub metadata files

# Example set up

This is a relatively simple example based on the Flusight forecasting exercise for influenza that CDC ran in the 2021/2022 influenza season.

## Original forecasting exercise setup

In the original exercise, model output submission files had the following columns:

| forecast_date | target | target_end_date | location | type | quantile | value |
|---------------|--------|-----------------|----------|------|----------|-------|
2022-06-20 | 1 wk ahead inc flu hosp | 2022-06-25 | 01 | point    | NA   | 21
2022-06-20 | 1 wk ahead inc flu hosp | 2022-06-25 | 01 | quantile | 0.01 | 8
... | ... | ... | ... | ... | ... | ...

We conceptually divide these columns into two groups:

### 1. Model task ids

Forecasts were accepted for all combinations of the following factors defining modeling tasks:
 * `forecast_date`: Mondays from `2022-01-10` to `2022-06-20`.
 * `target`: `['1 wk ahead inc flu hosp', '2 wk ahead inc flu hosp', '3 wk ahead inc flu hosp', '4 wk ahead inc flu hosp']`
 * `location`: `['01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56', '72', '78', 'US']`

As illustrated above, submission files additionally included a `target_end_date` column, but that column is redundant with the `forecast_date` and `target` columns in the sense that if the values of the `forecast_date` and `target` are known, the `target_end_date` can be calculated directly.

### 2. Model output representations

For all model tasks, point and quantile forecasts were accepted. The model outputs were identified by the following columns:
 * `type`: `'point'` or `'quantile'`. Note that it was not specified what should be used for point predictions (e.g., mean, median, or other)
 * `quantile`: `NA` if the `type` was `'point'`; for `'quantile'` forecasts, one of the following probability levels: [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99]
 * `value`: a non-negative integer, the numeric value of the model's prediction (i.e., the point or quantile forecast value).

## Revised proposal

A representation of model outputs in line with the recommendations that have been discussed by the hub data formats working group might take the following form:

| origin_date | horizon | location | type | type_id | value |
|---------------|--------|----------|------|----------|-------|
2022-06-20 | 1 | 01 | mean    | NA   | 21
2022-06-20 | 1 | 01 | quantile | 0.01 | 8
... | ... | ... | ... | ... | ...

We have made five changes from the original format of the model output submissions:
 * Rather than using `forecast_date`, we have switch to the column name `origin_date`, in line with naming standards agreed upon by the Hubs.
 * In the original format, all entries of the `target` column contained the string `" wk ahead inc flu hosp"`. In our revised proposal, this column has been replaced by the `horizon` column which contains values in the array `[1, 2, 3, 4]`. This eliminates the storage of redundant information, and reduces the need for regular expression parsing to extract the forecast horizon from the target.
 * In the original format, the `target_end_date` column was redundant with the `forecast_date` and `target` columns, as discussed above. We have eliminated that column here.
 * In the original format, the type of the point forecast was left unspecified. Here, we are explicit that the point forecast is a predictive mean. This ensures that the point forecasts from different models are comparable, and that the point forecast provides different information than the predictive quantile at probability level 0.5.
 * The `quantile` column has been renamed to the more generally-applicable `type_id`.
