#!/usr/bin/env python3

# Load the dataset
df = pd.read_csv("reviewed_dataset.csv")  # Make sure the file is in the same directory

# Show original missing values
print("Missing values before cleaning:")
print(df.isna().sum())

# Drop missing values
df = df.dropna()

# Show result
print("\nCleaned DataFrame:")
print(df.head())

# Save cleaned version (optional)
df.to_csv("cleaned_dataset.csv", index=False)
print("\nSaved cleaned data as cleaned_dataset.csv")
