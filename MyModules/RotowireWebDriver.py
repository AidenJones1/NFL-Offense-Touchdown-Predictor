# Imported Modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO
from sys import exit
import pandas as pd

def GetDataFrameFromGameID(gameID: str):
    """
    Access the url to scrape both team stats from the specified game ID and returns it as a DataFrame
    Parameters:
        gameID (str): The ID of the NFL game according to rotowire.com
    Returns:
        DataFrame: Both team stats from the game
    """

    # Construct url to access
    base_URL = "https://www.rotowire.com/football/box-score-teamstats.php?gameID="
    url = base_URL + gameID
    
    # Initialize Web Driver
    driverExe = "chromedriver"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)

    # Access the URL and wait for the table to load for parsing
    try:
        driver.get(url)

        # Get table element containing both team stats
        tableElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "full-width")))
        tableHTML = tableElement.get_attribute("outerHTML")
        tableDF = pd.read_html(StringIO(tableHTML))[0]
    
    except TimeoutException:
        driver.quit()
        print("Timed Out!!! Retrying...")
        return GetDataFrameFromGameID(gameID)
    
    except ValueError or UnboundLocalError:
        exit(f"INVALID GAME ID: Most likely an invalid ID was found in the Game IDs txt file. Perhaps changing or removing the invalid ID ({gameID})")

    driver.quit()
    return tableDF