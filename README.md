# Movie and Actor Analysis Project

## Overview
This Python project provides functions to analyze movie and actor datasets. It uses pandas and numpy libraries for data manipulation and analysis.

## Functions
### 1. `repeated_movie_titles`
- **Description:** Identifies movie titles that appear more than once in the movie dataset.
- **Input:** CSV file containing movie data.
- **Output:** DataFrame with repeated movie titles sorted by occurrence.

### 2. `actors_in_top_movies`
- **Description:** Calculates scores for movies based on revenue, votes, and budget, then identifies top movies and the actors in them.
- **Input:** CSV files containing movie and actor data, along with optional parameters for weights and number of top movies.
- **Output:** DataFrame with top movies and actors based on specified criteria.

### 3. `actors_with_most_collaborations`
- **Description:** Identifies actors who have collaborated with the greatest number of unique actors.
- **Input:** CSV file containing actor data.
- **Output:** DataFrame with actors and their collaboration counts.

### 4. `highest_grossing_movies_by_year`
- **Description:** Identifies the highest-grossing movie for each year based on total revenue.
- **Input:** CSV file containing movie data, along with optional parameter for the number of top movies per year.
- **Output:** DataFrame with highest-grossing movies for each year.

### 5. `actors_with_highest_median_score` (Extra Credit)
- **Description:** Identifies actors with the highest median vote_average score.
- **Input:** CSV files containing movie and actor data, along with optional parameter for the number of top actors.
- **Output:** DataFrame with top actors based on median vote_average score.

## Usage
1. Ensure you have Python installed along with the pandas and numpy libraries.
2. Import the necessary functions from the provided Python script.
3. Load your movie and actor datasets in CSV format.
4. Call the desired functions with appropriate arguments to perform analysis.

## Example Usage
```python
import pandas as pd
import numpy as np
from movie_actor_analysis import (
    repeated_movie_titles,
    actors_in_top_movies,
    actors_with_most_collaborations,
    highest_grossing_movies_by_year,
    actors_with_highest_median_score,
)

# Load datasets
movies_data = 'movies.csv'
actors_data = 'actors.csv'

# Example usage of functions
repeated_titles = repeated_movie_titles(movies_data)
top_actors_movies = actors_in_top_movies(movies_data, actors_data)
collaborating_actors = actors_with_most_collaborations(actors_data)
highest_grossing = highest_grossing_movies_by_year(movies_data)
top_median_actors = actors_with_highest_median_score(movies_data, actors_data)
```
