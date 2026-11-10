import pytest


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


    
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    user_input = driver.find_element(By.ID, "username")
    user_input.clear()
    user_input.send_keys("tomsmith")
    # скажите пожалуйста, каждый раз нужно делать очистку поля (так было в вебинаре)? или можно написать    
    # driver.find_element(By.ID, "username").send_keys("tomsmith")?


    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "You logged into a secure area!" in driver.find_element(By.ID, "flash").text


def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    user_input = driver.find_element(By.ID, "username")
    user_input.clear()
    user_input.send_keys("tomsmit")
    # скажите пожалуйста, тут вопрос по логину и паролю, если ввести неправильно только один из них, сообщения 
    # разные, invalid username or invalid pass, это 2 отдельных теста как я понимаю (3 в общем),
    # если проверять по сообщению как в первом, а не 2 как в условии
    # поэтому я сделала 2 с разными ассертами, подскажите, который из них НЕправильно? 

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("SuperSecretPassword")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    message = driver.find_element(By.ID, "flash")

    assert "error" in message.get_attribute("class")   