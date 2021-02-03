import requests

urls = [
    'https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv',
    'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv',
    'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv',
    'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
    'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv',
    'https://epistat.sciensano.be/Data/COVID19BE_tests.csv'
]

for i in urls:

    target_csv_path = i[(i.find('/COVID19BE_') + 1):].lower()
    response = requests.get(i)
    response.raise_for_status()

    with open(target_csv_path, "wb") as f:
        f.write(response.content)

print("Download ready.")
