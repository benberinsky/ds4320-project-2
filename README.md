# DS 4320 Project 2: Does State and National Economic Context Assist in Predicting Loan Default Risk for Small Businesses?

### Executive Summary
FILL IN

<br>

---
| Spec | Value |
|:---|:---|
| Name | Benjamin Berinsky |
| NetID | tfu5hw |
| DOI | [fill in](add link) |
| Press Release | [ADD LINK](ADD LINK) |
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
[**NEED TO ADD**](ADD LINK HERE)

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