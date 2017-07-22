# Averages and Calculations

In this challenge, we are asked to forecast the educational demand for California up to the year 2060.

We are provided with two datasets:
1. [CA Educational Attainment & Personal Income](https://data.ca.gov/dataset/ca-educational-attainment-personal-income) will provide education information
2. [California Population Projection by County, Age, and Ethnicity dataset for 2010-2060](https://data.ca.gov/dataset/california-population-projection-county-age-gender-and-ethnicity/resource/cd0453ba-a6db-4542#{}) will provide population forecasts up to 2060.

We will have to link those datasets and create a table that forecasts the demand for each level of education for each year:

| Year | Educational Attainment | Actual or Forecast Demand |
|---|---|---|
| 2008 | "Children under 15" | A number equaling the population of this segment |
| 2008 | "No high school diploma" | A number equaling the population of this segment |
| 2008 | "High school or equivalent" | A number equaling the population of this segment |
| 2008 | "Some college, less than 4-yr degree" | A number equaling the population of this segment |
| 2008 | "Bachelor's degree or higher" | A number equaling the population of this segment |

## MNR Notes
I make a choice to use actual data for years < 2015 and forecast for years 2015->2060.

The SQL for data < 2015 is in [create_demandFor2015Minus.sql](create_demandFor2015Minus.sql)

To generate the forecast for 2015->2060, I use the following process...

Given:
* Age
* Gender
* Population

Return the division of that population into the five different educational attainments.

This requires the calculation of coefficients for each age/gender/attainment combination. Here's the [SQLite to generate that table](create_demographicSplit.sql)


Then for each year/age/gender in DRU, divide the population of that demographic into five lines predicting the educational attainment for each demographic slice. [Here's the sql for that table](create_demandFor2015Plus).

It's possible to combine both factual data and forecast in one [SQL program](entireDemandReport.sql).
