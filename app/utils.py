import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data():
    df = pd.read_csv('data/creditcard.csv')
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    features = df.drop(['Class', 'Time'], axis=1)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    df_scaled = pd.DataFrame(scaled, columns=features.columns)
    df_scaled['Class'] = df['Class']
    return df_scaled