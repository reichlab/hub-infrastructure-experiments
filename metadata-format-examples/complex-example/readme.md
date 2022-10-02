# Files in this folder

This folder contains the following files:
 * this readme file, which describes the set up for the example
 * a proposed Hub metadata file, which encodes the model output tasks and task ids
 * sample python code that illustrates resolving references in the json metadata file
 * TODO: some sample R code that could be used to work with the Hub metadata file

# Example set up

We consider a hypothetical Hub that collects mean, quantile, and bin probability forecasts for one-week-ahead and two-week-ahead incidence, but bin probabilities for the timing of a season peak:

| origin_epiweek | location | target | horizon | type | type_id | value |
|----------------|----------|--------|---------|------|---------|-------|
| EW202242 | US | weekly rate | 1   | mean     | NA           | 5     |
| EW202242 | US | weekly rate | 1   | quantile | 0.25         | 2     |
| EW202242 | US | weekly rate | 1   | quantile | 0.5          | 3     |
| EW202242 | US | weekly rate | 1   | quantile | 0.75         | 10    |
| EW202242 | US | weekly rate | 1   | bin_prob | [0.0, 10.0]   | 0.1   |
| EW202242 | US | weekly rate | 1   | bin_prob | (10.0, 20.0]  | 0.2   |
| EW202242 | US | weekly rate | 1   | bin_prob | (20.0, Inf) | 0.7   |
| EW202242 | US | weekly rate | 2   | mean     | NA           | 4     |
| EW202242 | US | weekly rate | 2   | quantile | 0.25         | 1     |
| EW202242 | US | weekly rate | 2   | quantile | 0.5          | 3     |
| EW202242 | US | weekly rate | 2   | quantile | 0.75         | 12    |
| EW202242 | US | weekly rate | 2   | bin_prob | [0.0, 10.0]   | 0.2   |
| EW202242 | US | weekly rate | 2   | bin_prob | (10.0, 20.0]  | 0.2   |
| EW202242 | US | weekly rate | 2   | bin_prob | (20.0, Inf) | 0.6   |
| EW202242 | US | peak week   | NA  | bin_prob | EW202240     | 0.001 |
| EW202242 | US | peak week   | NA  | bin_prob | EW202241     | 0.002 |
| EW202242 | ... | ...         | ... | ...      | ...          | ...   |
| EW202242 | WY | peak week   | NA  | bin_prob | EW202320     | 0.013 |

Additionally, suppose that forecasts are required for all states, but are optional for the national level, and that the mean forecasts are optional but all other representations are required.

Again, at a conceptual level we divide these columns into two groups:

### 1. Model task ids

 * `origin_epiweek`: Epidemic week identifiers in the format `"EW<YYYYWW>"`
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
 * `type = "bin_prob"`:
    * if a forecast for a given model task id is present, quantile forecasts are required
    * `type_id` contains strings identifying the bins:
        * probabilities for the following bins are required: `[0.0, 10.0], (10.0, 20.0], (20.0, Inf)`
    * `value` must be a non-negative real number, with values that sum to 1 within each model task

For `"peak week"` targets, we accept the following output representation types:
 * `type = "bin_prob"`:
    * if a forecast for the given model task id is present, bin probabilities are required
    * `type_id` contains strings identifying the bins:
        * probabilities are required for bins corresponding to each epidemic week in the season
    * `value` must be a non-negative real number, with values that sum to 1 within each model task
