import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

browser = webdriver.Chrome('chromedriver.exe') # Caminho para o Chromedriver

def login():
    browser.get('https://www.linkedin.com/login/pt')

    file = open('dados.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]

    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)

    elementID.submit()

def search_terms():
    login()
    pesquisa = 'diretor de producao' # Termo para pesquisa (TROCAR AQUI)
    pesquisa = pesquisa.replace(' ', '%20')
    fullLink = 'https://www.linkedin.com/search/results/people/?keywords='+pesquisa+'&origin=SWITCH_SEARCH_VERTICAL'
    browser.get(fullLink)
    connect()
    fullLink = fullLink+'&page=2'
    for i in range(3,11):
        time.sleep(1)
        browser.get(fullLink)
        time.sleep(2)
        connect()
        fullLink = fullLink[:-1]+str(i)
    
def getNewProfileIDs(soup):
    profilesID = []
    all_links = soup.find_all('a', {'class': 'search-result__result-link ember-view'})
    for link in all_links:
        userID = link.get('href')
        if userID not in profilesID:
            profilesID.append(userID)
    return profilesID

def connect():
    visitedProfiles = open('visitedUsers.txt').read().split('\n')
    profilesQueued = getNewProfileIDs(BeautifulSoup(browser.page_source, features="lxml"))
    time.sleep(1)
    for profile in profilesQueued:
        if profile not in visitedProfiles:
            try:
                fullLink = 'https://www.linkedin.com'+profile
                browser.get(fullLink)
                time.sleep(1)

                browser.find_element_by_class_name('pv-s-profile-actions').click()
                time.sleep(1)
                browser.find_element_by_class_name('ml1').click()

                with open('visitedUsers.txt', 'a') as visitedUsersFile:
                    visitedUsersFile.write(str(profile)+'\n')
                visitedUsersFile.close()
                time.sleep(2)
            except:
                print('Error')
    visitedProfiles = update_visited()
    time.sleep(1)

def update_visited():
    global visitedProfiles
    visitedProfiles = open('visitedUsers.txt').read().split('\n')


update_visited()
search_terms()
