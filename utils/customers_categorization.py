from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def categorize_customers(df):
    # Define column transformer with OneHotEncoder and StandardScaler
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["income", "age"]),
            ("cat", OneHotEncoder(), ["gender", "job", "city", "hobby"]),
        ]
    )

    # Create a pipeline with preprocessing, PCA and KMeans
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("pca", PCA(n_components=2)),  # Reduce dimensions for better clustering
            (
                "kmeans",
                KMeans(n_clusters=4, random_state=42, n_init=10, init="k-means++"),
            ),  # n_init and init for better results
        ]
    )

    # Fit the pipeline
    pipeline.fit(df)

    # Predict the clusters
    df["Category"] = pipeline.named_steps["kmeans"].labels_

    # Rearrange the dataframe according to the category column
    df = df.sort_values("Category").reset_index(drop=True)

    return df


print(categorize_customers(pd.read_csv("./customers.csv")))
