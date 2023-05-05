import selenium.webdriver.support.wait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import date
from bs4 import BeautifulSoup as bs
from openpyxl import load_workbook
import openpyxl
import requests
import time
import json
import re
import random
import lxml
import glob
import shutil
from config import username, password, keys, vpnl, vpnp
from webdriver_manager.chrome import ChromeDriverManager

username = username
password = password
keys = keys
vpnlogin = random.choice(vpnl)
vpnpass = vpnp[0]
st = []

def r():
    x = random.randint(4,8)
    return x


def usevpn(driver):
    global st
    driver.get("https://www.tunnelbear.com/account/login") # зашли на сайт впн
    if driver.current_url == 'https://www.tunnelbear.com/account/overview':
        pass
    else:
        try:
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/section/div/div/div/div/button').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(f'{vpnlogin}')  # логин
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(f'{vpnpass}')  # пасс
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()  # залогинились
            time.sleep(6)
        except Exception as e:
            pass

    try:
        driver.get("chrome-extension://omdakjcmkglenbhjadbccaookpfjihpa/popup.html#/countries")  #in extension
        time.sleep(2)
        soup = bs(driver.page_source, "html.parser")
        cparse = soup.findAll('div', class_="item-text")
        vpnc = ['Germany','Austria'] #из каких стран выбирать
        cnames = []
        for c in cparse:
            names = c.text
            cnames.append(names)
        ind = []

        for i in vpnc:
            try:
                count = (cnames.index(i)+1)
                ind.append(count)
            except Exception as e:
                print(f"{i} не доступна к выбору")
        n = random.choice(ind)
        st.append(cnames[n-1])
        driver.find_element(By.XPATH, f'//*[@id="menu-container"]/ul/li[{n}]/div').click()  # Выбрали страну
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, f'//*[@id="menu-container"]/div/button').click()  # done
            time.sleep(2)
        except Exception as e:
            pass
        try:
            driver.find_element(By.XPATH, '//*[@id="on-off-toggle-container"]').click() # on
            time.sleep(8)
            return st
        except Exception as e:
            pass
    except Exception as e:
        print("Не удалось запустить впн")
        time.sleep(10)
        return usevpn(driver)


def weekly(driver):
    driver.find_element(By.XPATH, '//*[@id="root"]/div/nav/a[4]').click()  #клацнули на виклик
    time.sleep(2)
    daily_page = driver.page_source
    daily = bs(daily_page, 'html.parser') # парсим страницу виклика
    bad_days = [2,4,6,7]
    daycount = int(daily.findAll('div', {"class": re.compile("Tile_notCollected")})[0].text)# нашли не выполненный
    if daycount in bad_days:
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click() # закрыли окно
        time.sleep(r())
        pass
    else:
        try:
            driver.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div/div[2]/div[1]/div[1]/div[{daycount}]/div/div').click()  # нажали на награду
            time.sleep(2)

            claim_paige = driver.page_source
            claim = bs(claim_paige, 'html.parser')  # парсим страницу виклика
            rev1 = claim.contents[0].contents[1].contents[11].contents[0].contents[1].contents[0].contents[4].contents[1].attrs['class'][0]
            rev2 = claim.contents[0].contents[1].contents[11].contents[0].contents[1].contents[0].contents[4].contents[1].attrs['class'][1]
            rev3 = claim.contents[0].contents[1].contents[11].contents[0].contents[1].contents[0].contents[4].contents[1].attrs['class'][2]
            driver.find_element(By.CSS_SELECTOR, f'button[class="{rev1} {rev2} {rev3}"]').click()  # забрать награду
            time.sleep(r())
            # try:
            #     captcha = driver.find_element(By.CSS_SELECTOR, "div[class='recaptcha-checkbox-border']")  # нашли элемент с кодом
            #     driver.execute_script("arguments[0].click();", captcha); # нажали на капчу
            #     time.sleep(3)
            # except Exception as e:
            #     pass
            driver.find_element(By.XPATH, '//*[@id="body"]/div[7]/div/div[2]/button').click()  # назад
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click()  # назад
            time.sleep(r())
        except Exception as e:
            pass



