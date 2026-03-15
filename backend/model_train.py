import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset/health_lifestyle_dataset.csv")

# If dataset loaded as one column, fix it
if len(df.columns) == 1:
    df = df[df.columns[0]].str.replace('"','').str.split(",", expand=True)

    df.columns = [
        "id","age","gender","bmi","daily_steps","sleep_hours","water_intake_l",
        "calories_consumed","smoker","alcohol","resting_hr","systolic_bp",
        "diastolic_bp","cholesterol","family_history","disease_risk"
    ]

print("Columns:", df.columns)

# Convert numeric columns
numeric_cols = [
    "age","bmi","daily_steps","sleep_hours","water_intake_l",
    "calories_consumed","smoker","alcohol","resting_hr",
    "systolic_bp","diastolic_bp","cholesterol","family_history","disease_risk"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col])

# Encode gender
encoder = LabelEncoder()
df["gender"] = encoder.fit_transform(df["gender"])

# Drop id
df = df.drop("id", axis=1)

# Features and target
X = df.drop("disease_risk", axis=1)
y = df["disease_risk"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=200)

model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# Save model
joblib.dump(model, "models/health_model.pkl")

print("Model trained and saved!")