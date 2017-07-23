CREATE TABLE demandFor2015Plus AS
SELECT Year, EducationalAttainment, CAST(sum(coefficient * Population) AS INTEGER) AS Demand
FROM 'CA_DRU_proj_2010-2060' DRU
JOIN demographicSplit ON DRU.Gender = demographicSplit.Gender
    AND demographicSplit.Age = CASE
		      WHEN CAST (DRU.Age as INTEGER) < 18 THEN '00 to 17'
			  WHEN CAST (DRU.Age as INTEGER) < 65 THEN '18 to 64'
			  ELSE '65 to 80+'
		END
GROUP BY Year, EducationalAttainment