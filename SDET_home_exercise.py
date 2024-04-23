import os
import time
import csv
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

# The input_keys enters the keys into specified bowl, the input list is id of gold bars and bowl is left or right
def input_keys(input_list, bowl):
    n = len(input_list)
    for i in range(n):
        input_field = driver.find_element(By.ID, f"{bowl}_{i}")
        input_field.clear()
        input_field.send_keys(input_list[i])

# This function returns the bowl of less weight ,ie it returns given a list of inputs, it returns the list which has fake gold bar
def group_of_fake_gold(group1,group2,group3):
    #Click to reset weights from both bowls
    resetbutton = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[4]/button[1]")
    resetbutton.click()

    time.sleep(2)

    # Enter the weights to left and right bowls
    input_keys(group1,"left")
    input_keys(group2,"right")

    # Click on weight button
    weighbutton = driver.find_element(By.ID, "weigh")
    weighbutton.click()

    time.sleep(2)

    # Find the logic symbol in between the bowls
    symbolbutton = driver.find_element(By.ID, "reset")
    symbol_text = symbolbutton.text
    
    if symbol_text == "=":
        return group3
    if symbol_text == "<":
        return group1
    else:
        return group2
    time.sleep(2)

#This function finds the fake gold bar from the list of 9 gold bars
def find_fake_gold_bar(gold_bars):
    
    # We are going to divide the gold bars into group of 3
    group_size = len(gold_bars) // 3
    group1 = gold_bars[:group_size]
    group2 = gold_bars[group_size:2*group_size]
    group3 = gold_bars[2*group_size:]
    
    # Find the fake group containig gold bar
    fake_group = group_of_fake_gold(group1, group2, group3)
    
    # Once we got group containing fake group, we find the fake gold bar in that group
    fake_bar = group_of_fake_gold([fake_group[0]], [fake_group[1]], [fake_group[2]])

    # Click on fake gold bar
    coinbutton = driver.find_element(By.ID, "coin_" + str(fake_bar[0]))
    coinbutton.click()

    print("Fake gold bar is: " + str(fake_bar[0]))
    time.sleep(2)

    #Match the alert statement using below logic
    try:
        alert = Alert(driver)

        alert_text = alert.text

        expected_text = "Yay! You find it!"

        if alert_text == expected_text:
            print("Pop-up text is correct:", alert_text)
        else:
            print("Pop-up text is incorrect. Expected:", expected_text, "Actual:", alert_text)

        alert.dismiss()

    except Exception as e:
        print("An error occurred while handling the alert:", e)

    # Find the element with class 'game-info' to find the list of "Weighings"
    game_info_element = driver.find_element(By.CLASS_NAME, 'game-info')

    # Get the text from the element
    game_info_text = game_info_element.text

    print(game_info_text)

# This is the starting function to start this game   
def game():
    find_fake_gold_bar(range(9))
    time.sleep(2)

try:
    # Get the directory path of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Path to chromedriver executable (relative path)
    PATH = os.path.join(script_dir, "chromedriver-win64", "chromedriver.exe")

    # Path to chromedriver executable
    #PATH = r"C:\Users\kpsag\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    # Create a driver to access website
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    timeout = 10
    service = Service(PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    driver.get("http://sdetchallenge.fetch.com/")
    time.sleep(2)
    
    game()

except Exception as e:
    print("An error occurred:", e)
finally:
    print("Program ended")
    driver.quit()
