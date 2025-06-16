from sklearn.ensemble import IsolationForest

def train_model(df):
    X = df.drop('Class', axis=1)
    model = IsolationForest(contamination=0.001, random_state=42)
    model.fit(X)
    return model