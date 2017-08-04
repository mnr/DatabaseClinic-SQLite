/* This is the subquery that is used in searchSolution_2

It produces a table with two columns:
- county
... and ...
- female population

*/

CREATE TABLE female_population_table AS
select `County Name` as Female_Cty,
            sum(population) as Female_Pop
from secondTable
where Year = 2014 and gender = 'Female'
group by `County Name`