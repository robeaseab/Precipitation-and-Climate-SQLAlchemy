# Precipitation-and-Climate-SQLAlchemy
![precipitation](https://raw.githubusercontent.com/robeaseab/Precipitation-and-Climate-SQLAlchemy/master/precipitation.png)

For this project I used Python and SQLAlchemy to do climate analysis and data exploration of a climate database. The analysis was completed using only SQLAlchemy, ORM queries, Sqlite, Pandas, and Matplotlib.

* Using SQLAlchemy connected to my sqlite database and reflected my tables into classes and saved a reference to those classes.
* Designed a query to retrieve the last 12 months of precipitation data and selected values under analysis.
* Loaded the query results into a Pandas DataFrame and set the index to the date column.
* Sorted the DataFrame values by `date`.
* Plotted the results using the DataFrame `plot` method.
* Used Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designed a query to calculate the total number of stations.
* Designed a query to find the most active stations.
* Listed the stations and observation counts in descending order using `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.
* Designed a query to retrieve the last 12 months of temperature observation data (tobs).
* Filtered by the station with the highest number of observations.
* Plotted the results as a histogram with `bins=12`.

* Designed a Flask API based on the queries that you have just developed.
* Used FLASK to create your routes, which included: 
  * `/` : Home page; Lists all routes that are available.
  * `/api/v1.0/precipitation` : Converted the query results to a Dictionary using `date` as the key and `prcp` as the value; Returned the JSON representation of my dictionary.
  * `/api/v1.0/stations`: Returned a JSON list of stations from the dataset.  Used Flask `jsonify` to convert your API data into a valid JSON response object.
  * `/api/v1.0/tobs`: Returned a query for the dates and temperature observations from a year from the last data point; Return a JSON list of Temperature Observations (tobs) for the previous year.
  * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returned a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range; When given the start only, calculated `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

* I used function to calculate the min, avg, and max temperatures for the selected date trips using the matching dates from the previous year.  Plotted the min, avg, and max temperature from your previous query as a bar chart.
  * Used the average temperature as the bar height.
  * Used the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

### Daily Rainfall Average.

* Calculated the rainfall per weather station using the previous year's matching dates.
* Calculated the daily averages for the min, avg, and max temperatures.
* Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.
* Loaded the list of daily normals into a Pandas DataFrame and set the index equal to the date, and used Pandas to plot the daily normals.

