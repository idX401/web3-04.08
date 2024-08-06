import os
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

HOST = "127.0.0.1"
PORT = "3001"
SEED_FILE = "seed.txt"
AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYTE3ZGU1ZmZlMGFlOGQwNDA3YjVmNzU2NjkxMTFmYjA5YTNkMTQ1Nzk0MzQ0ODc2Y2EwMWEwMWZjYmU4MmRiZTc3NmEzOTA2ODY0OGNiNmEiLCJpYXQiOjE3MjI3NjU1OTkuOTAyNzMzLCJuYmYiOjE3MjI3NjU1OTkuOTAyNzM1LCJleHAiOjE3MjUzNTc1OTkuODkxMDQyLCJzdWIiOiIzMTMzMTM0Iiwic2NvcGVzIjpbXX0.SYWv11VBzwZRaUUzyPmavZfrJ0ukqOixhIJXxVFnKXfpgsglp2CWBeKLh9iqV64QKRaOUJ6WRvuEiuJi_oz22l4BtpojxT7JWotlESWPYIAmFDsm77NQqboi4qWED0XndTHllFuOWtCFxZuHUSOumwePYQK6ePVyMJH73SwKOQN9IURJIJPs7ytEFNrquX64KFx1X_9wUsmpv3ry6Wo0GXbJ7JFBnreUDyezktRg-ZxY2A0Vr8lxXGv9tx2ma_7Sj-y1lBnxz5XRf5owc_7x7Bx36RPX_4IWYOEiNIJoZs-txX_BLOtZoj_rpYcJbLgXSx0W2zKNDP2UrdWFnuQdrh-6tduMxfaTAR2FODgdQw6KHltp94xomMCu-bxHDHJAhPmifv1fFrETgofLi8BvOpyOsaOURrzG03hQMfW4_C9HiVLh4Xcgami3FSw7AL9ITZSUDVLe7ibIUDUnNjaIzShrSFt11Yyf7yo2OmaH57m56r923wzZQrgJHBwrUOKiuvQSWkWS9V7IfrZXRo107mruBAgU037bqB-WLjgimTzSmMFoMuYR4OBsN0cWAN2Wazv-9zlMkykObyMy6vGIqjSVNwJeSnsDLPsTPqYVpZzS--nIqVI5xR3e1wQty0zA3Sm7iFGZGCzLp8VgC2NS2M-t_feYY2BX7Ig-XPOzY_A"
PASSWORD = "cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm"


def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {message}")


def get_profile(profile_id=""):
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.get(
        f"https://dolphin-anty-api.com/browser_profiles/{profile_id}", headers=headers
    )
    result = json.loads(response.text)
    return result


def start_profile(profile_id):
    return f"http://{HOST}:{PORT}/v1.0/browser_profiles/{profile_id}/start?automation=1"


def stop_profile(profile_id):
    return f"http://{HOST}:{PORT}/v1.0/browser_profiles/{profile_id}/stop"


def remote_profile(remote_host, remote_port):
    options = webdriver.ChromeOptions()
    options.debugger_address = f"127.0.0.1:{remote_port}"
    driver = webdriver.Chrome(options=options)
    return driver


def get_seed_phrases(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def get_dolphin_profiles():
    list_profile = []
    for index, profile in enumerate(get_profile()["data"]):
        list_profile.append({"id": profile["id"], "name": profile["name"]})
    list_profile = sorted(list_profile, key=lambda k: (k["id"], k["name"]))
    return list_profile


def metamask(profile_id, seed_phrase):
    response = requests.get(start_profile(profile_id))
    result = json.loads(response.text)
    log(result)

    try:
        remote_host = HOST
        remote_port = result["automation"]["port"]
    except:
        input("Press enter to exit")
        exit()

    log("Starting chrome driver")
    driver = remote_profile(remote_host, remote_port)
    #
    #
    time.sleep(3)
    driver.get("chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html")
    time.sleep(12)
    firstCheckbox = driver.find_element(
        By.XPATH, '//*[@id="onboarding__terms-checkbox"]'
    )
    firstCheckbox.click()
    time.sleep(3)
    firstButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button'
    )
    firstButton.click()
    time.sleep(3)
    secondButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[2]'
    )
    secondButton.click()
    time.sleep(3)
    #
    wordsCount = len(seed_phrase.split())
    selectorId = 1
    if wordsCount == 15:
        selectorId = 2
    elif wordsCount == 18:
        selectorId = 3
    elif wordsCount == 21:
        selectorId = 4
    elif wordsCount == 24:
        selectorId = 5
    select = driver.find_element(
        By.XPATH,
        '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select',
    )
    select.click()
    time.sleep(3)
    selectVal = driver.find_element(
        By.XPATH,
        f'//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[{selectorId}]',
    )
    selectVal.click()
    time.sleep(3)

    for i, word in enumerate(seed_phrase.split()):
        el = driver.find_element(By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]')
        el.send_keys(word, Keys.TAB, Keys.TAB)
        time.sleep(1)

    time.sleep(3)
    thirdButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'
    )
    thirdButton.click()
    time.sleep(3)

    firstPassword = driver.find_element(
        By.XPATH,
        '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input',
    )
    firstPassword.send_keys(PASSWORD)
    time.sleep(3)

    secondPassword = driver.find_element(
        By.XPATH,
        '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input',
    )
    secondPassword.send_keys(PASSWORD)
    time.sleep(3)

    secondCheckbox = driver.find_element(
        By.XPATH,
        '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input',
    )
    secondCheckbox.click()
    time.sleep(3)

    fourthButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'
    )
    fourthButton.click()
    time.sleep(3)

    fiveButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
    )
    fiveButton.click()
    time.sleep(3)

    sixButton = driver.find_element(
        By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
    )
    sixButton.click()
    time.sleep(3)
    sixButton.click()
    time.sleep(3)

    log("Stop chrome driver")
    driver.quit()

    log("Stop profile")
    response = requests.get(stop_profile(profile_id))
    result = json.loads(response.text)
    print(result)


def main():
    seed_phrases = get_seed_phrases(SEED_FILE)
    dolphin_profiles = get_dolphin_profiles()
    print(seed_phrases, len(seed_phrases))
    print(dolphin_profiles, len(dolphin_profiles))
    for i, profile in enumerate(dolphin_profiles):
        if i <= len(seed_phrases):
            metamask(profile["id"], seed_phrases[i])


if __name__ == "__main__":
    main()