def main():
    k = len(username)
    book = openpyxl.Workbook()
    sheet = book.active
    sheet['A1'] = 'Account name'
    sheet['B1'] = 'Coins'
    sheet['C1'] = 'Diamonds'
    sheet['D1'] = 'Steam key'
    row = 2
    vp = int(input("Введите 1 если запустить с впн, 2 если без: "))
    i = 0 # начало списка с логинами
    for i in range(0,k):
        try:
            start_time = time.time()
            login = username[i]
            passw = password[0]
            options = Options()
            options.add_argument("--disable-infobars")
            options.add_argument('--disable-notifications')
            options.add_argument("--mute-audio")
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--save-screenshot")
            options.add_extension("TunnelBear-VPN.crx")
            driver = webdriver.Chrome(options=options)
            # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.maximize_window()

            if vp == 1:
                usevpn(driver) # запуск впн
            else:
                pass

            try:
                country = st[0]
            except Exception as e:
                pass
                
            time.sleep(r())
            driver.get("https://www.lootboy.de/offers")
            time.sleep(r())
            driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()  # принимаем кукисы
            time.sleep(r())
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click() #закрыли вплывающее окно дейлbка
            time.sleep(4)
            driver.find_element(By.XPATH, '//*[@id="root"]/div/nav/a[5]').click() #открыли меню
            time.sleep(4)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/button[2]').click() #кнопка логин
            time.sleep(4)
            driver.find_element(By.XPATH, '//*[@id="body"]/div[7]/div/div[2]/div[1]/div[2]/button').click()  # подтверждение
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/input').send_keys(login)  # логин
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/input').send_keys(passw)  # пароль
            time.sleep(r())
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/button').click()  # отправить
            time.sleep(r())



            id_page = driver.page_source
            id = bs(id_page, 'html.parser')
            time.sleep(r())
            quest = id.findAll('div', {"class": re.compile("LootboyContainer_lootboyContainer")})
            for q in quest:
                questid = str(q.contents[2].attrs['id'])
            time.sleep(r())

            driver.find_element(By.XPATH, f'//*[@id="{questid}"]/div/div/div[1]/div/div[2]/a[4]/div/div/div[1]/div').click()
            time.sleep(r())
            quest_page = driver.page_source
            que = bs(quest_page, 'html.parser')
            gems = que.findAll('div', {"class": re.compile("QuestTile_container")})
            gems_status = []
            try:
                gems_status.append(gems[0].contents[2].attrs['class'][0][0:19])
            except Exception as e:
                pass
            time.sleep(r())


            if len(gems_status) > 0: # проверка выполнен ли дейлик
                pass
            else:
                try:
                    wait = WebDriverWait(driver, 20)
                    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/section/ul/li[1]/div/a')))) #кнопка квеста
                    time.sleep(r())
                    new_window = driver.window_handles[0]
                    driver.switch_to.window(new_window) #переключились на главное окно
                    time.sleep(r())
                except Exception as e:
                    print(e)
                    pass
            
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click() #закрыли окно с дейликом
            time.sleep(3)

            # weekly(driver) # отправка на виклик

            if len(keys) > 0: # проверка списка с кодами, если ключей нет, пропускаем
                time.sleep(4)
                driver.find_element(By.XPATH, '//*[@id="root"]/div/nav/a[5]').click()  # открыли меню
                time.sleep(r())
                driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/button[2]').click() #ввод кодов
                time.sleep(r())
                for key in keys:
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/div/input').send_keys(f"{key}") #вставляем код
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[3]/button').click() #отправляем код
                    time.sleep(2)

                    try:                               
                        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]').click() #пробуем открыть лут пак

                        time.sleep(4)
                        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/button').click() # перешли в инвентарь
                        time.sleep(r())                
                        driver.find_element(By.XPATH, '//*[@id="root"]/div/nav/a[5]').click()  # открыли меню
                        time.sleep(r())                
                        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/button[2]').click() # ввод кодов
                        time.sleep(r())
                    except Exception as e:
                        time.sleep(0.5)
                        pass

                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click()  # кнопка назад
                    time.sleep(3)
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div[1]/button[2]').click()  # ввод кодов
                    time.sleep(3)

                try:
                    time.sleep(0.5)
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click() #кнопка назад
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/button').click() #кнопка назад
                    time.sleep(r())
                except Exception as e:
                    pass

            else:
                time.sleep(10) #спим
                pass

            
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/a[4]').click() # перешли в инвентарь
            time.sleep(r())
            source_page = driver.page_source #парсим страницу
            soup = bs(source_page, 'html.parser')
            currency = soup.findAll('div', {"class": re.compile("Balances_balances")})  # ищем сколько на акке монет и даймондов
            for cur in currency:
                coins = currency[0].contents[0].contents[1]
                diamond = int(currency[0].contents[1].contents[1])
                sticks = currency[0].contents[2].contents[1]

            time.sleep(0.5)
            dateе = date.today()
            timee = time.strftime("%H")
            steamcode = []
            if diamond >= 125: #проверяем кол-во диамантов на акке для покупки пака, если меньше пропускаем
                try:
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/a[2]').click()  # нажали Quest
                    time.sleep(r())

                    try:
                        if country == "Austria" or "Germany":
                            pcounter = 98
                    except Exception as e:
                        pcounter = 33
                        pass

                    driver.find_element(By.XPATH, f'//*[@id="{questid}"]/div/div/div[{pcounter}]/div/div/div/div[1]/a/div/div[1]').click()  # нажали loot
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div/div[4]/div[2]/button').click()  # нажали Get(купить)
                    time.sleep(r())

                    source_page1 = driver.page_source  # ищем кнопку подтверждения
                    soup1 = bs(source_page1, 'html.parser')
                    confirm = soup1.findAll('div', {"class": re.compile("PopupPlain_popupContent")})
                    con1 = confirm[0].contents[3].attrs['class'][0]
                    con2 = confirm[0].contents[3].attrs['class'][1]
                    con3 = confirm[0].contents[3].attrs['class'][2]
                    time.sleep(0.5)

                    driver.find_element(By.CSS_SELECTOR, f'button[class="{con1} {con2} {con3}"]').click() # подтвердили покупку
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]').click() # открыли пак
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/button').click() # перешли в инвентарь
                    time.sleep(r())

                    source_page2 = driver.page_source  # ищем карту с кодом
                    soup2 = bs(source_page2, 'html.parser')
                    gamepack = soup2.findAll('div', {"class": re.compile("CardWrapper_cardItem")})
                    card_id = gamepack[00].contents[0].attrs['class'][0]

                    driver.find_element(By.CSS_SELECTOR, f'.{card_id}.frameGold').click() # нашли карту
                    time.sleep(r())
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div/div').click()  # нажали открыть
                    time.sleep(r())
                    element = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/p') # нашли элемент с кодом
                    driver.execute_script("arguments[0].scrollIntoView(true);", element); # прокрутили вниз
                    time.sleep(r())
                    driver.save_screenshot(f"{login}_steamkey_{dateе}_{timee}.png")  # сделали скриншот
                    steamkey = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/p').text # получили ключ в переменную
                    steamcode.append(steamkey) # занесли ключ в список
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[1]/div[1]/button[1]').click() # закрыли окно с паком
                    time.sleep(2)
                    diamond = diamond-125
                except Exception as e:
                    pass
            else:
                pass


            time.sleep(0.5)
            # driver.save_screenshot(f"{login}_{dateе}_{timee}.png") #сделали скриншот
            if len(steamcode) == 0:
                sheet[row][0].value = (f"{login}")
                sheet[row][1].value = (f"{coins}")
                sheet[row][2].value = (f"{diamond}")
            else:
                k = steamcode[0]
                sheet[row][0].value = (f"{login}")
                sheet[row][1].value = (f"{coins}")
                sheet[row][2].value = (f"{diamond}")
                sheet[row][3].value = (f"{k}")

            row += 1
            book.save(f"{dateе}.xlsx")  # сохраняем в фаил
            i = i+1 #увеличили позицию логина в списке
            print("--- Ушло времени на проверку %s секунд---" % (time.time() - start_time))
            time.sleep(r())
            driver.quit() #закрыли окно
            try:
                for f in glob.glob(R"C:\Program Files (x86)\scopeD_dir*"):
                    shutil.rmtree(f)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            pass
    book.close()


main()