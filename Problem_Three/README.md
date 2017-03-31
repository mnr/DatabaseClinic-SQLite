# Problem 3 : Search a Database

The problem we've been given is to search [California Population Projections](https://data.ca.gov/dataset/california-population-projection-county-age-gender-and-ethnicity/resource/cd0453ba-a6db-4542#{}) and create a report showing the male and female population for each California county in the year 2014.

Be aware that the FORMAT of the report IS IMPORTANT. Your results should have these columns and rows. The solution should look something like this:

| Year:2014 | Male | Female |
| ---|---|---|
| Alameda | sum of male population | sum of female population |
| Amador | sum of male population | sum of female population |
| etc... |  sum of male population | sum of female population |

This is actually more difficult than it seems at first. The SQL to get the numbers is fairly easy. Here's the sql to do that...

```
select
   county_name,
   gender,
   sum(population)
from populationProjection
where Year = "01/01/2014 12:00:00 AM"
group by county_name, gender
order by county_name, gender
```

but formatting the report in the way specified makes this much more difficult. To solve it, I had to include a sub-query. I explain it in the video, but it looks like this...
```
select
   county_name as "Year.2014",
   sum(populationProjection.population) as 'Male',
   Fem_Pop as 'Female'
from ( select
      county_name as Fem_Cty,
			sum(population) as Fem_Pop
			from populationProjection
			where Year = "01/01/2014 12:00:00 AM"
            and gender = 'Female'
            group by county_name
			)
inner join  populationProjection
on Fem_Cty = populationProjection.county_name
where Year = "01/01/2014 12:00:00 AM"
and gender = 'Male'
group by county_name
order by county_name
```
