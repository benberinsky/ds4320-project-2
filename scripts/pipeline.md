# Analysis Pipeline Notebook


```python
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.preprocessing import OneHotEncoder
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve)
import time
import matplotlib.gridspec as gridspec
```

## Pulling Data In


```python
# Load environment variables from env file
load_dotenv()
user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
connection_string = f"mongodb+srv://{user}:{password}@cluster0.zqvm7.mongodb.net/?appName=Cluster0"

# creating database connection and collection
client = MongoClient(connection_string)
db = client["sba_loan_project"]
collection = db["loans"]
```


```python
# Pull data from MongoDB
raw_data = list(collection.find())

# Flatten nested documents into a flat DataFrame
data = pd.json_normalize(raw_data)

# Drop the MongoDB ObjectId field (not useful for analysis)
data.drop(columns=['_id'], inplace=True)

print(data.shape)
data.head()
```

    (418509, 28)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>default</th>
      <th>business.state</th>
      <th>business.naics_sector</th>
      <th>business.naics_description</th>
      <th>business.business_type</th>
      <th>business.jobs_supported</th>
      <th>loan_terms.gross_approval</th>
      <th>loan_terms.sba_guaranteed</th>
      <th>loan_terms.guarantee_pct</th>
      <th>loan_terms.term_months</th>
      <th>...</th>
      <th>economic_snapshot.state_median_income</th>
      <th>economic_snapshot.state_per_capita_income</th>
      <th>economic_snapshot.state_gdp</th>
      <th>economic_snapshot.national_unemployment</th>
      <th>economic_snapshot.fed_funds_rate</th>
      <th>economic_snapshot.cpi</th>
      <th>economic_snapshot.mortgage_30yr</th>
      <th>economic_snapshot.consumer_confidence</th>
      <th>economic_snapshot.treasury_10yr</th>
      <th>economic_snapshot.unemployment_vs_national</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>MI</td>
      <td>72</td>
      <td>Limited-Service Restaurants</td>
      <td>CORPORATION</td>
      <td>0.0</td>
      <td>398000.0</td>
      <td>358200.0</td>
      <td>0.90</td>
      <td>125</td>
      <td>...</td>
      <td>64260.0</td>
      <td>35635.0</td>
      <td>393179.6</td>
      <td>9.6083</td>
      <td>0.1750</td>
      <td>218.0762</td>
      <td>4.6898</td>
      <td>71.8417</td>
      <td>3.2151</td>
      <td>3.1334</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>MA</td>
      <td>72</td>
      <td>Limited-Service Restaurants</td>
      <td>CORPORATION</td>
      <td>6.0</td>
      <td>13100.0</td>
      <td>11790.0</td>
      <td>0.90</td>
      <td>60</td>
      <td>...</td>
      <td>84610.0</td>
      <td>52707.0</td>
      <td>409270.0</td>
      <td>9.6083</td>
      <td>0.1750</td>
      <td>218.0762</td>
      <td>4.6898</td>
      <td>71.8417</td>
      <td>3.2151</td>
      <td>-1.5083</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>NV</td>
      <td>56</td>
      <td>Landscaping Services</td>
      <td>INDIVIDUAL</td>
      <td>1.0</td>
      <td>5000.0</td>
      <td>4500.0</td>
      <td>0.90</td>
      <td>120</td>
      <td>...</td>
      <td>71090.0</td>
      <td>37289.0</td>
      <td>125149.0</td>
      <td>9.6083</td>
      <td>0.1750</td>
      <td>218.0762</td>
      <td>4.6898</td>
      <td>71.8417</td>
      <td>3.2151</td>
      <td>3.6417</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>IA</td>
      <td>72</td>
      <td>Limited-Service Restaurants</td>
      <td>INDIVIDUAL</td>
      <td>8.0</td>
      <td>59500.0</td>
      <td>53550.0</td>
      <td>0.90</td>
      <td>210</td>
      <td>...</td>
      <td>68060.0</td>
      <td>38190.0</td>
      <td>142497.7</td>
      <td>9.6083</td>
      <td>0.1750</td>
      <td>218.0762</td>
      <td>4.6898</td>
      <td>71.8417</td>
      <td>3.2151</td>
      <td>-3.5166</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>CA</td>
      <td>62</td>
      <td>Offices of Physicians (except Mental Health Sp...</td>
      <td>INDIVIDUAL</td>
      <td>5.0</td>
      <td>620000.0</td>
      <td>465000.0</td>
      <td>0.75</td>
      <td>300</td>
      <td>...</td>
      <td>86690.0</td>
      <td>60984.0</td>
      <td>2899530.9</td>
      <td>3.8917</td>
      <td>1.8317</td>
      <td>251.0995</td>
      <td>4.5446</td>
      <td>98.3667</td>
      <td>2.9112</td>
      <td>0.3666</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 28 columns</p>
</div>



## Filtering for Analysis


```python
# peeking at one row/document
data.iloc[1]
```




    default                                                                 0
    business.state                                                         MA
    business.naics_sector                                                  72
    business.naics_description                    Limited-Service Restaurants
    business.business_type                                        CORPORATION
    business.jobs_supported                                               6.0
    loan_terms.gross_approval                                         13100.0
    loan_terms.sba_guaranteed                                         11790.0
    loan_terms.guarantee_pct                                              0.9
    loan_terms.term_months                                                 60
    loan_terms.interest_rate                                              7.0
    loan_terms.variable_rate                                                1
    loan_terms.revolver_status                                              0
    loan_terms.approval_year                                             2010
    geography.borrower_state                                               MA
    geography.bank_in_state                                                 1
    geography.project_in_state                                              1
    economic_snapshot.state_unemployment                                  8.1
    economic_snapshot.state_median_income                             84610.0
    economic_snapshot.state_per_capita_income                         52707.0
    economic_snapshot.state_gdp                                      409270.0
    economic_snapshot.national_unemployment                            9.6083
    economic_snapshot.fed_funds_rate                                    0.175
    economic_snapshot.cpi                                            218.0762
    economic_snapshot.mortgage_30yr                                    4.6898
    economic_snapshot.consumer_confidence                             71.8417
    economic_snapshot.treasury_10yr                                    3.2151
    economic_snapshot.unemployment_vs_national                        -1.5083
    Name: 1, dtype: object



### Dropping unnecessary cols:
- "business.state": Placeholder for pulling in economic data
- "business.naics_description": Text, redundant with sector instead
- "geography.borrower_state": Placeholder for pulling in economic data
- "loan_terms.approval_year": Time is not important to the analysis
- "loan_terms.sba_guaranteed": Redundant with gross approval and guarantee %


```python
overall_analysis_data = data.drop(columns = ['business.state', 'business.naics_description', 'geography.borrower_state','loan_terms.approval_year', 'loan_terms.sba_guaranteed'])
```

### Encoding categorical variables: 
- "business.naics_sector"
- "business.business_type"


```python
overall_analysis_data['business.business_type'].value_counts()
```




    business.business_type
    CORPORATION    365015
    INDIVIDUAL      45764
    PARTNERSHIP      7712
                       18
    Name: count, dtype: int64




```python
# dropping rows(18) with empty business type
overall_analysis_data = overall_analysis_data[overall_analysis_data["business.business_type"].str.strip() != ""].copy()
```


```python
overall_analysis_data['business.naics_sector'].value_counts()
```




    business.naics_sector
    72    53196
    23    45373
    54    42261
    44    40784
    62    37771
    81    36420
    42    22531
    48    21836
    56    19718
    33    16963
    45    15948
    71    11948
    53     9044
    31     8564
    32     7874
    52     7108
    11     6948
    61     5693
    51     5051
    49     1519
    21     1268
    22      344
    55      254
    92       73
    na        2
    Name: count, dtype: int64




```python
# dropping rows(2) with na business sector
overall_analysis_data = overall_analysis_data[overall_analysis_data["business.naics_sector"].str.strip() != ""].copy()
```


```python
categorical_cols = ['business.naics_sector', 'business.business_type']
encoder = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
encoded_data = encoder.fit_transform(overall_analysis_data[categorical_cols])

# get_feature_names_out() with no arguments
encoded_df = pd.DataFrame(
    encoded_data, 
    columns=encoder.get_feature_names_out(),
    index=overall_analysis_data.index  # preserve the index for concat
)

final_analysis_data = pd.concat(
    [overall_analysis_data.drop(columns=categorical_cols), encoded_df], 
    axis=1
)

print(f"Shape: {final_analysis_data.shape}")
final_analysis_data.head()
```

    Shape: (418491, 47)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>default</th>
      <th>business.jobs_supported</th>
      <th>loan_terms.gross_approval</th>
      <th>loan_terms.guarantee_pct</th>
      <th>loan_terms.term_months</th>
      <th>loan_terms.interest_rate</th>
      <th>loan_terms.variable_rate</th>
      <th>loan_terms.revolver_status</th>
      <th>geography.bank_in_state</th>
      <th>geography.project_in_state</th>
      <th>...</th>
      <th>business.naics_sector_56</th>
      <th>business.naics_sector_61</th>
      <th>business.naics_sector_62</th>
      <th>business.naics_sector_71</th>
      <th>business.naics_sector_72</th>
      <th>business.naics_sector_81</th>
      <th>business.naics_sector_92</th>
      <th>business.naics_sector_na</th>
      <th>business.business_type_INDIVIDUAL</th>
      <th>business.business_type_PARTNERSHIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0.0</td>
      <td>398000.0</td>
      <td>0.90</td>
      <td>125</td>
      <td>5.980</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>6.0</td>
      <td>13100.0</td>
      <td>0.90</td>
      <td>60</td>
      <td>7.000</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>1.0</td>
      <td>5000.0</td>
      <td>0.90</td>
      <td>120</td>
      <td>7.750</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>8.0</td>
      <td>59500.0</td>
      <td>0.90</td>
      <td>210</td>
      <td>7.250</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>5.0</td>
      <td>620000.0</td>
      <td>0.75</td>
      <td>300</td>
      <td>5.125</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 47 columns</p>
</div>



### Splitting into model A (baseline) and model B (geographic) features


```python
final_analysis_data.columns
```




    Index(['default', 'business.jobs_supported', 'loan_terms.gross_approval',
           'loan_terms.guarantee_pct', 'loan_terms.term_months',
           'loan_terms.interest_rate', 'loan_terms.variable_rate',
           'loan_terms.revolver_status', 'geography.bank_in_state',
           'geography.project_in_state', 'economic_snapshot.state_unemployment',
           'economic_snapshot.state_median_income',
           'economic_snapshot.state_per_capita_income',
           'economic_snapshot.state_gdp',
           'economic_snapshot.national_unemployment',
           'economic_snapshot.fed_funds_rate', 'economic_snapshot.cpi',
           'economic_snapshot.mortgage_30yr',
           'economic_snapshot.consumer_confidence',
           'economic_snapshot.treasury_10yr',
           'economic_snapshot.unemployment_vs_national',
           'business.naics_sector_21', 'business.naics_sector_22',
           'business.naics_sector_23', 'business.naics_sector_31',
           'business.naics_sector_32', 'business.naics_sector_33',
           'business.naics_sector_42', 'business.naics_sector_44',
           'business.naics_sector_45', 'business.naics_sector_48',
           'business.naics_sector_49', 'business.naics_sector_51',
           'business.naics_sector_52', 'business.naics_sector_53',
           'business.naics_sector_54', 'business.naics_sector_55',
           'business.naics_sector_56', 'business.naics_sector_61',
           'business.naics_sector_62', 'business.naics_sector_71',
           'business.naics_sector_72', 'business.naics_sector_81',
           'business.naics_sector_92', 'business.naics_sector_na',
           'business.business_type_INDIVIDUAL',
           'business.business_type_PARTNERSHIP'],
          dtype='object')




```python
# saving target (default)
y = final_analysis_data["default"]
```


```python
# selecting features for baseline model
baseline_model_features = [
    "business.jobs_supported",
    "loan_terms.gross_approval",
    "loan_terms.guarantee_pct",
    "loan_terms.term_months",
    "loan_terms.interest_rate",
    "loan_terms.variable_rate",
    "loan_terms.revolver_status",

    # encoded categorical features
    "business.naics_sector_21", 'business.naics_sector_22',
    'business.naics_sector_23', 'business.naics_sector_31',
    'business.naics_sector_32', 'business.naics_sector_33',
    'business.naics_sector_42', 'business.naics_sector_44',
    'business.naics_sector_45', 'business.naics_sector_48',
    'business.naics_sector_49', 'business.naics_sector_51',
    'business.naics_sector_52', 'business.naics_sector_53',
    'business.naics_sector_54', 'business.naics_sector_55',
    'business.naics_sector_56', 'business.naics_sector_61',
    'business.naics_sector_62', 'business.naics_sector_71',
    'business.naics_sector_72', 'business.naics_sector_81',
    'business.naics_sector_92', 'business.naics_sector_na',
    'business.business_type_INDIVIDUAL',
    'business.business_type_PARTNERSHIP']
```


```python
# selecting features for full model
full_model_features = baseline_model_features + [
    # Geographic
    "geography.bank_in_state",
    "geography.project_in_state",
    
    # State-level
    "economic_snapshot.state_unemployment",
    "economic_snapshot.state_median_income",
    "economic_snapshot.state_per_capita_income",
    "economic_snapshot.state_gdp",
    
    # National
    "economic_snapshot.national_unemployment",
    "economic_snapshot.fed_funds_rate",
    "economic_snapshot.cpi",
    "economic_snapshot.mortgage_30yr",
    "economic_snapshot.consumer_confidence",
    "economic_snapshot.treasury_10yr",
    
    # Derived
    "economic_snapshot.unemployment_vs_national",
]
```


```python
X_baseline = final_analysis_data[baseline_model_features]
X_full = final_analysis_data[full_model_features]

print(f"Target shape: {y.shape}")
print(f"Model A features: {X_baseline.shape[1]}")
print(f"Model B features: {X_full.shape[1]}")
```

    Target shape: (418491,)
    Model A features: 33
    Model B features: 46


## Modeling

Analysis rationale: 
I chose to examine three different classifiers, logistic regression, gradient boosted decision trees, and random forests. Within each classifier I used a baseline dataset and a dataset including state and national economic indicators. My general goal was to see if the different datasets led to differences in performance. Because of this, I wanted to see how the data performed across different models, not just one. After preparing the data I ran a gridsearch across hyperparameters to find the optimal ones. Initially I had many more combinations, but since training was taking many hours I decided to research a few possibilities and just test 2 for each parameter. I then saved evaluation metrics for further analysis and visualization. I felt this approach was a logical way to examine whether model performance differed across the datasets.


```python
# ============================================================
# Train-test split
# ============================================================

X_baseline_train, X_baseline_test, y_train, y_test = train_test_split(
    X_baseline, y, test_size=0.2, random_state=42, stratify=y
)
X_full_train, X_full_test, _, _ = train_test_split(
    X_full, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_baseline_train)} rows")
print(f"Test set: {len(X_baseline_test)} rows")
print(f"Train default rate: {y_train.mean()*100:.2f}%")
print(f"Test default rate: {y_test.mean()*100:.2f}%")

# ============================================================
# SCALE FEATURES (for logistic regression)
# ============================================================

# scaling baseline features
scaler_a = StandardScaler()
X_baseline_train_scaled = scaler_a.fit_transform(X_baseline_train)
X_baseline_test_scaled = scaler_a.transform(X_baseline_test)

# scaling full features
scaler_b = StandardScaler()
X_full_train_scaled = scaler_b.fit_transform(X_full_train)
X_full_test_scaled = scaler_b.transform(X_full_test)

# ============================================================
# DEFINE BASE MODELS AND PARAM GRIDS
# ============================================================
from sklearn.model_selection import GridSearchCV
from copy import deepcopy

base_models = {
    "Logistic Regression": LogisticRegression(
        class_weight='balanced',
        random_state=42,
        solver='saga', 
        max_iter= 1000 # supports both l1 and l2

    ),
    "Random Forest": RandomForestClassifier(
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ),
    "XGBoost": XGBClassifier(
        scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
        random_state=42,
        n_jobs=-1,
        eval_metric='logloss'
    )
}

# param grids for gridsearch to find optimal hyperparameters for each model
log_reg_param_grid = {
        'C': [0.01, 0.1, 1],
        'penalty': ['l1', 'l2']
    }
rf_param_grid = {
        'n_estimators': [100, 200],      
        'max_depth': [10, 20],
        'min_samples_leaf': [1, 4]        
    }
xgb_param_grid = {
        'n_estimators': [100, 200],     
        'max_depth': [3, 6],
        'learning_rate': [0.01, 0.1]
    }

param_grids = {
    "Logistic Regression": log_reg_param_grid,
    "Random Forest": rf_param_grid,
    "XGBoost": xgb_param_grid
}

# ============================================================
# TRAIN WITH GRIDSEARCH AND EVALUATE
# ============================================================
def gridsearch_evaluate(base_model, param_grid, X_train, X_test,
                        y_train, y_test, model_name, feature_set):
    """GridSearchCV, refit best model, return metrics + artifacts with logging"""

    n_combos = 1
    for v in param_grid.values():
        n_combos *= len(v)
    n_folds = 5

    start = time.time()

    gs = GridSearchCV(
        estimator=deepcopy(base_model),
        param_grid=param_grid,
        scoring='roc_auc',
        cv=n_folds,
        n_jobs=-1,
        verbose=0,   
        refit=True
    )
    gs.fit(X_train, y_train)
    print(f"    Best params: {gs.best_params_}")
    print(f"    Best CV AUC: {gs.best_score_:.4f}")

    best_model = gs.best_estimator_
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        'Model': model_name,
        'Feature Set': feature_set,
        'Best Params': gs.best_params_,
        'CV AUC (mean)': gs.best_score_,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1': f1_score(y_test, y_pred),
        'AUC-ROC': roc_auc_score(y_test, y_prob)
    }

    return metrics, best_model, y_pred, y_prob
# ============================================================
# STORAGE — metrics, models, predictions, feature importance
# ============================================================

# list of dicts for df
all_metrics = []             
trained_models = {}             # {key: fitted model}
predictions = {}                # {key: {'y_pred': ..., 'y_prob': ...}}
feature_importances = {}        # {key: DataFrame(feature, importance)}

# ============================================================
# TRAIN AND EVALUATE ALL MODELS
# ============================================================

for name in base_models:
    print(f"\n{'='*60}")
    print(f"  GridSearchCV: {name}")
    print(f"{'='*60}")

    # pick scaled vs unscaled data based on model
    if name == "Logistic Regression":
        X_tr_a, X_te_a = X_baseline_train_scaled, X_baseline_test_scaled
        X_tr_b, X_te_b = X_full_train_scaled, X_full_test_scaled
    else:
        X_tr_a, X_te_a = X_baseline_train, X_baseline_test
        X_tr_b, X_te_b = X_full_train, X_full_test

    # ---------- Model A: Loan Only ----------
    key_a = f"{name}_A"
    metrics_a, model_a, preds_a, probs_a = gridsearch_evaluate(
        base_models[name], param_grids[name],
        X_tr_a, X_te_a, y_train, y_test,
        name, "A: Loan Only"
    )
    all_metrics.append(metrics_a)
    trained_models[key_a] = model_a
    predictions[key_a] = {'y_pred': preds_a, 'y_prob': probs_a}

    print(f"\n  Model A (Loan Only)  — Best params: {metrics_a['Best Params']}")
    print(f"    CV AUC:    {metrics_a['CV AUC (mean)']:.4f}")
    print(f"    Accuracy:  {metrics_a['Accuracy']:.4f}")
    print(f"    Precision: {metrics_a['Precision']:.4f}")
    print(f"    Recall:    {metrics_a['Recall']:.4f}")
    print(f"    F1:        {metrics_a['F1']:.4f}")
    print(f"    AUC-ROC:   {metrics_a['AUC-ROC']:.4f}")

    # ---------- Model B: Loan + Economic ----------
    key_b = f"{name}_B"
    metrics_b, model_b, preds_b, probs_b = gridsearch_evaluate(
        base_models[name], param_grids[name],
        X_tr_b, X_te_b, y_train, y_test,
        name, "B: Loan + Economic"
    )
    all_metrics.append(metrics_b)
    trained_models[key_b] = model_b
    predictions[key_b] = {'y_pred': preds_b, 'y_prob': probs_b}

    print(f"\n  Model B (Loan + Econ) — Best params: {metrics_b['Best Params']}")
    print(f"    CV AUC:    {metrics_b['CV AUC (mean)']:.4f}")
    print(f"    Accuracy:  {metrics_b['Accuracy']:.4f}")
    print(f"    Precision: {metrics_b['Precision']:.4f}")
    print(f"    Recall:    {metrics_b['Recall']:.4f}")
    print(f"    F1:        {metrics_b['F1']:.4f}")
    print(f"    AUC-ROC:   {metrics_b['AUC-ROC']:.4f}")

    auc_diff = metrics_b['AUC-ROC'] - metrics_a['AUC-ROC']
    print(f"\n  ➜ AUC Improvement (B − A): {auc_diff:+.4f}")

    # ---------- Feature importance ----------
    # store for BOTH A and B where available
    for key, fitted, cols in [
        (key_a, model_a, X_baseline_train.columns if hasattr(X_baseline_train, 'columns') else [f"f{i}" for i in range(X_tr_a.shape[1])]),
        (key_b, model_b, X_full_train.columns if hasattr(X_full_train, 'columns') else [f"f{i}" for i in range(X_tr_b.shape[1])])
    ]:
        if hasattr(fitted, 'feature_importances_'):
            imp = fitted.feature_importances_
        elif hasattr(fitted, 'coef_'):
            imp = np.abs(fitted.coef_[0])   # absolute coefficients for LR
        else:
            imp = None

        if imp is not None:
            feature_importances[key] = (
                pd.DataFrame({'feature': cols, 'importance': imp})
                .sort_values('importance', ascending=False)
                .reset_index(drop=True)
            )

# ============================================================
# RESULTS SUMMARY TABLE
# ============================================================

results_df = pd.DataFrame(all_metrics)

# clean display copy (drop the dict column for printing)
display_cols = ['Model', 'Feature Set', 'CV AUC (mean)',
                'Accuracy', 'Precision', 'Recall', 'F1', 'AUC-ROC']
print("\n" + "=" * 60)
print("FULL RESULTS SUMMARY")
print("=" * 60)
print(results_df[display_cols].to_string(index=False))

# ============================================================
# IDENTIFY BEST MODEL (by test AUC-ROC)
# ============================================================

best_idx = results_df['AUC-ROC'].idxmax()
best_row = results_df.loc[best_idx]
best_key = f"{best_row['Model']}_{'A' if 'A:' in best_row['Feature Set'] else 'B'}"

print(f"\n★  Best model: {best_row['Model']} | {best_row['Feature Set']}")
print(f"   Test AUC-ROC: {best_row['AUC-ROC']:.4f}")
print(f"   Best params:  {best_row['Best Params']}")

# ============================================================
# VISUALIZATION — ROC CURVES
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, name in enumerate(base_models.keys()):
    ax = axes[idx]

    probs_a = predictions[f"{name}_A"]['y_prob']
    probs_b = predictions[f"{name}_B"]['y_prob']

    fpr_a, tpr_a, _ = roc_curve(y_test, probs_a)
    fpr_b, tpr_b, _ = roc_curve(y_test, probs_b)
    auc_a = roc_auc_score(y_test, probs_a)
    auc_b = roc_auc_score(y_test, probs_b)

    ax.plot(fpr_a, tpr_a, label=f"Loan Only (AUC={auc_a:.4f})", color="steelblue")
    ax.plot(fpr_b, tpr_b, label=f"Loan + Economic (AUC={auc_b:.4f})", color="indianred")
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
    ax.set_title(f"{name}", fontsize=12)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(loc="lower right")

plt.suptitle("ROC Curves: Model A vs Model B (GridSearch-tuned)", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("roc_comparison.png", dpi=150, bbox_inches='tight')
plt.show()

# ============================================================
# FEATURE IMPORTANCE (best model)
# ============================================================

if best_key in feature_importances:
    imp_df = feature_importances[best_key]
    top_15 = imp_df.head(15)

    print(f"\nTop 15 Features ({best_key}):")
    print(top_15.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(top_15)), top_15['importance'], color='steelblue')
    ax.set_yticks(range(len(top_15)))
    ax.set_yticklabels(top_15['feature'], fontsize=9)
    ax.invert_yaxis()
    ax.set_title(f"Top 15 Feature Importances ({best_key})")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig("../figures/feature_importance.png", dpi=150)
    plt.show()

# ============================================================
# FINAL OUTPUTS
# ============================================================
# all_metrics          → list of dicts (one per model variant)
# results_df           → DataFrame of all metrics
# trained_models       → dict of fitted estimators
# predictions          → dict of y_pred / y_prob arrays
# feature_importances  → dict of DataFrames (feature, importance)
```

    Training set: 334792 rows
    Test set: 83699 rows
    Train default rate: 7.91%
    Test default rate: 7.91%
    
    ============================================================
      GridSearchCV: Logistic Regression
    ============================================================
        Best params: {'C': 0.01, 'penalty': 'l1'}
        Best CV AUC: 0.8459
    
      Model A (Loan Only)  — Best params: {'C': 0.01, 'penalty': 'l1'}
        CV AUC:    0.8459
        Accuracy:  0.7683
        Precision: 0.2288
        Recall:    0.8135
        F1:        0.3571
        AUC-ROC:   0.8513
        Best params: {'C': 0.01, 'penalty': 'l1'}
        Best CV AUC: 0.8532
    
      Model B (Loan + Econ) — Best params: {'C': 0.01, 'penalty': 'l1'}
        CV AUC:    0.8532
        Accuracy:  0.7737
        Precision: 0.2337
        Recall:    0.8165
        F1:        0.3634
        AUC-ROC:   0.8578
    
      ➜ AUC Improvement (B − A): +0.0065
    
    ============================================================
      GridSearchCV: Random Forest
    ============================================================
        Best params: {'max_depth': 20, 'min_samples_leaf': 4, 'n_estimators': 200}
        Best CV AUC: 0.9603
    
      Model A (Loan Only)  — Best params: {'max_depth': 20, 'min_samples_leaf': 4, 'n_estimators': 200}
        CV AUC:    0.9603
        Accuracy:  0.9206
        Precision: 0.4989
        Recall:    0.8691
        F1:        0.6339
        AUC-ROC:   0.9622
        Best params: {'max_depth': 20, 'min_samples_leaf': 4, 'n_estimators': 200}
        Best CV AUC: 0.9602
    
      Model B (Loan + Econ) — Best params: {'max_depth': 20, 'min_samples_leaf': 4, 'n_estimators': 200}
        CV AUC:    0.9602
        Accuracy:  0.9428
        Precision: 0.6026
        Recall:    0.8123
        F1:        0.6919
        AUC-ROC:   0.9627
    
      ➜ AUC Improvement (B − A): +0.0004
    
    ============================================================
      GridSearchCV: XGBoost
    ============================================================
        Best params: {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200}
        Best CV AUC: 0.9692
    
      Model A (Loan Only)  — Best params: {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200}
        CV AUC:    0.9692
        Accuracy:  0.9085
        Precision: 0.4615
        Recall:    0.9381
        F1:        0.6186
        AUC-ROC:   0.9707
        Best params: {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200}
        Best CV AUC: 0.9722
    
      Model B (Loan + Econ) — Best params: {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200}
        CV AUC:    0.9722
        Accuracy:  0.9160
        Precision: 0.4839
        Recall:    0.9349
        F1:        0.6378
        AUC-ROC:   0.9735
    
      ➜ AUC Improvement (B − A): +0.0028
    
    ============================================================
    FULL RESULTS SUMMARY
    ============================================================
                  Model        Feature Set  CV AUC (mean)  Accuracy  Precision   Recall       F1  AUC-ROC
    Logistic Regression       A: Loan Only       0.845949  0.768265   0.228767 0.813500 0.357110 0.851321
    Logistic Regression B: Loan + Economic       0.853208  0.773713   0.233745 0.816521 0.363447 0.857817
          Random Forest       A: Loan Only       0.960297  0.920573   0.498873 0.869073 0.633880 0.962218
          Random Forest B: Loan + Economic       0.960235  0.942771   0.602622 0.812292 0.691922 0.962656
                XGBoost       A: Loan Only       0.969226  0.908494   0.461481 0.938085 0.618633 0.970657
                XGBoost B: Loan + Economic       0.972211  0.915973   0.483937 0.934914 0.637754 0.973476
    
    ★  Best model: XGBoost | B: Loan + Economic
       Test AUC-ROC: 0.9735
       Best params:  {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200}



    
![png](pipeline_files/pipeline_23_1.png)
    


    
    Top 15 Features (XGBoost_B):
                                    feature  importance
                     loan_terms.term_months    0.336441
                   loan_terms.variable_rate    0.085418
                   loan_terms.guarantee_pct    0.076725
                    geography.bank_in_state    0.054997
                   loan_terms.interest_rate    0.038336
                 loan_terms.revolver_status    0.037676
                 geography.project_in_state    0.031124
    economic_snapshot.national_unemployment    0.028918
                  loan_terms.gross_approval    0.018182
                   business.naics_sector_72    0.017258
           economic_snapshot.fed_funds_rate    0.015356
                economic_snapshot.state_gdp    0.013882
                   business.naics_sector_45    0.010732
          business.business_type_INDIVIDUAL    0.009982
      economic_snapshot.consumer_confidence    0.009944



    
![png](pipeline_files/pipeline_23_3.png)
    


### Main Takeaways: 
- Logistic regression is largely outperformed by the more advanced gradient boosting and random forest models
- Although it is very very small the AUC is greater for model B (full) across all three models
  - precision, accuracy, and F1 scores all have more significant differences across types of models
- The random forest model appears to have the greatest discrepancy between model A and model B performance

## Final Analysis Visualization

Rationale: 
1) For the first visualization I chose to create grouped bar charts of performance metrics for the baseline and full models. By putting the bars side by side with numeric labels on top, difference can be easily compared. I chose to visualize all three models rather than just one because I felt all three models told a different story and I wanted to paint a complete picture. I chose to group the bars by metric rather than model type or model A/B because I felt this best communicated difference between the two datasets. I also chose to add a brief explanation of what the metrics meant at the bottom of each graph to make the meaning clear to non-technical viewers.
2) For the second visualization I chose to plot all of the top feature importances for each model in a horizontal bar chart. Since each model had a different top ten each graph needed its own labels. I bolded the features that were geographically related as this is the focus of the project.



