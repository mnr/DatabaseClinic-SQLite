/* This is the subquery that is used in searchSolution_2

It produces a table with two columns:
- county
... and ...
- female population

It also has two optional commented lines at the start
when uncommented...
The first creates a table from the select
The second creates a view from the select
To view the result of the view, use "SELECT * FROM female_population_view"

*/

-- CREATE TABLE female_population_table AS
-- CREATE VIEW female_population_view AS
select `County Name` as Female_Cty,
            sum(population) as Female_Pop
from secondTable
where Year = 2014 and gender = 'Female'
group by `County Name`