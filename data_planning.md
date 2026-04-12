Sources: 
- FRED API
- SBA Dataset - https://data.sba.gov/dataset/7-a-504-foia

Plan:

SBA dataset
- Filter to find a specific time period to look at
-  Drop loans where MIS_Status is missing (outcome unknown)
- Convert MIS_Status to binary (PIF = 0, CHGOFF = 1)
- Sample if needed for storage constraints

FRED API
- Figure out what geographic data is needed (backdrop stats)

Pulling in data
- Get from FRED API, then filter what's needed
- Structure/join datasets, mongoDB-ready