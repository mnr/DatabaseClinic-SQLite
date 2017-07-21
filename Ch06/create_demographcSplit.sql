CREATE TABLE demographicSplit AS 
 SELECT Age, Gender, EducationalAttainment,
    sum(PopulationCount) / 
      (SELECT sum(PopulationCount)
	     FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
	     GROUP BY Age, Gender) AS coefficient
    FROM 'CA_Educational_Attainment___Personal_Income_2008-2014'
    GROUP BY Age,Gender,EducationalAttainment