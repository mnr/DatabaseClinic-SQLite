CREATE TABLE demographicSplit AS
SELECT CAEA.Age Age, CAEA.Gender Gender, EducationalAttainment,  
      	sum(PopulationCount) / lookup.TotalPopCount AS coefficient
FROM 'CA_Educational_Attainment___Personal_Income_2008-2014' CAEA
JOIN 
   (SELECT Age, Gender, CAST(sum(PopulationCount) as REAL) AS TotalPopCount
   FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
   GROUP BY Age, Gender) AS lookup 
   ON 
     CAEA.Age = lookup.Age 
	 AND CAEA.Gender = lookup.Gender
GROUP BY CAEA.Age,CAEA.Gender,EducationalAttainment