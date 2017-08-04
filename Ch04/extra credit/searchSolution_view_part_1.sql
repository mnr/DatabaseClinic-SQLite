/* This is the subquery that is used in searchSolution_2

It produces a view with two columns:
- county
... and ...
- female population

To view the result of the view, use "SELECT * FROM female_population_view"

*/

CREATE VIEW female_population_view AS
select `County Name` as Female_Cty,
            sum(population) as Female_Pop
from secondTable
where Year = 2014 and gender = 'Female'
group by `County Name`