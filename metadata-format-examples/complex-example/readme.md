# Files in this folder

This folder contains the following files:
 * this readme file, which describes the set up for the example
 * a proposed Hub metadata file, which encodes the model output tasks and task ids
 * sample python code that illustrates resolving references in the json metadata file

# Example set up

We consider a hypothetical Scenario Modeling Hub that runs for two submission rounds with a different set of forecast tasks in each round. We give the details of each round in its own section.

## Round 1

In round 1, teams contribute mean, quantile, and cdf probabilities for one-week-ahead and two-week-ahead incidence, and cdf probabilities for the timing of a season peak. A `value` for a cdf forecast is the predictive probability that the target variable is less than or equal to the entry in the `type_id` column.

| origin_date | scenario_id | location | target      | horizon | type     | type_id  | value |
|-------------|-------------|----------|-------------|---------|----------|----------|-------|
| 2022-09-03  | 1           | US       | weekly rate | 1       | mean     | NA       | 5     |
| 2022-09-03  | 1           | US       | weekly rate | 1       | quantile | 0.25     | 2     |
| 2022-09-03  | 1           | US       | weekly rate | 1       | quantile | 0.5      | 3     |
| 2022-09-03  | 1           | US       | weekly rate | 1       | quantile | 0.75     | 10    |
| 2022-09-03  | 1           | US       | weekly rate | 1       | cdf      | 10.0     | 0.1   |
| 2022-09-03  | 1           | US       | weekly rate | 1       | cdf      | 20.0     | 0.2   |
| 2022-09-03  | 1           | US       | weekly rate | 2       | mean     | NA       | 4     |
| 2022-09-03  | 1           | US       | weekly rate | 2       | quantile | 0.25     | 1     |
| 2022-09-03  | 1           | US       | weekly rate | 2       | quantile | 0.5      | 3     |
| 2022-09-03  | 1           | US       | weekly rate | 2       | quantile | 0.75     | 12    |
| 2022-09-03  | 1           | US       | weekly rate | 2       | cdf      | 10.0     | 0.2   |
| 2022-09-03  | 1           | US       | weekly rate | 2       | cdf      | 20.0     | 0.4   |
| 2022-09-03  | 1           | US       | peak week   | NA      | cdf      | EW202240 | 0.001 |
| 2022-09-03  | 1           | US       | peak week   | NA      | cdf      | EW202241 | 0.002 |
| 2022-09-03  | ...         | ...      | ...         | ...     | ...      | ...      | ...   |
| 2022-09-03  | 1           | WY       | peak week   | NA      | cdf      | EW202320 | 0.013 |

Additionally, suppose that projections are required for all states, but are optional for the national level, and that the mean forecasts are optional but all other representations are required.

Again, at a conceptual level we divide these columns into two groups:

### 1. Model task ids

 * `origin_date`: `[2022-10-01]` Date relative to which short-term look-ahead targets are defined
 * `scenario_id`: `[1]` A unique identifier for the scenario under which projections are to be generated. In round 1, only a single scenario is considered.
 * `location`: `['01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56', 'US']`
 * `target`: `["weekly rate", "peak week"]`
 * `horizon`: `[1, 2]`; only applicable for the `"weekly rate"` targets

### 2. Model output representations

Of note, the accepted output representations differ for different values of the `target`.

For `"weekly rate"` targets, we accept the following output representation types:

 * `type = "mean"`:
    * submission is optional
    * `type_id` must be `"NA"`
    * `value` must be a non-negative integer
 * `type = "quantile"`:
    * if a forecast for a given model task id is present, quantile forecasts are required
    * `type_id` contains quantile probability levels
        * forecasts at the following probability levels are required: `[0.25, 0.5, 0.75]`
        * forecasts at the following probability levels are optional: `[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]`
    * `value` must be a non-negative integer
 * `type = "cdf"`:
    * if a forecast for a given model task id is present, cdf probability forecasts are required
    * `type_id` contains strings identifying the bins:
        * probabilities for the following values of incidence are required: `10.0`, corresponding to the interval `[-Inf, 10.0]`, and `20.0`, corresponding to the interval `(-Inf, 20.0]`
    * `value` must be a non-negative real number, with values that sum to 1 within each model task

For `"peak week"` targets, we accept the following output representation types:
 * `type = "cdf"`:
    * if a forecast for the given model task id is present, cdf probabilities are required
    * `type_id` contains strings identifying the values of the response variable at which the cdf is evaluated:
        * submissions are required for the probability that the peak occurs on or before each epidemic week in the season
    * `value` must be a non-negative real number, with values that sum to 1 within each model task

## Round 2

In round 2, two scenarios are considered, but only the short term quantile forecasts are submitted:

| origin_date | scenario_id | location | target      | horizon | type     | type_id | value |
|-------------|-------------|----------|-------------|---------|----------|---------|-------|
| 2022-10-01  | 2           | US       | weekly rate | 1       | quantile | 0.25    | 2     |
| 2022-10-01  | 2           | US       | weekly rate | 1       | quantile | 0.5     | 3     |
| 2022-10-01  | 2           | US       | weekly rate | 1       | quantile | 0.75    | 10    |
| 2022-10-01  | 2           | US       | weekly rate | 2       | quantile | 0.25    | 1     |
| 2022-10-01  | 2           | US       | weekly rate | 2       | quantile | 0.5     | 3     |
| 2022-10-01  | 2           | US       | weekly rate | 2       | quantile | 0.75    | 12    |
| 2022-10-01  | ...         | ...      | ...         | ...     | ...      | ...     | ...   |
| 2022-10-01  | 2           | WY       | weekly rate | 2       | quantile | 0.75    | 13    |
| 2022-10-01  | 3           | US       | weekly rate | 1       | quantile | 0.25    | 7     |
| 2022-10-01  | 3           | US       | weekly rate | 1       | quantile | 0.5     | 13    |
| 2022-10-01  | 3           | US       | weekly rate | 1       | quantile | 0.75    | 22    |
| 2022-10-01  | 3           | US       | weekly rate | 2       | quantile | 0.25    | 2     |
| 2022-10-01  | 3           | US       | weekly rate | 2       | quantile | 0.5     | 6     |
| 2022-10-01  | 3           | US       | weekly rate | 2       | quantile | 0.75    | 12    |
| 2022-10-01  | ...         | ...      | ...         | ...     | ...      | ...     | ...   |
| 2022-10-01  | 3           | WY       | weekly rate | 2       | quantile | 0.75    | 44    |

As before, projections are required for all states, but are optional for the national level.

For this round, we have the following specification of the columns in the submission files:

### 1. Model task ids

 * `origin_date`: `[2022-10-01]` Date relative to which short-term look-ahead targets are defined for this round
 * `scenario_id`: `[2, 3]` A unique identifier for the scenario under which projections are to be generated. In round 1, only a single scenario is considered.
 * `location`: `['01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56', 'US']`
 * `target`: `["weekly rate", "peak week"]`
 * `horizon`: `[1, 2]`; only applicable for the `"weekly rate"` targets

### 2. Model output representations

In this round, there are only `"weekly rate"` targets with quantile forecasts:

 * `type = "quantile"`:
    * if a forecast for a given model task id is present, quantile forecasts are required
    * `type_id` contains quantile probability levels
        * forecasts at the following probability levels are required: `[0.25, 0.5, 0.75]`
        * forecasts at the following probability levels are optional: `[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]`
    * `value` must be a non-negative integer
