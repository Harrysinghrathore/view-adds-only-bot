# Import necessary modules
import logging
import random
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

# FileHandler class definition
class FileHandler:
    def __init__(self, proxies_file_path, login_credentials_file_path, channels_file_path):
        self.proxies_file_path = proxies_file_path
        self.channels_file_path = channels_file_path
        self.login_credentials_file_path = login_credentials_file_path

    # Function to read proxies from an Excel file
    def read_proxies_from_excel(self, ip_col_index=0, port_col_index=1):
        try:
            proxies_df = pd.read_excel(self.proxies_file_path, header=None, engine='openpyxl')
            proxies_list = [(row[ip_col_index], row[port_col_index]) for index, row in proxies_df.iterrows()]
            return proxies_list
        except Exception as e:
            logging.error(f"Error reading proxies from Excel: {e}")
            return []

    # Function to read login credentials from an Excel file
    def read_login_credentials_from_excel(self, email_col_index=0, password_col_index=1, recovery_email_col_index=2):
        try:
            credentials_df = pd.read_excel(self.login_credentials_file_path, header=None)
            credentials_list = [
                (row[email_col_index], row[password_col_index], row[recovery_email_col_index])
                for index, row in credentials_df.iterrows()
            ]
            return credentials_list
        except Exception as e:
            logging.error(f"Error reading login credentials from Excel: {e}")
            return []
        
    def read_channels_from_excel(self):
        try:
            channels_data = pd.read_excel(self.channels_file_path, header=None)
            channels_list = channels_data.values.tolist()
            print(channels_list)
            return channels_list
        except Exception as e:
            logging.error(f"Error reading channels from Excel: {e}")
            return []


    # Function to select a random proxy from a list
    def select_random_proxy(self, proxies_list):
        if proxies_list:
            selected_proxy = random.choice(proxies_list)
            ip, port = selected_proxy
            return f"socks5://{ip}:{port}"
        else:
            return None

    # Function to select random login credentials from a list
    def select_random_login_credentials(self, login_credentials_list):
        if login_credentials_list:
            selected_credentials = random.choice(login_credentials_list)
            email, password, recovery_email = selected_credentials
            return email, password, recovery_email
        else:
            return None

# End of FileHandler.py
