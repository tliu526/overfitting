#%% [markdown]
# # Kaggle Don't Overfit II scraping
# The goal here is to scrape all the test set predictions provided
# on the kaggle notebooks page https://www.kaggle.com/c/dont-overfit-ii/notebooks
# 
# ## Things to scrape
# 1. any output csv files that match the shape of the test set submission
# 2. the user's public and private leaderboard scores


# %% imports

import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import pickle
import time
from urllib.parse import urlparse

# %% get initial notebook listing
# Unfortunately, kaggle pages are dynamic javascript, so requests/beautifulsoup doesn't work
base_url = "https://www.kaggle.com/c/dont-overfit-ii/notebooks"
PAGE_SIZE = 1000
COMPETITION_ID = 12896 # dont-overfit-ii competition id

query_params = {
    'sortBy': 'scoreDescending', # sorts by notebook scores
    'group': 'everyone',
    'pageSize': PAGE_SIZE,
    'competitionId': COMPETITION_ID,
    'outputType': 'Data' # only pull notebooks that have output data files
}

notebooks_req = requests.get(base_url, params=query_params)

# %% initial parse tree exploration

notebooks_soup = BeautifulSoup(notebooks_req.text, "lxml")

# %%
competition_container = notebooks_soup.find("div", {"data-component-name": "CompetitionContainer"})

for child in competition_container.children:
    print(child)
    idx += 1

print(idx)

# %% Selenium test

options = Options()
options.headless = True
full_url = "https://www.kaggle.com/c/dont-overfit-ii/notebooks?sortBy=hotness&group=everyone&pageSize=100000&competitionId=12896&outputType=Data"
driver = webdriver.Firefox(options=options)
driver.get(full_url)


# %% scroll to bottom of page
# https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# %% get hrefs to notebooks
elements = driver.find_elements_by_class_name("block-link__anchor")

links = []
for child in elements:
    links.append(child.get_attribute("href"))

print(len(links))

# %% testing to see if the notebook page has static content
# the answer is...nope
notebook_url = "https://www.kaggle.com/derekpowll/bayesian-lr-w-cauchy-prior-in-pymc3"

notebook_req = requests.get(notebook_url)
notebook_soup = BeautifulSoup(notebook_req.text, "lxml")
notebook_soup.find("div")


# %% Selenium pull of notebook pages
notebook_url = "https://www.kaggle.com/derekpowll/bayesian-lr-w-cauchy-prior-in-pymc3"
driver.get(notebook_url)


# %% get submission link (not needed)
download_button = driver.find_element_by_class_name("kernel-files-pane__download-all-button")
print(download_button.get_attribute("href"))


# %% pull scores
private_pane = driver.find_element_by_class_name("kernel-code-pane__submission-score-private")
public_pane = driver.find_element_by_class_name("kernel-code-pane__submission-score-public")

print(private_pane.find_element_by_class_name("kernel-code-pane__submission-score-value").text)
print(public_pane.find_element_by_class_name("kernel-code-pane__submission-score-value").text)


# %% pull all scores
scores_dict = {}

for link in links:
    print(link)
    driver.get(link)

    kernel_name = urlparse(link).path[1:]
    private_score = None
    public_score = None

    try:
        private_pane = driver.find_element_by_class_name("kernel-code-pane__submission-score-private")
        private_score = private_pane.find_element_by_class_name("kernel-code-pane__submission-score-value").text
    except Exception as e:
        print(e)
    
    try:
        public_pane = driver.find_element_by_class_name("kernel-code-pane__submission-score-public")
        public_score = public_pane.find_element_by_class_name("kernel-code-pane__submission-score-value").text
    except Exception as e:
        print(e)

    scores_dict[kernel_name] = (private_score, public_score)

#print(scores_dict)

pickle.dump(scores_dict, open("dont-overfit-ii/scores.dict", "wb"), -1)

# %% write kernel names to file
with open("dont-overfit-ii/kernels.txt", "a") as f:
    for link in links:
        f.write(urlparse(link).path[1:] + "\n")
# download command: kaggle kernels output <kernel name>


