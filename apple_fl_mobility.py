# -*- coding: utf-8 -*-
# %% [markdown]
#  ## [Apple Mobility Data](https://www.apple.com/covid19/mobility)
# %% [markdown]
#  According to Apple:
#
#  > ### About This Data
#  The CSV file and charts on this site show a relative volume of directions requests per country/region, sub-region or city compared to a baseline volume on January 13th, 2020. We define our day as midnight-to-midnight, Pacific time. Cities are defined as the greater metropolitan area and their geographic boundaries remain constant across the data set. In many countries/regions, sub-regions, and cities, relative volume has increased since January 13th, consistent with normal, seasonal usage of Apple Maps. Day of week effects are important to normalize as you use this data. Data that is sent from users’ devices to the Maps service is associated with random, rotating identifiers so Apple doesn’t have a profile of individual movements and searches. Apple Maps has no demographic information about our users, so we can’t make any statements about the representativeness of usage against the overall population.

# %%
# Querying the API for the latest links

import json
from urllib.request import urlopen
import pandas as pd

with urlopen(
    "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
) as response:
    test = json.load(response)

basePath = test.get("basePath")
csvPath = test.get("regions").get("en-us").get("csvPath")


# %%
aapl_mobility = pd.read_csv("https://covid19-static.cdn-apple.com" + basePath + csvPath)


# %%
aapl_mobility.region.unique()


# %%
fl_aapl = aapl_mobility[aapl_mobility["sub-region"] == "Florida"]

# %%
fl_aapl.region.unique()

# %%
len(fl_aapl.region.unique())

# %%
apple_counties = list(fl_aapl.region.unique()[6:])

# %%
counties = "http://lmsresources.labormarketinfo.com/library/laus/counties/LFS_cnty.xlsx"
df = pd.read_excel(
    counties,
    skiprows=6,
    usecols="A,B,D,F,H,J,L",
#     names=[
#         "county",
#         f"{preliminary}_labor_force",
#         f"{preliminary}_unemp_level",
#         f"{revised}_labor_force",
#         f"{revised}_unemp_level",
#         f"{last_year}_labor_force",
#         f"{last_year}_unemp_level",
#     ],
    skipfooter=10,
)

# %%
deo_counties = list(df.COUNTY)

# %%
[i for i in deo_counties if i not in apple_counties]

# %%
print(diff)

# %%
# mia_aapl = aapl_mobility.query("region == 'Miami'")

# mdc_aapl = aapl_mobility.query("region == 'Miami-Dade County'")


# %%
# mia_aapl.tail()

# %%
fl_aapl.head()


# %%
def apple_tidy(df):
    """
    Cleanup for Apple Mobility Data
    """

    df = df.drop(
        ["geo_type", "alternative_name", "sub-region", "country"], axis="columns",
    )

    #     df = df.T.reset_index()

    #     if len(df.columns) < 4:
    #         df.columns = ["date", "driving"]

    #     else:
    #         df.columns = ["date", "driving", "transit", "walking"]

    #     df = df.drop(index=0)

    #     df["baseline"] = 100

    #     df.date = df.date.apply(pd.to_datetime)

    #     df = df.set_index("date")

    #     df = df.div(100)

    return df


# %%
fl_aapl = apple_tidy(fl_aapl)

# %%
fl_aapl.head()

# %%
fl_aapl.iloc[:, :2]

# %%
fl_aapl.iloc[:, 2:].T

# %%
mdc_aapl = apple_tidy(mdc_aapl)


# %%
mia_aapl = apple_tidy(mia_aapl)


# %%
mia_aapl.plot(title="Apple Mobility Trends: Miami, FL")


# %%
mdc_aapl.plot(title="Apple Mobility Trends: Miami-Dade County")

# %% [markdown]
#  ## [New York Times COVID-19 Data](https://github.com/nytimes/covid-19-data)

# %%
# NY Times
covid_19 = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
    parse_dates=True,
)


# %%
fl = covid_19.query("state == 'Florida'")


# %%
fl.tail(67)


# %%
latest_date = list(covid_19.date.unique())[-1]


# %%
latest_date


# %%
covid_19.query("date == @latest_date").sort_values(
    by=["cases"], ascending=False
).reset_index(drop=True).head(10)


# %%
mdc = covid_19.query("fips == 12086").reset_index(drop=True)


# %%
mdc.date = mdc.date.apply(pd.to_datetime)


# %%
mdc = mdc.set_index("date")


# %%
mdc["new_cases"] = mdc.cases.diff()


# %%
mdc["pct_cases"] = mdc.cases.pct_change()


# %%
mdc["pct_new"] = mdc.new_cases.pct_change()


# %%
mdc["pct_deaths"] = mdc.deaths.pct_change()


# %%
mdc.tail(7)


# %%
mdc.tail(30)


# %%
mia_aapl.tail(1)


# %%
plt.plot(mia_aapl.index, mia_aapl.driving, label="Driving")
plt.plot(mia_aapl.index, mia_aapl.transit, label="Transit")
plt.plot(mia_aapl.index, mia_aapl.walking, label="Walking")
plt.axhline(
    1, xmin=0, xmax=1, color="k", linestyle="dashed",
)
plt.plot(mdc.index, mdc.pct_new, label="Percent Change New COVID-19 Cases")
plt.title("Apple Mobility Trends vs. Percent Change New COVID-19 Cases")
# plt.yscale("log")
plt.legend()
plt.show()
