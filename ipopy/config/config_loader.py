import configparser
from ipopy.utils.urls import CONFIG_FILE_PATH

# Initialize the configparser
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

# Parsing configurations:

# IPO Premium configurations
IPO_PREMIUM_TABLE_CLASS = config["IpoPremium"]["table_class"]
IPO_PREMIUM_DATE_FORMAT = config["IpoPremium"]["date_format"]
IPO_PREMIUM_COLUMNS_ORDER = tuple(
    map(
        lambda x: int(x) if x != "None" else None,
        config["IpoPremium"]["desired_columns_order"].split(","),
    )
)

# GMP Today configurations
GMP_TODAY_TABLE_ROWS_XPATH = config["GmpToday"]["table_rows_xpath"]
GMP_TODAY_DATE_FORMAT = config["GmpToday"]["date_format"]
GMP_TODAY_COLUMNS_ORDER = tuple(
    map(
        lambda x: int(x) if x != "None" else None,
        config["GmpToday"]["desired_columns_order"].split(","),
    )
)

# WhatsApp configurations
WHATSAPP_SEARCH_BOX_XPATH = config["WhatsApp"]["search_box_xpath"]
WHATSAPP_MESSAGE_TEXTFIELD_XPATH = config["WhatsApp"]["message_textfield_xpath"]

# Chrome configurations
CHROME_PROFILE_PATH = config["Chrome"]["chrome_profile_path"]
