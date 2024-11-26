# config.py
STAGING_URL = "https://myzenwel.indociti.com/"
PRODUCTION_URL = "https://dashboard.zenwel.com"

def get_url_based_on_environment(environment):
    if environment == 'staging':
        return STAGING_URL
    elif environment == 'production':
        return PRODUCTION_URL
    else:
        raise ValueError("Environment not recognized. Please set 'staging' or 'production'.")