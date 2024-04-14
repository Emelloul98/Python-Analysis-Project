import pandas as pd
import numpy as np

def repeated_movie_titles(
        fn_movies: str,
) -> pd.DataFrame:
    """
    Identify the movie titles (column name `original_title`) that appear more than once in the movie dataset.

    Args:
        fn_movies: filename of the movies dataset (CSV file)

    Returns:
        DataFrame with columns 'original_title', 'n_movies', sorted by 'n_movies' in descending order.
            `n_movies` is the number of times the movie title appears in the dataset.
            Only include movies that appear more than once.
    """
     # Read the movies dataset from the given file name
    df = pd.read_csv(fn_movies)
    
    # Group by 'original_title' and count occurrences to find repeated movies
    group_df = df.groupby('original_title').size().reset_index(name='n_movies')
    
    # Sort the DataFrame by the number of movies in descending order
    sorted_df = group_df.sort_values(by='n_movies', ascending=False, ignore_index=True)
    
    # Return only rows where the number of movies is greater than 1 (repeated movies)
    return sorted_df[sorted_df.n_movies > 1]
    
    

def actors_in_top_movies(
        fn_movies: str,
        fn_actors: str,
        n_movies: int = 2,
        revenue_weight: float = 0.5,
        vote_weight: float = 0.5,
        budget_weight: float = 0.5,
) -> pd.DataFrame:
    """
    Use the weights to calculate the score for each movie and identify the top n_movies.
    The score is calculated as follows:
    score = revenue * revenue_weight + vote * vote_weight + budget * budget_weight
    Then, identify the actors who appeared in those movies.
    Return a DataFrame with the following columns:
     - Movie name
     - Movie score (rounded to 1 decimal place)
     - Actor name
    The DataFrame should be sorted by movie score in descending order, and then by actor name in ascending order.
    Each movie will appear in this DataFrame many times - once for each actor who appeared in the movie.
    For example, if the top-rating movie has 3 actors, and the second top-rating movie has 2 actors,
    and we call this function with `n_movies=2`, the DataFrame will have 5 rows.


    Args:
        fn_movies: filename of the movies dataset (CSV file)
        fn_actors: filename of the actors dataset (CSV file)
        n_movies: number of top movies to return

    Returns:
        DataFrame with columns "Movie name", "Movie score", "Actor name".
        Note that the columns should be in the order specified above, and the names should be as specified above.
        Keep in mind the sorting requirements specified above.

    """
    # Read the movies and actors datasets from the given file names
    df1 = pd.read_csv(fn_movies)
    df2 = pd.read_csv(fn_actors)
    
    # Define a scoring formula based on provided weights
    formula = lambda x: (x['revenue'] * revenue_weight) + (x['vote_count'] * vote_weight) + (x['budget'] * budget_weight)
    
    # Calculate scores for each movie using the scoring formula
    new_movies = df1.assign(score=df1.apply(formula, axis=1))
    
    # Select top N movies based on calculated scores
    top_n = new_movies.sort_values(by='score', ascending=False).head(n_movies)
    
    # Merge top movies with actors dataset based on movie titles
    merged_df = pd.merge(df2, top_n, left_on='movie_title', right_on='original_title', how='left').sort_values(by=['score', 'actor_name'], ascending=[False, True], ignore_index=True)
    
    # Round the scores to one decimal place
    merged_df['score'] = merged_df['score'].round(1)
    
    # Select necessary columns and filter out rows with non-positive scores
    right_col = merged_df[['movie_title', 'score', 'actor_name']]
    right_row = right_col[right_col.score > 0].copy()
    
    # Rename columns for clarity
    right_row.rename(columns={'movie_title': 'Movie name', 'score': 'Movie score', 'actor_name': 'Actor name'}, inplace=True)
    
    # Reset the index of the resulting DataFrame
    right_row.reset_index(drop=True)
    
    # Return the DataFrame with actors in top-rated movies
    return right_row

def actors_with_most_collaborations(
        fn_actors: str,
        n_actors: int = 5,
) -> pd.DataFrame:
    """
    Identify the actors who have played alongside the greatest number of unique actors.
    For example, if I have acted in 1 movie with 3 actors, and in another movie with 3 different actors,
    then I have acted with 6 unique actors.

    Tip: use merge to join the actors DataFrame with itself, and then count the number of unique actors for each pair.

    Args:
        fn_actors: filename of the actors dataset (CSV file)
        n_actors: number of top actors to return

    Returns:
        DataFrame with columns 'actor_name', 'n_movies', sorted by 'n_movies' in descending order.
        `actor_name` is the name of the actor, and `n_movies` is the integer number of unique actors
        the actor has played with.

    """
    # Read the actors dataset from the given file name
    df = pd.read_csv(fn_actors)
    
    # Drop rows with null actor names
    df = df.dropna(subset=['actor_name'])
    
    # Merge the dataset with itself based on movie titles
    merged_df = pd.merge(df, df, on='movie_title')
    
    # Exclude rows where actor_name_x and actor_name_y are the same (self-collaboration)
    merged_df = merged_df[merged_df['actor_id_x'] != merged_df['actor_id_y']]
    
    # Group by 'actor_name_x' and count the unique collaborations
    collaboration_counts = merged_df.groupby('actor_name_x')['actor_name_y'].nunique().reset_index()
    
    # Rename columns for clarity
    collaboration_counts.columns = ['actor_name', 'n_movies']
    
    # Sort the DataFrame based on the collaboration counts in descending order
    collaboration_counts = collaboration_counts.sort_values(by='n_movies', ascending=False, ignore_index=True)
    
    collaboration_counts.rename(columns={'actor_name': 'actor_name','n_movies':'n_collaborators'}, inplace=True)
    
    # Return the top N actors with the most collaborations
    return collaboration_counts.head(n_actors)


