# importing the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# step 1: load data & setup
file_path = "data/trends_analysis.csv"

# check if file exists
if not os.path.exists(file_path):
    print("File not found. Please run Task 3 first.")
    exit()

# load CSV
df = pd.read_csv(file_path)

# create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)

# chart 1: Top 10 stories by score
# get top 10 stories
top10=df.sort_values(by="score",ascending=False).head(10)

# shorten long titles
top10["short_title"]=top10["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(10,6))
plt.barh(top10["short_title"],top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis() 

# save chart
plt.savefig("outputs/chart1_top10_scores.png")
plt.close()

# chart 2: stories per category
category_counts=df["category"].value_counts()
plt.figure(figsize=(8,5))
plt.bar(category_counts.index,category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

# save chart
plt.savefig("outputs/chart2_categories.png")
plt.close()

# chart 3: score vs comments
# separate popular and non-popular
popular=df[df["is_popular"]==True]
not_popular=df[df["is_popular"]==False]

plt.figure(figsize=(8,6))
plt.scatter(popular["score"],popular["num_comments"],label="Popular")
plt.scatter(not_popular["score"],not_popular["num_comments"],label="Not Popular")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

# save chart
plt.savefig("outputs/chart3_scatter.png")
plt.close()


# Bonus: Dashboard

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axs[0].barh(top10["short_title"], top10["score"])
axs[0].set_title("Top Stories")
axs[0].set_xlabel("Score")
axs[0].invert_yaxis()

# Chart 2 in dashboard
axs[1].bar(category_counts.index, category_counts.values)
axs[1].set_title("Categories")
axs[1].set_xlabel("Category")

# Chart 3 in dashboard
axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")
axs[2].set_xlabel("Score")
axs[2].set_ylabel("Number of Comments")
axs[2].legend()

# overall title
plt.suptitle("TrendPulse Dashboard")

# save dashboard
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved in the outputs folder!")