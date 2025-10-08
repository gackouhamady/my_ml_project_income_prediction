# 💰 Census Income Classification (U.S. CPS/ASEC 2019)

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](#-getting-started)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Dataset](https://img.shields.io/badge/Dataset-Census%20Income%20(ASEC)-lightgrey)](#-dataset)
[![Reproducible](https://img.shields.io/badge/Reproducible-Yes-success)](#-configuration)
[![CI Ready](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=github)](#-project-structure)

> Predict whether an individual’s annual income exceeds **$50K** using the U.S. **Current Population Survey (CPS) / Annual Social and Economic (ASEC)** dataset — one of the most comprehensive labor, income, and demographic datasets in the U.S.

---

## 📦 Project Overview

This project builds a **binary classification** model to predict income level (`≤50K` or `>50K`) based on demographic and employment attributes from the **CPS ASEC microdata**.  
The workflow follows a **reproducible ML pipeline** with well-defined configuration and modular code organization.

---

## 🧱 Project Structure

```bash
census-income-classification/
├── data/
│   ├── raw/                  # Raw CPS/ASEC or extracted UCI files
│   ├── interim/              # Cleaned intermediate files
│   └── processed/            # Final ML-ready datasets
├── models/                   # Saved models, checkpoints
├── reports/
│   ├── figures/              # Visualizations (EDA, feature importance)
│   └── metrics/              # Performance logs / JSON reports
├── scripts/
│   ├── preprocess.py         # Feature cleaning, encoding, scaling
│   ├── train.py              # Baseline & advanced model training
│   ├── evaluate.py           # Metrics computation (AUC, F1, etc.)
│   └── infer.py              # Predict new samples
├── src/
│   ├── dataio/               # Data loading and utilities
│   ├── features/             # Preprocessing pipeline
│   ├── models/               # ML algorithms (sklearn, XGBoost)
│   ├── metrics/              # Custom metrics for imbalanced data
│   └── utils/                # Logging, config parsing
├── utils/
│   └── __init__.py
├
│── 01_EDA.ipynb
│── 02_Baseline_Experiment.ipynb
│── 03_Final_Model_Experiment.ipynb
├── config.yml                # YAML configuration (paths, hyperparams)
├── requirements.txt          # Dependencies
├── start.sh                  # Environment bootstrap script
├── LICENSE                   # MIT license
└── README.md
````

##  Dataset

- Source: U.S. Census Bureau — CPS ASEC
 

- census_income_additional_info

- Donors: Terran Lane & Ronny Kohavi, Silicon Graphics

- census_income_metadata

- Task: Predict income threshold at $50K

- Train instances: 199,523 (46,716 duplicates)

- Test instances: 99,762 (20,936 duplicates)

- Features: 40 (7 continuous, 33 nominal)

- Class imbalance:

- ≤ $50K → 93.8%

- $50K → 6.2%

- Weights: Each record has an instance weight representing population counts (used for analysis, not model fitting).

- ⚠️ Use the instance_weight only for evaluation or weighted metrics, not for training ML models.

## Configuration

- Example (config.yml):
``` yaml
project: census-income-classification
seed: 42
data:
  raw_dir: data/raw
  processed_dir: data/processed
target: income
weights_column: instance_weight
preprocessing:
  missing_strategy: median
  encoder: onehot
  scale: true
modeling:
  baseline: logistic_regression
  advanced: xgboost
cv:
  n_splits: 5
  stratify: true
metrics: [accuracy, f1, auroc, auprc]

```
## Getting Startet
``` powershell
# 1️⃣ Create virtual environment
python -m venv .venv && source .venv/bin/activate

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Prepare data
python scripts/preprocess.py --config config.yml

# 4️⃣ Train baseline model
python scripts/train.py --config config.yml

# 5️⃣ Evaluate results
python scripts/evaluate.py --config config.yml

```
| Feature Example              | Description                         |
| ---------------------------- | ----------------------------------- |
| `age`                        | Continuous — age in years           |
| `education`                  | Highest educational attainment      |
| `occupation code`            | Detailed occupation recode          |
| `capital gains/losses`       | Continuous values                   |
| `marital status`             | Married / Never-married / Separated |
| `weeks worked`               | Number of working weeks in the year |
| `sex`, `race`, `citizenship` | Demographic features                |
| `income` *(target)*          | `≤50K` or `>50K`                    |

## Models

- Baselines: Logistic Regression, Random Forest, Naive Bayes

- Boosted Trees: XGBoost / LightGBM

- Handling Imbalance: Class weights, SMOTE, threshold tuning

- Metrics: AUROC, AUPRC, F1, Recall@Precision≥90%

## Notebooks

- 01_EDA.ipynb — Feature distributions, correlation heatmaps

- 02_Baseline_Experiment.ipynb — Logistic regression / Random forest

- 03_Final_Model_Experiment.ipynb — Hyperparameter tuning, feature importance, explainability (SHAP)

## Reproducibility

- Seeds fixed in config.yml

- Deterministic CV splits

- Versioned environments (requirements.txt)

- Modular scripts for pipeline reproducibility

## License

- This project is licensed under the MIT License — see the LICENSE file for details.

## References

- U.S. Census Bureau, Current Population Survey: 2019 ASEC Technical Documentation

- census_income_additional_info

- Census Income Metadata (Terran Lane & Ronny Kohavi, SGI)

- census_income_metadata
