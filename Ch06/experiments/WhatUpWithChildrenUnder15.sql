-- None of the educationalAttainments for children under 15 have values
-- This SQL checks to make sure that is true
select EducationalAttainment, sum(PopulationCount)
from 'CA_Educational_Attainment___Personal_Income_2008-2014'
group by EducationalAttainment
-- someone created that split - but forgot to include the data!