import requests
import pandas as pd
import time

FRED_API_KEY = "33cfb977d2144be5a6e0e2db1e0a2fd2"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def get_fred_annual(series_id, start="2010-01-01", end="2019-12-31"):
    """Pull a FRED series and return annual averages."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start,
        "observation_end": end
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    
    observations = response.json()["observations"]
    df = pd.DataFrame(observations)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["year"] = pd.to_datetime(df["date"]).dt.year
    
    annual = df.groupby("year")["value"].mean().reset_index()
    return annual

# ============================================================
# STATE FIPS MAPPING (needed for some series)
# ============================================================
state_fips = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "FL": "12", "GA": "13",
    "HI": "15", "ID": "16", "IL": "17", "IN": "18", "IA": "19",
    "KS": "20", "KY": "21", "LA": "22", "ME": "23", "MD": "24",
    "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29",
    "MT": "30", "NE": "31", "NV": "32", "NH": "33", "NJ": "34",
    "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45",
    "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VT": "50",
    "VA": "51", "WA": "53", "WV": "54", "WI": "55", "WY": "56",
    "DC": "11"
}

# ============================================================
# PULL STATE-LEVEL DATA
# ============================================================

state_data = {}

for state, fips in state_fips.items():
    print(f"Pulling data for {state}...")
    
    try:
        unemployment = get_fred_annual(f"{state}UR")
        median_income = get_fred_annual(f"MEHOINUS{fips}A672N")
        per_capita_income = get_fred_annual(f"{state}PCPI")
        state_gdp = get_fred_annual(f"{state}NGSP")
        nonfarm_employment = get_fred_annual(f"{state}NA")
        
        for year in range(2010, 2020):
            key = (state, year)
            state_data[key] = {
                "state": state,
                "year": year,
                "state_unemployment": unemployment[unemployment["year"] == year]["value"].values[0] if year in unemployment["year"].values else None,
                "state_median_income": median_income[median_income["year"] == year]["value"].values[0] if year in median_income["year"].values else None,
                "state_per_capita_income": per_capita_income[per_capita_income["year"] == year]["value"].values[0] if year in per_capita_income["year"].values else None,
                "state_gdp": state_gdp[state_gdp["year"] == year]["value"].values[0] if year in state_gdp["year"].values else None,
                "state_nonfarm_employment": nonfarm_employment[nonfarm_employment["year"] == year]["value"].values[0] if year in nonfarm_employment["year"].values else None,
            }
        
        time.sleep(1)  # Be nice to the API
        
    except Exception as e:
        print(f"  ERROR for {state}: {e}")

print(f"\nPulled data for {len(state_data)} (State, Year) pairs")

# ============================================================
# PULL NATIONAL DATA
# ============================================================

print("Pulling national indicators...")

national_unemployment = get_fred_annual("UNRATE")
fed_funds = get_fred_annual("FEDFUNDS")
cpi = get_fred_annual("CPIAUCSL")
mortgage_30yr = get_fred_annual("MORTGAGE30US")
consumer_confidence = get_fred_annual("UMCSENT")
treasury_10yr = get_fred_annual("DGS10")

# ============================================================
# BUILD COMPLETE LOOKUP TABLE
# ============================================================

fred_rows = []

for (state, year), state_vals in state_data.items():
    row = state_vals.copy()
    
    # Add national indicators
    row["national_unemployment"] = national_unemployment[national_unemployment["year"] == year]["value"].values[0] if year in national_unemployment["year"].values else None
    row["fed_funds_rate"] = fed_funds[fed_funds["year"] == year]["value"].values[0] if year in fed_funds["year"].values else None
    row["cpi"] = cpi[cpi["year"] == year]["value"].values[0] if year in cpi["year"].values else None
    row["mortgage_30yr"] = mortgage_30yr[mortgage_30yr["year"] == year]["value"].values[0] if year in mortgage_30yr["year"].values else None
    row["consumer_confidence"] = consumer_confidence[consumer_confidence["year"] == year]["value"].values[0] if year in consumer_confidence["year"].values else None
    row["treasury_10yr"] = treasury_10yr[treasury_10yr["year"] == year]["value"].values[0] if year in treasury_10yr["year"].values else None
    
    fred_rows.append(row)

fred_df = pd.DataFrame(fred_rows)

# ============================================================
# ENGINEER DERIVED FEATURES
# ============================================================

fred_df["unemployment_vs_national"] = fred_df["state_unemployment"] - fred_df["national_unemployment"]
fred_df["real_interest_rate"] = fred_df["fed_funds_rate"] - ((fred_df["cpi"].pct_change()) * 100)

# ============================================================
# VERIFY
# ============================================================

print(f"\nFRED lookup table shape: {fred_df.shape}")
print(f"Nulls:\n{fred_df.isnull().sum()}")
print(f"\nSample rows:")
print(fred_df.head(10))

# Save for reference
fred_df.to_csv("data/interim/fred_lookup.csv", index=False)