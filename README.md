# DS 4320 Project 2: Can Economic Indicators Improve Default Prediction?


### Executive Summary
This repository contains all materials for an analysis of 
the importance of general economic indicators for small business
loan default risk prediction. The `data/` directory includes a subset 
of the data files used for analysis. A majority of the data used is stored
in MongoDB Atlas. The `scripts/` directory contains the data collection
and cleaning in python file and jupyter notebook format, and analysis 
pipeline in both Jupyter notebook and markdown formats. The `figures/`
directory includes all visualizations produced by the pipeline. The 
`press_release.md` markdown file presents the key findings in a 
newspaper-like tone. Further background on the project and data is 
documented below.

<br>

---
| Spec | Value |
|:---|:---|
| Name | Benjamin Berinsky |
| NetID | tfu5hw |
| DOI |[DOI](https://doi.org/10.5281/zenodo.19712819) |
| Press Release | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/press_release.md) |
| Pipeline | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/scripts/pipeline.ipynb) |
| License | [MIT](https://github.com/benberinsky/ds4320-project-2/blob/main/LICENSE) |

---
<br>

## Problem Definition

### General and Specific Problem
* **General Problem:** General problem: Does geographic information impact loan default rate?
* **Specific Problem:** Does incorporating state and national-level geographic and economic context improve the ability to predict default on Small Business Administration (SBA)-guaranteed loans, or is default risk independent of business location and the surrounding economic environment?

### Motivation
Small businesses are key to the American economy, and are largely made possible through loans. Although in an ideal world all small businesses would turn into massive successes, not all loans pan out. Loan defaults for small businesses may be due to cash flow shortages, high operating costs, economic downturns, or a variety of other factors. Defaulting on large loans can be incredibly economically detrimental to small business owners and is also harmful to the banks that approve them. Although loan defaults are caused by a multitude of factors, is geographic location one of them? By knowing the location of a small business as well as current state and national-level economic conditions, can we gain a better understanding of the risk of that business defaulting? If so, banks and lenders can incorporate local economic conditions when determining potential risks for loans to small business owners. Past research has focused primarily on individual-level loan default risk, but this project looks at the bigger picture in hopes of improving risk detection in default prediction models.

### Problem Refinement Rationale
My initial general problem statement identifies the project domain as generally investigating if there is any relationship between location and default rate. However, it does not provide specifics of what type of loans will be looked at, what 'geographic' means in context, or what the motivation of the research question is. The refined problem statement defines that we will be looking at SBA approved loans which narrows the data that will be used as well as the focus of the project. It also defines the geographic context as 'state level' which is more specific and actionable in terms of variables used. The specific problem also includes the caveat that state level economic context may not impact loan default rate which ensures that conclusions will not be impacted by confirmation bias.


### Press Release: 
[**Where Your Borrower Does Business Matters More Than You Think**](https://github.com/benberinsky/ds4320-project-2/blob/main/press_release.md)

## Domain Exposition

### Terminology
---

| Term | Description |
|------|-------------|
| Small Business Adminstration (SBA) | Organization that helps small business owners start, grow, and expand their businesses through counseling, loans, disaster recovery, etc. |
| Charged-Off | Declaration by the lender that a loan is unlikely to be collected, typically after 120–180 days of non-payment. Represents a realized loss|
| Paid in Full (PIF) | Loans that have been completely repaid, meaning the outstanding balance is $0 |
| SBA Guarantee	| The portion of the loan that the SBA agrees to repay to the lender if the borrower defaults |
| Consumer Price Index (CPI) | Measure of average change in prices paid by consumers for goods and services bought for consumption purposes by households |
| Default Rate | Percentage of outstanding loans that borrowers have failed to repay |

---

### Domain Explanation
This project lives in the domain of small business lending. Small businesses often need loans from banks to get started, with the goal of becoming successful and eventually paying lenders back. The SBA backs certain loans for small businesses, providing financial support by pledging to pay back a portion of the loan if borrowers are unable to. This makes lending to small businesses less risky for banks. Unfortunately, not all businesses are successful, and some borrowers are unable to pay back their loans in full. This project aims to explore state level economic indicators such as unemployment rate, median household income, and consumer price index. These indicators will be incorporated into default prediction to determine whether there is a relationship between local economic conditions and the rate at which small businesses fail to repay their loans. If such a relationship exists, these findings could impact how the SBA structures its approval process as well as how banks assess lending risk.

### Background Reading
[Folder here](https://1drv.ms/f/c/1A9305D23C7E8C8F/IgDaxVwTP4n-SYxINrIXzzADAam30aLrOdk3DaXIJnZStoU?e=PFEysM)

### Background Reading Table

| # | Title | Description | Link |
|---|-------|-------------|------|
| 1 | "SBA Loan Default Rates By State: Full 2025 Rankings" | Ranked list of SBA loan default rates for all states and potential reasons for differences | [View Paper](https://1drv.ms/b/c/1A9305D23C7E8C8F/IQC7oOMaAHybRblxIca_tiswASnKq2sZ14q9C8OUJ_GS9hM?e=tUyjGF) |
| 2 | "Predicting Loan Default Risk Using Machine Learning: <br> A Simple, Data-Driven Approach" | Overview of how logistic regression is used in loan-default risk prediction | [View Paper](https://1drv.ms/b/c/1A9305D23C7E8C8F/IQASH7AGU3uxSIi7UcRdOj8NAcKbmgFkyF7WHsJs3J5QDJw?e=9xrZUY) |
| 3 | "The Effects of State and Local Economic Incentives on <br> Business Start-Ups in the United States: County-Level Evidence" | Explores the relationship between location and emerging businesses, economic conditions | [View Paper](https://1drv.ms/b/c/1A9305D23C7E8C8F/IQAX1OwmjbVlQK3VPN2wgBPLAaW9rUCRwNXslooDT4ALVqI?e=9FweHw) |
| 4 | "US SBA Loans" | Overview of how the SBA supports small businesses by reducing financial risk of loans | [View Paper](https://1drv.ms/b/c/1A9305D23C7E8C8F/IQB-B0RuT7b7R6Z9_VhlnbGYAeqU3N95uUnPetmrwgTJJa0?e=3JcXvh) |
| 5 | "What Happens if You Can’t Repay Your SBA Loan?" | Outlines the process of handling loan default, risks and consequences | [View Paper](https://1drv.ms/b/c/1A9305D23C7E8C8F/IQAhIdcRhzoAR6Bx5Ci32EuXAR4Bnxs3CJQ99BdZvwJ289c?e=e7i8wK) |

## Data Creation

### Data Acquisition (Provenance)

I acquired the data for this project from two separate sources before merging them together to create comprehensive documents. The first data source was from the U.S Small Business administration (SBA) website. I downloaded a CSV file from their website that contained information about small businesses from 2010-19 who were supported for loans by the SBA. The file contained a wide array of information about the businesses and their approved loans, but my main focus was on the state the business was in and whether the loan was paid off in full or charged off (defaulted). I then cleaned the data in a Jupyter notebook, keeping only relevant columns, featuring engineering new fields, and encoding categorical variables.

The second data source I used was from the Federal Reserve Economic Data (FRED) API. I created a free API key and made a Python script that pulled in 10 years of both state and national level economic data, such as unemployment rate, median household income etc. After this data was pulled into a CSV file, I merged the two CSVs so that each row contained state and national economic information. The state economic information was about the state that the business operated in. Finally, I made a Jupyter notebook that converted the merged CSV to document format and using the PyMongo package pushed the data to Mongodb Atlas.

### Data Acquisition code

---

| File Name | Description | Link |
|-----------|-------------|------|
| `sba_data_cleaning.ipynb` | Data cleaning notebook for SBA loans. Removes unnecessary columns, <br> feature engineers new fields, keeps only relevant columns, ensures valid <br> structure | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/scripts/sba_data_cleaning.ipynb) |
| `fred_api.py` | Pulls in state and national-level economic data from FRED API from 2010-19. <br> Saves to a reference CSV file for downstream merge | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/scripts/fred_api.py) |
| `fred_clean_merge.ipynb` | Merges the SBA data with the FRED data, appending state and national <br>economic context to each business's loan based on location and year | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/scripts/fred_clean_merge.ipynb) |
| `convert_to_mongo.ipynb` | Connects to MongoDB Atlas, builds document structure for DB, batchs inserts <br> rows into MongoDB in document format | [Link](https://github.com/benberinsky/ds4320-project-2/blob/main/scripts/convert_to_mongo.ipynb) |

---

### Critical Decision Rationale
In the formation of my database I decided to drop the variables indicating the amount that was charged off and encode the target variable as binary, either paid off or defaulted. Although the amount that was charged off could be insightful, I wanted to make my research question to be specific. I dropped the variable `businessage` from my database as it was missing for about 80% of all businesses and I did not believe it would be insightful for my analysis. I used annual averages for FRED data rather than values at the time the loan was approved for simplicity as it would have been difficult to pull in the exact economic snapshot values for 400k+ documents, and the values did not fluctuate greatly throughout the year. I chose to analyze at the state level rather than zip-code, county, city, or more specific areas because I felt this analysis would be too granular and would not produce generalizable findings. Finally, I dropped all loans that were not either paid off in full or charged off they were not related to my research question.

### Bias Identification
In the process of creating my database, some selection bias may have been present as I only looked at approved loans. By ignoring loans that were not approved I am excluding key context on the economic state of all small businesses. Further, since I am only looking at state-level geography, I may miss some key nuances. For example, the economic climate in New York city is vastly different than in the mountains of upstate New York, but they are classified in the same state-level economic bucket. The timeframe I am looking at is 2010-2019, right after the great recession and before the COVID-19 pandemic. This data may not be representative of current economic patterns. Finally, I am only looking at SBA backed loans which may not be representative of all small businesses.

### Bias Mitigation
I will make the conclusions of my analysis specific rather than generalizing to broader populations. By clearly disclosing the timeframe the data was collected in as well as the businesses represented in my dataset, I can frame my takeaways as specific to these conditions and caution against making broad generalizations. Further analysis of this data could be more granular, such as looking at a larger scope of time or more specific regions (zip-code rather than state for example).

## Metadata

### Implicit Schema
The document structure has 6 top-level fields: id, business, loan_terms, geography, economic_snapshot, and default. ID and default have no subfields. ID is a document identifier string and default is a binary indicator of whether or not the loan defaulted.

- Business contains subfields such as state and business_type that provide insight into the specific business the document represents.

- Loan_terms contains subfields such as gross_approval and interest_rate that relate to the specific terms of the loan.

- Geography contains the field borrower state that represents which state the loan was applied for/approved in as well as whether or not the bank and project were in the same state.

- Economic_snapshot contains a multitude of subfields, such as unemployment rate and median income at both the state and national level that are indicative of the economic climate at the time the loan was approved.

- For an exhaustive list of the fields contained in the document see the data dictionary below. There are only two levels of subfields.

### Database Summary
The database contains approximately 419,000 documents, each representing a loan backed by the Small Business administration. Each document contains economic information about the loan as well as state and national economic reference data. Each document has 5 top-level fields, business, loan_terms, geography, and economic_snapshot, all containing nested subfields. There are also top level fields of ID and default without subfields. The information comes from the SBA website as well as the FRED API.

### Data Dictionary
**Business**

| Field | Data Type | Description | Example |
|-------|-----------|-------------|---------|
| `business.state` | string | State the business operates in | 'CA' |
| `business.naics_sector` | string | Numerical indicator of business sector | 44 |
| `business.naics_description` | string | Description of business sector | 'Gasoline Stations with Convenience Stores' |
| `business.business_type` | string | Description of business ownership type | 'INDIVIDUAL' |
| `business.jobs_supported` | integer | Number of jobs the business supports | 5 |

**Loan Terms**

| Field | Data Type | Description | Example |
|-------|-----------|-------------|---------|
| `loan_terms.gross_approval` | integer | Total dollar amount the loan was approved for |1562500 |
| `loan_terms.sba_guaranteed` | integer | The dollar amount of the loan guaranteed by the SBA (portion the SBA will repay the lender if the borrower defaults) | 1406250 |
| `loan_terms.guarantee_pct` | float | The proportion of the gross approval guarunteed by the SBA (guaranteed/gross) | 0.9 |
| `loan_terms.term_months` | integer | The length of the loan repayment period in months | 300 |
| `loan_terms.interest_rate` | float | The initial interest rate on the loan at the time of approval, expressed as an annual percentage | 6.0 |
| `loan_terms.variable_rate` | integer | Binary indicator of whether the loan has a variable interest rate (1) or fixed rate (0) | 1 |
| `loan_terms.revolver_status` | integer | Binary indicator of whether the loan is a revolving line of credit (1) or a standard term loan (0) | 0 |
| `loan_terms.approval_year` | integer | Year the loan was approved | 2010 |

**Geography**

| Field | Data Type | Description | Example |
|-------|-----------|-------------|---------|
| `geography.borrower_state` | string | State the borrowing company operates in| 'MA' |
| `geography.bank_in_state` | integer | Binary indicator of whether the bank is in the same state as the business (1) or not (0) | 1 |
| `geography.project_in_state` | integer | Binary indicator of whether the project is in the same state as the business (1) or not (0) | 0 |

**Economic Snapshot**

| Field | Data Type | Description | Example |
|-------|-----------|-------------|---------|
| `economic_snapshot.state_unemployment` | float | Percentage of adults within state that are unemployed | 12.3167 |
| `economic_snapshot.state_median_income` | integer | Individual income for a given state and year where 50% make more and 50% make less | 75000|
| `economic_snapshot.state_per_capita_income` | integer | Average income per person in the state for the loan's approval year, from FRED | 43137.0 |
| `economic_snapshot.state_gdp` | float | Total gross domestic product of the state in millions of dollars for the loan's approval year | 1938603.3 |
| `economic_snapshot.national_unemployment` | float |Percentage of adults within the country that are unemployed | 11.325 |
| `economic_snapshot.fed_funds_rate` | float | The average annual federal funds rate — the interest rate at which banks lend to each other<br> overnight, set by the Federal Reserve | 0.175 |
| `economic_snapshot.cpi` | integer | Consumer Price Index — a measure of the average change in  prices paid by consumers for goods<br> and services, used to track inflation | 218 |
| `economic_snapshot.mortgage_30yr` | float | The average annual interest rate on a 30-year fixed-rate mortgage,  used as a proxy for the broader <br> borrowing environment | 4.6898 |
| `economic_snapshot.consumer_confidence` | float | University of Michigan Consumer Sentiment Index — measures household confidence in the economy,<br> higher values indicate greater optimism | 71.8417 |
| `economic_snapshot.treasury_10yr` | float | The average annual yield on 10-year US Treasury bonds — a benchmark interest rate that influences<br> lending rates across the economy | 3.2151 |
| `economic_snapshot.unemployment_vs_national` | float | The difference between the state unemployment rate and the national unemployment rate — positive <br>values indicate the state is performing worse than average | 2.7084 |

**Economic Snapshot**

| Field | Data Type | Description | Example |
|-------|-----------|-------------|---------|
| `economic_snapshot.state_unemployment` | float | Percentage of adults within state that are unemployed | 12.3167 |
| `economic_snapshot.state_median_income` | integer | Individual income for a given state and year where 50% make more and 50% make less | 75000|
| `economic_snapshot.state_per_capita_income` | integer | Average income per person in the state for the loan's approval year, from FRED | 43137.0 |
| `economic_snapshot.state_gdp` | float | Total gross domestic product of the state in millions of dollars for the loan's approval year | 1938603.3 |
| `economic_snapshot.national_unemployment` | float |Percentage of adults within the country that are unemployed | 11.325 |
| `economic_snapshot.fed_funds_rate` | float | The average annual federal funds rate — the interest rate at which banks lend to each other<br> overnight, set by the Federal Reserve | 0.175 |
| `economic_snapshot.cpi` | integer | Consumer Price Index — a measure of the average change in  prices paid by consumers for goods<br> and services, used to track inflation | 218 |
| `economic_snapshot.mortgage_30yr` | float | The average annual interest rate on a 30-year fixed-rate mortgage,  used as a proxy for the broader <br> borrowing environment | 4.6898 |
| `economic_snapshot.consumer_confidence` | float | University of Michigan Consumer Sentiment Index — measures household confidence in the economy,<br> higher values indicate greater optimism | 71.8417 |
| `economic_snapshot.treasury_10yr` | float | The average annual yield on 10-year US Treasury bonds — a benchmark interest rate that influences<br> lending rates across the economy | 3.2151 |
| `economic_snapshot.unemployment_vs_national` | float | The difference between the state unemployment rate and the national unemployment rate — positive <br>values indicate the state is performing worse than average | 2.7084 |


### Uncertainty Quantification

**Business**

| Field Name | Data Type | Uncertainty | Rationale |
|---|---|---|---|
| `business.jobs_supported` | integer | +/- 0.03 | Self reported, inherently uncertain, SEM calculated as 0.03 |

**Loan Terms**

| Field Name | Data Type | Uncertainty | Rationale |
|---|---|---|---|
| `loan_terms.gross_approval` | integer | +/- 0 | Comes from official SBA loan records |
| `loan_terms.sba_guaranteed` | integer | +/- 0 | Comes from official SBA loan records |
| `loan_terms.guarantee_pct` | float | +/- 0 | Comes from official SBA loan records |
| `loan_terms.interest_rate` | float | +/- 0 | Comes from official SBA loan records |


**Economic Snapshot**

Note: BLS indicates Bureau of Labor Statistics, BEA indicates The Bureau of Economic Analysis
| Field Name | Data Type | Uncertainty | Rationale |
|---|---|---|---|
| `economic_snapshot.state_unemployment` | float | +/- 0.3 | Uncertainty estimated as 0.2-0.5 by BLS |
| `economic_snapshot.state_median_income` | integer | +/- 1500 | Uncertainty reported as between 1000-2000 by US Census |
| `economic_snapshot.state_per_capita_income` | integer | +/- 750 | Uncertainty reported as between 500 and 1000 by BEA |
| `economic_snapshot.state_gdp` | float | +/- 0	 | Officially calculated metric |
| `economic_snapshot.national_unemployment` | float | +/- 0.1 | Uncertainty estimated as 0.1 by BLS |
| `economic_snapshot.fed_funds_rate` | float |+/- 0	| Exact policy rate set by the Federal Reserve |
| `economic_snapshot.cpi` | integer | +/- 0.2	| BLS reports SE of ~0.1–0.2 index points for CPI estimates |
| `economic_snapshot.mortgage_30yr` | float | +/- 0.01 | Potential survey error, would be very low |
| `economic_snapshot.consumer_confidence` | float | +/- 0.15 | Uncertainty published at 1.5% by the University of Michigan |
| `economic_snapshot.treasury_10yr` | float |+/- 0 |Directly observed market rate, no measurement error |
| `economic_snapshot.unemployment_vs_national` | float | +/- 0.03 | SEM calculated from parent fields |