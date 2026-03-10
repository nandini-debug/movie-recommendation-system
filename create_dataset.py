import csv
import pandas as pd

# -------- MOVIE DATA --------

movies_data = [
["movie_id","title"],
["27205","Inception"],
["19995","Avatar"],
["157336","Interstellar"],
["155","The Dark Knight"],
["299536","Avengers: Infinity War"],
["603","The Matrix"],
["597","Titanic"],
["13","Forrest Gump"],
["680","Fight Club"],
["1891","The Empire Strikes Back"]
]

# -------- CREATE CSV FILE --------

with open("movie.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerows(movies_data)

print("CSV file created successfully")

# -------- READ CSV USING PANDAS --------

movies = pd.read_csv("movies.csv")

print("\nMovies in dataset:\n")

for i in range(len(movies)):

    title = movies.iloc[i]["title"]

    print(title)