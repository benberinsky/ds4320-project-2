# **Where Your Borrower Does Business Matters More Than You Think**

## Hook
Small Business Administration (SBA) guaranteed loan charge-off rates vary widely by state, driven by local economic factors. This geographic variation is a critical yet underutilized factor in loan default risk prediction, and ignoring it is costing lenders money.

## The Problem: Banks focus on specific loans but fail to consider larger context 
Loan default risk prediction is a well studied field, with complex models used to output a probability score that individuals or businesses will be unable to pay back their loans in full. These probabilities are often used to determine whether loans are granted or denied. These decisions are crucial. A wrong prediction could mean economic disaster for banks, the SBA, and small business owners alike. Current models focus solely on aspects of the specific business and loan to determine risk which are important factors contributing to loan defaults, but do not paint the full picture. Going beyond loan-level data to examine broader economic context could separate good lenders from the best in the industry.

The question this analysis addresses is: does incorporating state-level geographic and economic context into a predictive model improve the ability to predict default on Small Business Administration (SBA)-guaranteed loans, or is default risk independent of business location and the surrounding economic environment?

## Solution Description 
To tackle this problem we gathered data about 400k+ loans approved by the SBA with characteristics about the business and the loan itself. We also gathered economic information, such as unemployment rate and median income, at the state and national level at the time the loan was approved. We proceeded to build three different predictive models trained on two datasets - one as a baseline including information about the loan and the business and one as a comparison including economic indicators. 

As can be seen in figure one below, all models and performance metrics we found that the enhanced model outperformed the baseline model. Our most accurate model was a Random Forest model. The biggest differences were found in F1 score, a metric that balances that rate at which defaults are caught vs. false alarms, with the F1 score of the enhanced random forest model outperforming the baseline by nearly 0.06. The enhanced random forest model was also 2.2% more accurate than the baseline model. 

Figure two shows the attributes that contributed most in making decisions of whether to classify a loan as default or paid off. Although the economic indicators did not impact the logistic regression or gradient boosted models greatly, 50% of the top 10 most important features for the random forest model were economic indicators. These were outweighed by the importance of other factors, such as the amount and duration of the loan, but they were still important to the final decision.

In conclusion, looking at state level economic context can improve ability to predict which loans are at risk of default. For lenders approving thousands of loans a year, even a small improvement in predictive accuracy translates to real dollars saved.

## Charts
![Figure 1: Model Performance Comparison](https://github.com/benberinsky/ds4320-project-2/blob/main/figures/model_performance_comp.png)

![Figure 2: Feature Importance of Full Models](https://github.com/benberinsky/ds4320-project-2/blob/main/figures/feature_importance_comparison.png)