import pandas as pd
import matplotlib.pyplot as plt

# Countries for comparison
countries = [
    "Brazil",
    "China",
    "Japan",
    "United States",
    "France",
    "United Kingdom"
]

# Loading of the World Bank CSV files
exports = pd.read_csv("exports.csv", skiprows=4)
imports = pd.read_csv("imports.csv", skiprows=4)

# Countries chosen based on list
exports = exports[exports["Country Name"].isin(countries)]
imports = imports[imports["Country Name"].isin(countries)]

# Selected years
years = [str(year) for year in range(2000, 2024)]

# Transform the data from wide format to long format
exports_long = exports.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=years,
    var_name="year",
    value_name="exports"
)

imports_long = imports.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=years,
    var_name="year",
    value_name="imports"
)

# Merge exports and imports
df = pd.merge(
    exports_long,
    imports_long,
    on=["Country Name", "Country Code", "year"]
)

# Rename the country column
df = df.rename(columns={"Country Name": "country"})

# Calculate the difference between the exports and imports
df["trade_difference"] = df["exports"] - df["imports"]

# Sort the data
df = df.sort_values(["country", "year"])

# Display the first few rows
print(df.head())


# Chart 1: Exports over time
plt.figure(figsize=(10, 6))

for country in countries:
    country_data = df[df["country"] == country]
    plt.plot(
        country_data["year"],
        country_data["exports"],
        label=country
    )

plt.title("Exports as a Percentage of GDP (2000–2023)")
plt.xlabel("Year")
plt.ylabel("Exports (% of GDP)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("exports_over_time.png")
plt.show()


# Chart 2: Imports over time
plt.figure(figsize=(10, 6))

for country in countries:
    country_data = df[df["country"] == country]
    plt.plot(
        country_data["year"],
        country_data["imports"],
        label=country
    )

plt.title("Imports as a Percentage of GDP (2000–2023)")
plt.xlabel("Year")
plt.ylabel("Imports (% of GDP)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("imports_over_time.png")
plt.show()


# Chart 3: Trade difference
latest_year = df["year"].max()
latest_data = df[df["year"] == latest_year].copy()

plt.figure(figsize=(9, 5))

plt.bar(
    latest_data["country"],
    latest_data["trade_difference"]
)

plt.axhline(0, linewidth=0.8)
plt.title(f"Exports Minus Imports ({latest_year})")
plt.xlabel("Country")
plt.ylabel("Percentage points")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("trade_difference_latest_year.png")
plt.show()

# Save the clean dataset
df.to_csv("trade_data_cleaned.csv", index=False)

print("Analysis complete.")
