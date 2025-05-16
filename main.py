# from fastapi import FastAPI
# from pydantic import BaseModel
# import joblib
# import pandas as pd
# import tldextract
# import re
# from urllib.parse import urlparse
# import ipaddress

# # Load the trained model
# model = joblib.load("random_forest_model.pkl")

# app = FastAPI()

# class URLItem(BaseModel):
#     url: str

# def extract_url_features(url):
#     features = {}
    
#     # Length based features
#     features['url_length'] = len(url)
#     features['num_dots'] = url.count('.')
#     features['num_hyphens'] = url.count('-')
#     features['num_slashes'] = url.count('/')
#     features['num_params'] = url.count('&')
#     features['has_https'] = int('https' in url)
    
#     # Domain & IP based features
#     try:
#         ipaddress.ip_address(urlparse(url).hostname)
#         features['has_ip'] = 1
#     except:
#         features['has_ip'] = 0
    
#     # TLD and domain part
#     ext = tldextract.extract(url)
#     features['tld'] = ext.suffix
#     features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0

#     # Suspicious words
#     suspicious_words = ['login', 'secure', 'update', 'free', 'confirm', 'account', 'bank']
#     features['suspicious_words'] = sum(word in url.lower() for word in suspicious_words)
    
#     return features

# @app.post("/predict")
# def predict_url(data: URLItem):
#     # Extract features
#     features = extract_url_features(data.url)

#     # Convert to DataFrame
#     input_df = pd.DataFrame([features])
    
#     # One-hot encode (for tld)
#     input_df = pd.get_dummies(input_df)
    
#     # Align with model training columns
#     model_columns = joblib.load("model_columns.pkl")  # Save your training column order
#     input_df = input_df.reindex(columns=model_columns, fill_value=0)

#     # Predict
#     prediction = model.predict(input_df)[0]
#     probability = model.predict_proba(input_df)[0].max()

#     return {
#         "url": data.url,
#         "prediction": int(prediction),
#         "confidence": round(probability, 4)
#     }

from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import re
import math
import tldextract

app = FastAPI()

class URLItem(BaseModel):
    url: str

def extract_url_features(url: str):
    try:
        if not isinstance(url, str) or url.strip() == "":
            raise ValueError("Invalid URL format")

        parsed = urlparse(url)
        ext = tldextract.extract(url)

        def get_entropy(s):
            prob = [float(s.count(c)) / len(s) for c in set(s)]
            entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
            return round(entropy, 4)

        domain = ext.domain + '.' + ext.suffix if ext.suffix else ext.domain
        subdomain_parts = ext.subdomain.split('.') if ext.subdomain else []

        features = {
            'url_length': len(url),
            'has_ip_address': 1 if re.match(r'http[s]?://(?:\d{1,3}\.){3}\d{1,3}', url) else 0,
            'num_dots': url.count('.'),
            'has_hyphen': 1 if '-' in ext.domain else 0,
            'has_at_symbol': 1 if '@' in url else 0,
            'has_double_slash_redirect': 1 if url.count('//') > 1 else 0,
            'num_digits': sum(c.isdigit() for c in url),
            'url_entropy': get_entropy(url),
            'has_https': 1 if parsed.scheme == 'https' else 0,
            'num_special_chars': len(re.findall(r'[^\w\s]', url)),
            'domain_length': len(domain),
            'subdomain_count': len(subdomain_parts),
        }

    except Exception:
        features = {
            'url_length': 0,
            'has_ip_address': 0,
            'num_dots': 0,
            'has_hyphen': 0,
            'has_at_symbol': 0,
            'has_double_slash_redirect': 0,
            'num_digits': 0,
            'url_entropy': 0,
            'has_https': 0,
            'num_special_chars': 0,
            'domain_length': 0,
            'subdomain_count': 0,
        }

    return features

@app.post("/predict")
def predict_phishing(item: URLItem):
    features = extract_url_features(item.url)
    
    # Placeholder prediction logic, replace with your model
    prediction = "phishing" if features['has_https'] == 0 else "legitimate"
    
    return {
        "url": item.url,
        "features": features,
        "prediction": prediction
    }
