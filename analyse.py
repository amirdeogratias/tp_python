import pandas as pd
import json

with open("catalogue.json", "r") as f:
    data = json.load(f)
#print(data)
df = pd.DataFrame(data)
print(df)
df = df.explode("albums")
albums_df = pd.json_normalize(df["albums"])
df_final = df.drop(columns=["albums"]).join(albums_df)
print(albums_df)