```python
# Split results into A and B
model_a_outputs = results_df[results_df['Feature Set'].str.contains('A:')].reset_index(drop=True)
model_b_outputs = results_df[results_df['Feature Set'].str.contains('B:')].reset_index(drop=True)

metrics_to_plot = ['Accuracy', 'AUC-ROC', 'F1']
metric_descriptions = {
    'Accuracy':  'Share of all predictions (default and non-default) the model got right.',
    'AUC-ROC': 'Ability to distinguish defaulters from non-defaulters across all thresholds.',
    'F1': 'Balances catching defaults vs. false alarms.'
}

model_names = model_a_outputs['Model']
x = np.arange(len(model_names))
width = 0.32


fig = plt.figure(figsize=(18, 8), facecolor='#FAFAFA')

# defining custom layout
gs = gridspec.GridSpec(
    3, 3,
    height_ratios=[0.08, 1, 0.12],
    hspace=0.35, wspace=0.45,
    right = 0.96  # was 0.28
)

# Creating shared legend
ax_legend = fig.add_subplot(gs[0, :])
ax_legend.axis('off')
dummy_a = ax_legend.bar([0], [0], color='#4878A8', alpha=0.85, label='Model A — Loan Only')
dummy_b = ax_legend.bar([0], [0], color='#C45C5C', alpha=0.85, label='Model B — Loan + Economic Context')

# Defining legend foramtting
ax_legend.legend(
    handles=[dummy_a, dummy_b],
    loc='center', ncol=2, fontsize=11,
    frameon=False, handlelength=1.0,
    handletextpad=0.4, columnspacing=1.5 
)

# Creating bar charts
for i, metric in enumerate(metrics_to_plot):
    ax = fig.add_subplot(gs[1, i])

    # separating into model A and B for side by side
    bars_a = ax.bar(x - width/2, model_a_outputs[metric], width,
                    color='#4878A8', alpha=0.85, edgecolor='white', linewidth=0.8)
    bars_b = ax.bar(x + width/2, model_b_outputs[metric], width,
                    color='#C45C5C', alpha=0.85, edgecolor='white', linewidth=0.8)

    # value labels
    for bar in bars_a:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f"{bar.get_height():.3f}", ha='center', va='bottom',
                fontsize=8.5, color='#333333', fontweight='medium')
    for bar in bars_b:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f"{bar.get_height():.3f}", ha='center', va='bottom',
                fontsize=8.5, color='#333333', fontweight='medium')

    ax.set_title(metric, fontsize=14, fontweight='bold', color='#222222', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, fontsize=9.5, color='#444444')
    ax.set_ylim(0, 1.08)
    ax.set_ylabel('')

    # Styling for newspaper-like look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(axis='y', colors='#888888', labelsize=8.5)
    ax.tick_params(axis='x', colors='#888888')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#AAAAAA')
    ax.set_axisbelow(True)

# Brief descriptions of metrics
for i, metric in enumerate(metrics_to_plot):
    ax_desc = fig.add_subplot(gs[2, i])
    ax_desc.axis('off')
    ax_desc.text(
        0.5, 1.0,
        metric_descriptions[metric],
        ha='center', va='top',
        fontsize=9, fontstyle='italic', color='#666666',
        wrap=True,
        transform=ax_desc.transAxes
    )

# Title
fig.suptitle(
    "Does State and National Level Economic Context Improve Loan Default Prediction?",
    fontsize=18, fontweight='bold', color='#1a1a1a',
    y=0.98
)

plt.savefig("../figures/model_performance_comp.png", dpi=200, bbox_inches='tight', facecolor='#FAFAFA')
plt.show()
```


    
![png](pipeline_files/pipeline_27_0.png)
    


