# CarSathi AI — Split Jupyter Notebooks

The original `02_data_understanding.ipynb` was split into focused notebooks.

## Recommended execution order

1. `01_data_understanding.ipynb` — raw dataset understanding
2. `02_missing_data.ipynb` — missing values and data-quality investigation
3. `03_data_cleaning.ipynb` — cleaning and ML dataset creation
4. `04_eda.ipynb` — exploratory data analysis
5. `05_model_training.ipynb` — model training
6. `06_model_evaluation.ipynb` — evaluation and tuning
7. `07_pipeline_prediction.ipynb` — final pipeline and prediction

## Important

- The notebooks preserve the original notebook's code sections rather than replacing them with a new workflow.
- The cleaning notebook additionally saves `cars_ml.csv` into the project's `data/processed` folder.
- Later notebooks load that processed dataset so each notebook does not depend on variables remaining in another notebook's Jupyter kernel.
- Update the Windows paths in the setup cells if your project folder is different.
