import requests
import pandas as pd
import time
import logging
from datetime import datetime

# ============================================================
# LOGGING SETUP
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/fred_data_collection.log"),
        logging.StreamHandler() 
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# API KEY PROMPT
# ============================================================
def get_api_key():
    """Prompt user for FRED API key and validate it."""
    print("=" * 60)
    print("FRED API Data Collection Script")
    print("=" * 60)
    print("\nA FRED API key is required to run this script.")
    print("Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html\n")
    
    # user inputs API key
    api_key = input("Enter your FRED API key: ").strip()
    
    if not api_key:
        logger.error("No API key provided. Exiting.")
        raise ValueError("API key cannot be empty.")
    
    # Testing API key to ensure validity
    logger.info("Validating API key...")
    try:
        test_url = "https://api.stlouisfed.org/fred/series/observations"
        test_params = {
            "series_id": "UNRATE",
            "api_key": api_key,
            "file_type": "json",
            "observation_start": "2019-01-01",
            "observation_end": "2019-01-31"
        }
        response = requests.get(test_url, params=test_params)
        response.raise_for_status()
        logger.info("API key validated successfully.")
        return api_key
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            logger.error("Invalid API key. Please check and try again.")
            raise ValueError("Invalid FRED API key.") from e
        else:
            logger.error(f"API validation failed: {e}")
            raise

# ============================================================
# STATE MAPPINGS
# ============================================================

