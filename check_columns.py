import pandas as pd

# CSV file पढ़ो
df = pd.read_csv("crime_data_fixed.csv")

# Column names print करो
print("Column Names:")
print(df.columns)
