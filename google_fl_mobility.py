# -*- coding: utf-8 -*-
# %% [markdown]
"""
## [Google Mobility Data](https://www.google.com/covid19/mobility/)

https://www.google.com/covid19/mobility/data_documentation.html?hl=en

According to Google:

> These reports show how visits and length of stay at different places change
> compared to a baseline. We calculate these changes using the same kind of
> aggregated and anonymized data used to show popular times for places in Google
> Maps.
> - The baseline is the median value, for the corresponding day of the week,
>   during the 5-week period Jan 3–Feb 6, 2020.
> - The reports show trends over several weeks with the most recent data
>   representing approximately 2-3 days ago—this is how long it takes to produce
>   the reports.
"""


# %%
import pandas as pd

mobility = pd.read_csv(
    "https://storage.googleapis.com/covid19-open-data/v2/mobility.csv"
)

mobility.head()

# %%
fl = mobility[mobility.key.str.startswith("US_FL").fillna(False)].copy()

fl.key.unique()

fl.tail()

# %%
def goog_cleanup(df):
    df.date = df.date.apply(pd.to_datetime)

    mobility = []

    for name in list(df.columns):
        name = name.replace("mobility_", "")
        print(name)
        mobility.append(name)

    df.columns = mobility

    df["key"] = df.key.str.replace("US_FL_", "")

    df = df.query("key != 'US_FL'").copy()

    df["key"] = df["key"].astype(str).astype(int)

    df = df.reset_index(drop=True)

    FLORIDA = pd.read_csv(
        "https://raw.githubusercontent.com/danielcs88/covid-19/master/data/florida_county_population.csv"
    )

    def county_name(fips):
        """
        Returns county name for FIPS code.
        """

        keys = list(FLORIDA["FIPS"])
        values = list(FLORIDA.county)
        counties = dict(zip(keys, values))

        county = counties.get(fips)

        return county

    df["county"] = df.apply(lambda x: county_name(x["key"]), axis=1)

    df = df.rename(columns={"key": "fips"})

    df = df[
        [
            "date",
            "fips",
            "county",
            "retail_and_recreation",
            "grocery_and_pharmacy",
            "parks",
            "transit_stations",
            "workplaces",
            "residential",
        ]
    ]

    return df


# %%
fl = goog_cleanup(fl)

# %%
print(fl)

# %%
fl.to_csv("google_fl_mobility.csv", index=False)
