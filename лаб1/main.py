import pandas as pd, random
from concurrent.futures import ProcessPoolExecutor as Pool

countOfFiles = 5
categoryList = ("A", "B", "C", "D")
csv_files = []


for i in range(1, countOfFiles+1):
    data = {
        "category": [random.choice(categoryList)],
        "value": [round(random.random() * 100, 3)]
    }
    df = pd.DataFrame(data)
    fileName = f"file{i}.csv"
    df.to_csv(fileName, index=False)
    csv_files.append(fileName)


def processing(fileName):
    df = pd.read_csv(fileName)
    return df.iloc[0]["category"], df.iloc[0]["value"]


if __name__ == "__main__":
    with Pool(max_workers=countOfFiles) as executor:
        results = list(executor.map(processing, csv_files))

    full_df = pd.DataFrame(results, columns=["category", "value"])

    stats = full_df.groupby("category")["value"].agg(
        median="median",
        std="std"
    ).reset_index()

    print("По категориям")
    print(stats.fillna(0))

    
    median_values = stats["median"]

    result = pd.DataFrame({
        "category": stats["category"],
        "median_of_medians": [median_values.median()] * len(stats),
        "std_of_medians": [median_values.std()] * len(stats)
    })

    print("\nМедиана медиан и std медиан")
    print(result)