def highest_grossing_movies_by_year(
        fn_movies: str,
        n_movies_per_year: int = 5,
) -> pd.DataFrame:
    """
    Identify the highest-grossing movie for each of the top n_years based on total revenue.
    The function should return a DataFrame with the following columns:
     - Year: integer year
     - Movie Name: as specified by the `original_title` column in the movies dataset
     - Movie Revenue: as specified by the `revenue` column in the movies dataset
     - Average Revenue: average revenue for that year
     - Standard Deviation of Revenue: standard deviation of revenue for that year
     - Number of Movies: number of movies in that year

    The DataFrame should be sorted by Year in ascending order, then by Movie Revenue in descending order.
    For each year, only include the top n_movies_per_year based on Movie Revenue. If there are fewer than
    n_movies_per_year, include all movies for that year. Ties should be broken by Movie Name in ascending order.

    Args:
        fn_movies: filename of the movies dataset (CSV file)
        n_movies_per_year: number of top movies per year to return

    Returns:
        DataFrame with columns as specified above

    """
    # Read the movies dataset from the given file name
    my_df = pd.read_csv(fn_movies)

    # Convert 'release_date' column to datetime, specifying format as 'mixed'
    my_df['release_date'] = pd.to_datetime(my_df['release_date'], errors='coerce', format='mixed')


    # Exclude rows with null values in the 'release_date' column
    my_df = my_df.dropna(subset=['release_date'])

    # Extract year from 'release_date' and create a new column 'Year'
    my_df['Year'] = my_df['release_date'].dt.year

    # Define columns for the new DataFrame
    my_columns = ['Year', 'Movie Name', 'Movie Revenue', 'Average Revenue', 'Standard Deviation of Revenue', 'Number of Movies']

    # Initialize an empty list to store rows
    rows = []

    # Group movies by 'Year'
    grouped_by_year = my_df.groupby('Year')

    # Iterate over each group (year) and select the top n movies with the highest revenue
    for group_name, group_data in grouped_by_year:
        # Sort movies in the group by revenue in descending order
        sorted_group_data = group_data.sort_values(by='revenue', ascending=False)
        
        # Take the top n movies or all movies if there are fewer than n_movies_per_year
        top_movies = sorted_group_data.head(n_movies_per_year)
        
        # Sort the top movies by movie name in ascending order to handle ties
        top_movies = top_movies.sort_values(by='original_title', ascending=True,kind='mergesort')
        
        # Calculate summary statistics for the year
        total_revenue = group_data['revenue'].sum()
        average_revenue = group_data['revenue'].mean()
        std_revenue = group_data['revenue'].std()
        num_movies = len(group_data)

        # Append rows for each of the top movies
        for index, movie in top_movies.iterrows():
            new_row = {
                'Year': int(group_name),
                'Movie Name': movie['original_title'],
                'Movie Revenue': movie['revenue'],
                'Average Revenue': average_revenue,
                'Standard Deviation of Revenue': std_revenue,
                'Number of Movies': num_movies
            }
            rows.append(new_row)

    # Convert the list of rows to a DataFrame
    new_df = pd.DataFrame(rows)

    # Sort the DataFrame based on the Year and Movie Revenue
    sorted_df = new_df.sort_values(by=['Year', 'Movie Revenue'], ascending=[True, False],kind='mergesort',ignore_index=True)

    return sorted_df






## Extra Credit. You will not get more than 100 points for this assignment, but if you have errors in the previous
## functions, you can still get points for this one.

def actors_with_highest_median_score(
        fn_movies: str,
        fn_actors: str,
        n_actors: int = 5,
) -> pd.DataFrame:
    """

    Identify the actors with the highest median vote_average score.
    To do so, you will need to merge the movies and actors datasets, and then calculate the median score for each actor.


    The function should return a DataFrame with the following columns:
     - Actor Name
     - Median Vote Average
    The DataFrame should be sorted by Median Vote Average in descending order.

    Args:
        fn_movies: filename of the movies dataset (CSV file)
        fn_actors: filename of the actors dataset (CSV file)
        n_actors: number of top actors to return

    Returns:
        DataFrame with columns as specified above

    """
    # Read the movies and actors datasets from the given file names
    movies_df = pd.read_csv(fn_movies)
    actors_df = pd.read_csv(fn_actors)
    
    # Merge datasets based on original movie title and movie title
    merged_df = pd.merge(movies_df, actors_df, left_on='original_title', right_on='movie_title', how='inner')
    
    # Drop rows with null vote_average scores
    merged_df = merged_df.dropna(subset=['vote_average'])
    
    # Group by actor name and calculate median vote_average score
    actor_median_scores = merged_df.groupby('actor_name')['vote_average'].median().reset_index()
    
    # Sort actors by median vote_average score in descending order
    actor_median_scores = actor_median_scores.sort_values(by='vote_average', ascending=False, ignore_index=True)
    
    # Select top N actors
    top_actors = actor_median_scores.head(n_actors).copy()  # Create a copy of the DataFrame
    
    # Rename columns for clarity
    top_actors.rename(columns={'actor_name': 'Actor Name', 'vote_average': 'Median Vote Average'}, inplace=True)
    
    # Return the DataFrame with actors having the highest median vote_average score
    return top_actors
