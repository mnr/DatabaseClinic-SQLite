CREATE TABLE finalSolutionForPlot AS

SELECT substr(Year,7,4) AS Year, EducationalAttainment, CAST(sum(PopulationCount) AS INTEGER) AS Demand
FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
GROUP BY Year,EducationalAttainment

UNION

SELECT Year, EducationalAttainment, CAST(sum(coefficient * Population) AS INTEGER) AS Demand
FROM 'CA_DRU_proj_2010-2060' DRU
JOIN demographicSplit ON DRU.Gender = demographicSplit.Gender
    AND demographicSplit.Age = CASE
		      WHEN CAST (DRU.Age as INTEGER) < 18 THEN '00 to 17'
			  WHEN CAST (DRU.Age as INTEGER) < 65 THEN '18 to 64'
			  ELSE '65 to 80+'
		END
WHERE CAST(Year AS INTEGER)  > 2014
GROUP BY Year, EducationalAttainment