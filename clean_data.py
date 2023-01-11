import pandas as pd
import numpy as np

df = pd.read_csv('/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv',
                 low_memory=False)

df.columns = [col.lower().replace(" ", "_") for col in df.columns]

print(df.columns)


def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return float(value.replace("$", "").replace(",", "").replace(" ", ""))


def no_values(val):
    if pd.isna(val):
        return np.NaN


print("number of nan values per attribute:")
print(df.isnull().sum())
print("---------------------------------------------")
df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))
df["service_fee"] = df["service_fee"].apply(lambda x: remove_dollar_sign(x))
df["host_identity_verified"] = df["host_identity_verified"].apply(lambda x: no_values(x))
df["neighbourhood"] = df["neighbourhood"].apply(lambda x: no_values(x))
df["country"] = df["country"].apply(lambda x: no_values(x))
df["cancellation_policy"] = df["cancellation_policy"].apply(lambda x: no_values(x))
df["last_review"] = df["last_review"].apply(lambda x: no_values(x))
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].apply(lambda x: no_values(x))
df["license"] = df["license"].apply(lambda x: no_values(x))

row = df.isnull().sum(axis=1).tolist()

print("number of nan values per row:")
count = 0
for element in row:
    if element == 0:
        print(element)
    elif element < 7:
        print(element)
    else:
        count = count + 1
        print(str(count))


# check data it do be messed up, there are some fake dates
# delete license, country, country_code doesnt give any info
