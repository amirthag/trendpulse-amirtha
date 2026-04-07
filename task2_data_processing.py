# Importing the required libraries
import pandas as pd
import os
import glob

# step 1: Find the latest JSON file inside the data folder
json_files=glob.glob("data/trends_*.json")
if not json_files:
    print("No JSON files found in the data folder.")
    exit()

# Getting the latest file
latest_file=max(json_files,key=os.path.getctime)

#Loading the JSON file into a DataFrame
df=pd.read_json(latest_file)
print(f"Loaded {len(df)} stories from {latest_file}")


# step 2: Data Cleaning
# 1. Removing duplicated based on the post_id
df=df.drop_duplicates(subset="post_id")
print(f"After removing duplicates, {len(df)}")

# 2. Remove rows with missing important fields
df=df.dropna(subset=["post_id","title","score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types 
df["score"]=df["score"].astype(int)
df["num_comments"]=df["num_comments"].fillna(0).astype(int)

# 4. Remove low qulaity stories (score < 5)
df=df[df["score"]>=5]
print(f"After removing low scores: {len(df)}")

# 5. Remove extra whitespace from title
df["title"]=df["title"].str.strip()


# step 3: Save as CSV
#To ensure the data folder exists
os.makedirs("data",exist_ok=True)

#save cleaned data
output_file="data/trends_clean.csv"
df.to_csv(output_file,index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# step 4: Summary

print("\nStories per category:")
print(df["category"].value_counts())