# states numerically encoded, mapping for clarity in data output
STATE_FIPS = {
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
# CORE FRED PULL FUNCTION
# ============================================================
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def get_fred_annual(series_id, api_key, start="2010-01-01", end="2019-12-31", max_retries=3):
    """
    Pull a single FRED series and return annual averages.
    
    Args:
        series_id: FRED series identifier
        api_key: FRED API key
        start: start date for observations
        end: end date for observations
        max_retries: number of retry attempts for server errors
    
    Returns:
        DataFrame with year and value columns, or None if failed
    """
    for attempt in range(max_retries):
        try:
            params = {
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "observation_start": start,
                "observation_end": end
            }
            
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            
            # parsing response
            observations = response.json()["observations"]
            
            if not observations:
                logger.warning(f"No observations returned for {series_id}")
                return None
            
            df = pd.DataFrame(observations)
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df["year"] = pd.to_datetime(df["date"]).dt.year
            annual = df.groupby("year")["value"].mean().reset_index()
            
            logger.debug(f"Successfully pulled {series_id}: {len(annual)} years")
            return annual
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                logger.warning(f"Server error for {series_id}, retry {attempt + 1}/{max_retries}")
                time.sleep(2 * (attempt + 1))  # Increasing backoff
                continue
            elif response.status_code == 400:
                logger.error(f"Bad request for series {series_id} — series ID may not exist")
                return None
            elif response.status_code == 429:
                logger.warning(f"Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                logger.error(f"HTTP error for {series_id}: {e}")
                return None
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error for {series_id}: {e}")
            time.sleep(5)
            continue
        
        except Exception as e:
            logger.error(f"Unexpected error for {series_id}: {e}")
            return None
    
    logger.error(f"Failed after {max_retries} retries: {series_id}")
    return None

def extract_year_value(df, year):
    """Extract a value for a given year from a FRED annual DataFrame."""
    if df is None:
        return None
    matches = df[df["year"] == year]["value"]
    if len(matches) == 0:
        return None
    return round(float(matches.values[0]), 4)

# ============================================================
# PULL STATE-LEVEL DATA
# ============================================================
def pull_state_data(api_key):
    """Pull all state-level economic indicators from FRED."""
    
    state_data = {}
    failed_series = []
    total_states = len(STATE_FIPS)
    
    for i, (state, fips) in enumerate(STATE_FIPS.items(), 1):
        logger.info(f"Pulling state data for {state} ({i}/{total_states})")
        
        # Define series for this state
        series = {
            "state_unemployment": f"{state}UR",
            "state_median_income": f"MEHOINUS{state}A672N",
            "state_per_capita_income": f"{state}PCPI",
            "state_gdp": f"{state}NGSP",
            "state_nonfarm_employment": f"{state}NA",
        }
        
        # Pull each series
        results = {}
        for name, series_id in series.items():
            result = get_fred_annual(series_id, api_key)
            results[name] = result
            
            if result is None:
                failed_series.append({"state": state, "series": name, "series_id": series_id})
                logger.warning(f"  Missing: {name} ({series_id})")
            
            time.sleep(1)
        
        # Build rows for each year
        for year in range(2010, 2020):
            state_data[(state, year)] = {
                "state": state,
                "year": year
            }
            for name, result in results.items():
                state_data[(state, year)][name] = extract_year_value(result, year)
        
        time.sleep(1)  

    logger.info(f"State data collection complete. {len(failed_series)} series failed.")
    
    if failed_series:
        logger.warning("Failed series summary:")
        for f in failed_series:
            logger.warning(f"  {f['state']}: {f['series']} ({f['series_id']})")
    
    return state_data, failed_series

# ============================================================
# PULL NATIONAL DATA
# ============================================================
def pull_national_data(api_key):
    """Pull all national-level economic indicators from FRED."""
    
    logger.info("Pulling national indicators...")
    
    national_series = {
        "national_unemployment": "UNRATE",
        "fed_funds_rate": "FEDFUNDS",
        "cpi": "CPIAUCSL",
        "mortgage_30yr": "MORTGAGE30US",
        "consumer_confidence": "UMCSENT",
        "treasury_10yr": "DGS10",
    }
    
    # looping over national series and pulling data
    results = {}
    for name, series_id in national_series.items():
        logger.info(f"  Pulling {name} ({series_id})")
        result = get_fred_annual(series_id, api_key)
        
        if result is None:
            logger.error(f"  FAILED: {name}")
        else:
            logger.info(f"  Success: {name} — {len(result)} years")
        
        results[name] = result
        time.sleep(1)
    
    return results

# ============================================================
# BUILD COMPLETE LOOKUP TABLE
# ============================================================
def build_lookup_table(state_data, national_data):
    """Combine state and national data into a single lookup table."""
    
    logger.info("Building combined lookup table...")
    
    fred_rows = []
    
    for (state, year), state_vals in state_data.items():
        row = state_vals.copy()
        
        # Add national indicators
        for name, result in national_data.items():
            row[name] = extract_year_value(result, year)
        
        fred_rows.append(row)
    
    fred_df = pd.DataFrame(fred_rows)
    
    # Engineer derived features
    fred_df["unemployment_vs_national"] = (
        fred_df["state_unemployment"] - fred_df["national_unemployment"]
    )
    
    logger.info(f"Lookup table shape: {fred_df.shape}")
    logger.info(f"Null counts:\n{fred_df.isnull().sum().to_string()}")
    
    return fred_df

# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    """Main execution flow for FRED data collection."""
    
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("FRED DATA COLLECTION — START")
    logger.info("=" * 60)
    
    try:
        # Get user input for API key
        api_key = get_api_key()
        
        # Pull state level data
        state_data, failed_series = pull_state_data(api_key)
        
        # Pull national data
        national_data = pull_national_data(api_key)
        
        # Build lookup table
        fred_df = build_lookup_table(state_data, national_data)
        
        # Save results
        output_path = "data/raw/fred_lookup.csv"
        fred_df.to_csv(output_path, index=False)
        logger.info(f"Saved lookup table to {output_path}")
        
        # Save failed series log for reference
        if failed_series:
            failed_df = pd.DataFrame(failed_series)
            failed_df.to_csv("data/interim/fred_failed_series.csv", index=False)
            logger.warning(f"Saved {len(failed_series)} failed series to fred_failed_series.csv")
        
        # Summary
        elapsed = datetime.now() - start_time
        logger.info("=" * 60)
        logger.info("COLLECTION COMPLETE")
        logger.info(f"  Rows: {len(fred_df)}")
        logger.info(f"  Columns: {fred_df.shape[1]}")
        logger.info(f"  Nulls: {fred_df.isnull().sum().sum()}")
        logger.info(f"  Failed series: {len(failed_series)}")
        logger.info(f"  Time elapsed: {elapsed}")
        logger.info("=" * 60)
        
        return fred_df
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected failure: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    fred_df = main()