CREATE TABLE demandFor2015Minus AS
SELECT substr(Year,7,4) AS Year, EducationalAttainment, sum(PopulationCount) AS Demand
FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
GROUP BY Year,EducationalAttainment
