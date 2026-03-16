import pandas as pd

df = pd.read_csv("C:/Users/RAVI/Desktop/smart-healthcare-system/backend/dataset/health_lifestyle_dataset.csv")
print(df["disease_risk"].value_counts())