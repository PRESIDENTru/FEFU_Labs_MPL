import pandas as pd, random
from concurrent.futures import ProcessPoolExecutor as Pool

countOfFiles = 5
countOfLines = 5
categoryList = ("A", "B", "C", "D")
csv_files = []


for i in range(1, countOfFiles+1):
    data = {
        "category": [random.choice(categoryList) for _ in range(countOfLines)],
        "value": [round(random.random() * 100, 3) for _ in range(countOfLines)]
    }
    df = pd.DataFrame(data)
    fileName = f"file{i}.csv"
    df.to_csv(fileName, index=False)
    csv_files.append(fileName)


def processing(fileName):
    df = pd.read_csv(fileName)
    medianAndStd = df.groupby("category")["value"].agg(
        median="median",
        std="std"
    )
    return fileName, medianAndStd


if __name__ == "__main__":
    with Pool(max_workers=countOfFiles) as executor:
        results = list(executor.map(processing, csv_files))

    print("Результаты по каждому файлу")
    for fileName, df in results:
        print(f"\nФайл: {fileName}")
        print(df)

    full_df = pd.concat([df for _, df in results])

    result = full_df.groupby("category")["median"].agg(
        median="median",
        std="std"
    )

    print("\nМедиана из медиан и стандартное отклонение медиан")
    print(result)