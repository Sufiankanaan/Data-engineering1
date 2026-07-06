import sys

import pandas as pd
print("arguments", sys.argv)

if len(sys.argv)<2:
    print("ERORR : Enter the month's number. ")
    print ("Example : python pipeline.py 10")
    sys.exit(1)

month = int(sys.argv[1])

df = pd.DataFrame({"day": [1, 2], "num-passengers": [3, 4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")


print(f"Running pipeline for {month} month")