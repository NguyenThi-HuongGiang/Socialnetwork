from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass


class FacebookGroupScraper:
    def __init__(self):
        print('------------------------------')
        print("Facebook Group Scraper Members")
        print('------------------------------')

        self.get_config()
        self.setup_driver()
    
    def get_config(self):
        try:
            # Nhập thông tin đăng nhập
            print('----------Nhập thông tin đăng nhập---------------')
            self.email = input("Email Address: ").strip()
            self.password = getpass.getpass("Password: ")

            # ID group
            print('----------Nhập ID group---------------')
            self.group_id = input("Group ID: ").strip()

            # Số lần scroll
            print('----------Nhập số lần scroll---------------')
            self.scroll_count = int(input("So lan scroll (mac dinh 5)") or "5")

        except Exception as e:
            print(f"Loi cau hinh: {e}")
            pass
            
    def setup_driver(self):
        try:
            
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            print("---------------Error------------------:", str(e))
    
    def login(self):
        try:
            self.driver.get("https://www.facebook.com/login")
            time.sleep(5)  # Chờ tải trang

            #nhap email
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(self.email)
            
            #nhap password
            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)
            
            #click dang nhap
            login_button = self.driver.find_element(By.ID, "Login")
            login_button.click()
            time.sleep(10)
            print("Dang nhap thanh cong")
            return True
        
        except Exception as e:
            print("--------------Error đăng nhập---------------:", str(e))
            return False
    
    def get_group_members(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")

            time.sleep(5) 

            members = set()  # Dung set de cac member khong bi trung lap
            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(3)  
                print(f'scroll la thu {i+1}/{self.scroll_count}')

                # thu thap thong tin sau moi lan scroll
                user_element = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")

                # print len user
                for user_element in user_element:
                    try:
                        href = user_element.get_attribute('href')
                        if '/user/' in href:
                            user_id = href.split('/user/')[1].strip('/')
                            name = user_element.text
                            members.add(user_id, name)
                            print(user_id, '-', name)
                    except Exception as e:
                        continue
                


        except Exception as e:
            print("--------------Error lấy thông tin thành viên---------------:", str(e))
            return None

              
def main():
    scraper = None

    try:
        scraper = FacebookGroupScraper()
        
        if scraper.login():
            scraper.get_group_members()
            time.sleep(10)
        time.sleep(10)
    except Exception :
        pass

if __name__ == "__main__":
    main()