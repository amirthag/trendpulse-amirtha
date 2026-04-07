# Importing the required libraries
import pandas as pd
import numpy as np
import os

# step 1: Load and explore the data
file_path="data/trends_clean.csv"

# Check if the file exists
if not os.path.exists(file_path):
    print("CSV file not found. Please run Task 2 first.")
    exit()

# Load CSV
df=pd.read_csv(file_path)

# Print shape
print(f"Loaded Data: {df.shape}")

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate averages
avg_score=df["score"].mean()
avg_comments=df["num_comments"].mean()
print(f"\nAverage Score: {int(avg_score)}")
print(f"Average Comments: {int(avg_comments)}")


# step 2: Analysis using Numpy
scores=df["score"].values

mean_score=np.mean(scores)
median_score=np.median(scores)
std_score=np.std(scores)

max_score=np.max(scores)
min_score=np.min(scores)

print("\n---Numpy Analysis---")
print(f"Mean Score: {int(mean_score)}")
print(f"Median Score: {int(median_score)}")
print(f"Standard Deviation: {int(std_score)}")
print(f"Max Score: {int(max_score)}")
print(f"Min Score: {int(min_score)}")

# catogory with most stories
category_counts=df["category"].value_counts()
top_category=category_counts.idxmax()
top_count=category_counts.max()

print(f"\nMost stores in : {top_category} ({top_count} stories)")

# Story with most comments
max_comments_row=df.loc[df["num_comments"].idxmax()]

print(f"\nMost commented story: '{max_comments_row['title']}' - {max_comments_row['num_comments']} comments")


# step 3: Add new columns
df["engagement"]=df["num_comments"]/(df["score"]+1) 

# popularity flag
df["is_popular"]=df["score"]> avg_score


# step 4: save to CSV

output_file="data/trends_analysis.csv"
df.to_csv(output_file,index=False)
print(f"\nSaved to {output_file}")