The plots above show that there is the biggest difference between performance of the baseline and the full mode


```python
# plotting top 10 feature importances for all 3 best models
logistic_reg_feature_imp = feature_importances.get('Logistic Regression_B')
random_forest_feature_imp = feature_importances.get('Random Forest_B')
xgb_feature_imp = feature_importances.get('XGBoost_B')

top_n = 10
fig, axes = plt.subplots(1, 3, figsize=(24, 6))
fig.suptitle("Most Important Factors in Model Decisions",
             fontsize=16, fontweight='bold', color='#1a1a1a', y=1.02)

# looping over feature importances to plot
for ax, imp_df, title in zip(
    axes,
    [logistic_reg_feature_imp, random_forest_feature_imp, xgb_feature_imp],
    ['Logistic Regression', 'Random Forest', 'XGBoost']
):
    if imp_df is not None:
        top_features = imp_df.head(top_n)

        # clean up feature names
        clean_names = (top_features['feature']
                       .str.replace('.', ' → ', regex=False)
                       .str.replace('_', ' ')
                       .str.title())

        ax.barh(range(top_n), top_features['importance'],
                color='#4878A8', alpha=0.85, edgecolor='white', linewidth=0.5)

        ax.set_yticks(range(top_n))
        ax.set_yticklabels([]) 
        ax.invert_yaxis()

        # add labels individually, bold if economic snapshot
        for j, name in enumerate(clean_names):
            weight = 'bold' if 'Economic Snapshot' in name else 'normal'
            color = '#1a1a1a' if 'Economic Snapshot' in name else '#333333'
            ax.text(-0.01, j, name, ha='right', va='center',
                    fontsize=8.5, fontweight=weight, color=color,
                    transform=ax.get_yaxis_transform())

        ax.set_title(title, fontsize=13, fontweight='bold', color='#222222', pad=10)

        # cleaning up formatting
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#CCCCCC')
        ax.tick_params(axis='y', length=0)
        ax.tick_params(axis='x', colors='#888888', labelsize=0)
        ax.grid(axis='x', linestyle='--', alpha=0.3, color='#AAAAAA')
        ax.set_axisbelow(True)
        ax.set_xticks([])
        ax.spines['bottom'].set_visible(False)

plt.subplots_adjust(wspace=0.55)
plt.savefig("../figures/feature_importance_comparison.png", dpi=200, bbox_inches='tight', facecolor='white')
plt.show()
```


    
![png](pipeline_files/pipeline_29_0.png)
    

