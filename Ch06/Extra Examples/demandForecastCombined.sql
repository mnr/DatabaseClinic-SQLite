-- this sample combines two steps into one code
-- the steps are:
-- create_demandFor2015Plus.sql
-- and
-- create_demographicSplit.sql

CREATE TABLE testforecast AS
SELECT Year, EducationalAttainment, CAST(sum(coefficient * Population) AS INTEGER) AS Demand
FROM 'CA_DRU_proj_2010-2060' DRU
JOIN  (SELECT CAEA.Age Age, CAEA.Gender Gender, EducationalAttainment,  
      	sum(PopulationCount) / lookup.TotalPopCount AS coefficient
FROM 'CA_Educational_Attainment___Personal_Income_2008-2014' CAEA
JOIN 
   (SELECT Age, Gender, CAST(sum(PopulationCount) as REAL) AS TotalPopCount
   FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
   GROUP BY Age, Gender) AS lookup 
   ON 
     CAEA.Age = lookup.Age 
	 AND CAEA.Gender = lookup.Gender
GROUP BY CAEA.Age,CAEA.Gender,EducationalAttainment) as demographicSplit ON DRU.Gender = demographicSplit.Gender
    AND demographicSplit.Age = CASE
		      WHEN CAST (DRU.Age as INTEGER) < 18 THEN '00 to 17'
			  WHEN CAST (DRU.Age as INTEGER) < 65 THEN '18 to 64'
			  ELSE '65 to 80+'
		END
GROUP BY Year, EducationalAttainment