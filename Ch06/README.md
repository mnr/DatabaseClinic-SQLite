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

Here's the SQL for the data < 2015:

    CREATE TABLE demandFor2015Minus AS
    SELECT substr(Year,7,4) AS Year, EducationalAttainment, PopulationCount AS Demand
    FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
    GROUP BY Year,EducationalAttainment

To generate the forecast for 2015->2060, I use the following process...

Given:
* Age
* Gender
* Population

Return the division of that population into the five different educational attainments.

This requires the calculation of coefficients for each age/gender/attainment combination. Here's the SQLite to generate that table:

    CREATE TABLE demographicSplit AS
    SELECT Age, Gender, EducationalAttainment,
    sum(PopulationCount) /
      (SELECT sum(PopulationCount)
	     FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
	     GROUP BY Age, Gender) AS coefficient
    FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
    GROUP BY Age,Gender,EducationalAttainment

Then for each year/age/gender in DRU, divide the population of that demographic into five lines predicting the educational attainment for each demographic slice.

    CREATE TABLE demandFor2015Plus AS
    SELECT Year, EducationalAttainment, CAST(sum(coefficient * Population) AS INTEGER) AS Demand
    FROM 'CA_DRU_proj_2010-2060' DRU
    JOIN demographicSplit ON DRU.Gender = demographicSplit.Gender
       AND demographicSplit.Age = CASE
		    WHEN CAST (DRU.Age as INTEGER) < 18 THEN '00 to 17'
			  WHEN CAST (DRU.Age as INTEGER) < 65 THEN '18 to 64'
			  ELSE '65 to 80+'
	  END
    WHERE CAST(Year AS INTEGER) > 2014
    GROUP BY Year, EducationalAttainment



# below is scratch
    CREATE TABLE EduAttCoef AS
    SELECT Age, Gender, EducationalAttainment, CAST (sum(PopulationCount ) / 190366967 AS REAL) as Coefficient
    FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
    GROUP BY Age,Gender,EducationalAttainment




### First:
get coefficients for age/gender/EducationalAttainment (Note: 190366967 is the sum of population for CA_Educational_Attainment___Personal_Income_2008-2014)

    CREATE TABLE EduAttCoef AS
    SELECT Age, Gender, EducationalAttainment, CAST (sum(PopulationCount ) / 190366967 AS REAL) as Coefficient
    FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
    GROUP BY Age,Gender,EducationalAttainment

### Second:
attach those coefficients to CA_DRU... and create a table with population forecasts

    SELECT Year, EducationalAttainment, Population, Coefficient * Population AS ForecastDemand
    FROM 'CA_DRU_proj_2010-2060' DRU
    JOIN EduAttCoef ON  DRU.Gender = EduAttCoef.Gender
       AND EduAttCoef.Age = CASE
		          WHEN CAST (DRU.Age as INTEGER) < 18 THEN '00 to 17'
						  WHEN CAST (DRU.Age as INTEGER) < 65 THEN '18 to 64'
						  ELSE '65 to 80+'
						END
    WHERE Year = 2020
    GROUP BY Year, EducationalAttainment


    getPopulations(interestingYear) {
      if (interestingYear < 2015) {
        # we have actual data for these years
        doSQLite(
          SELECT EducationalAttainment,PopulationCount
          FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
          WHERE Year IS '01/01/2008 12:00:00 AM'
          GROUP BY EducationalAttainment
        )
      } else {
        # we have to forecast for years 2015->2060


      }
    }


## Discrepancies in the datasets
Relating the two datasets is a hidden challenge.

### First:
_Age in CA Educational…_ is in ranges. Age in _California Population Projection_ is in exact integers. I'll need to create a field in _Projections_ that assigns Projections.Age to the range corresponding to the range in Educational.Age. For example, if Projections.Age = 20, that would correspond to Education.Age = "18 to 64"

### Second:
Population in Ca Population projection is by County. Population in CA Educational is for entire California. I’ll need to aggregate the population from CA Population Projection.

### Third:
Use the aggregate sum of Male and Female per year. Also use the aggregate sum of race
