
from requests import options
from selenium import webdriver
from time import sleep
from logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import uuid
import json
import os
import urllib.request

class Scraper():
    """
            This class initialises the webscraper, that collect the data and save it locally. 
            It will initialises the variable which can be accessible anywhere in code.
            and call the method to create folder.

    """
    def __init__(self): 
        driver_path ="/Users/pratiksha/Documents/scratch/Datacollection_pipeline_johnlewis/src/chromedriver"
        self.driver_path = driver_path
        self.search_name = "mobile"
        self.folder_name = "raw_data"
        self.service = Service(self.driver_path)
        options = Options()
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self._create_metadata_folders(self.folder_name)

    @staticmethod
    def _create_metadata_folders(directory_name):
        current_directory = os.getcwd() 
        saving_data_dir = os.path.join(current_directory, directory_name)
        if os.path.exists(saving_data_dir):
            os.chdir(saving_data_dir)
        else:
            os.mkdir(directory_name)
            os.chdir(saving_data_dir)

    def load_page(self, url):
        """
            This method load the website "johnlewis" and call 2 different method from the very first page.
            acceptcookies method will accept the cookis and allow to search the content using searchbar method.

          Parameters
          ----------
          url : str

        """
        self.driver.get(url) 
        sleep(2)  
        self.__accept_cookies()
        self.__search_on_searchbar()
        sleep(2)

    def __accept_cookies(self):
        try:
            accept_cookies_by_clicking = self.__get_each_element("//*[@data-test='allow-all']") 
            accept_cookies_by_clicking.click()
        except AttributeError:
            pass
        except Exception as e:
            Logger.logrecord(str(e))

    def __search_on_searchbar(self):
        try:
            search_name = self.__get_each_element("//input[@name='search-term']")
            search_name.send_keys(self.search_name)  
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()  
        except AttributeError:
            pass
        except Exception as e:
            Logger.logrecord(str(e))   
   
    def get_product_information(self):
        """
            This method will collect all the search result into one container and apply loop to get the product details.
            We used UUid which is universal id to identify the record.

        """
        mobile_categories_container =[]
        product_list= []
        mobile_categories_container = self.__get_elements_list("//div[@class='ProductGrid_product-grid__product__oD7Jq']")    
        for mobile in mobile_categories_container:
            u_id = uuid.uuid4()
            u_unique_id = str(u_id)
            mobile_product_href = mobile.find_element(by=By.XPATH, value=".//a[@class='image_imageLink__1Znsz product-card_c-product-card__image__bO3kW product__image']").get_attribute("href")
            unique_productid = mobile_product_href.split("/")
            product_id = unique_productid[-1]
            mobile_info_title = mobile.find_element(by=By.XPATH, value=".//span[@class='title_title__desc__ZCdyp title_title__desc--four-lines__7hRtk']").text
            mobile_info_price = mobile.find_element(by=By.XPATH, value=".//span[@class='price_price__now__3B4yM']").text
            mobile_info_src = mobile.find_element(by=By.XPATH, value=".//img[@class='image_image__jhaxk']").get_attribute("src")     
            mobile_container = {
                'unique_id':u_unique_id,
                'product_id':product_id,
                'title':mobile_info_title,
                'price':mobile_info_price,
                'src':mobile_info_src
            }
            product_list.append(mobile_container)
        return product_list

    def varify_the_folder_path(self, directory_name):
        if os.path.exists(directory_name):
            print(f"Directory path is already exist : {directory_name}")
        else:
            os.mkdir(directory_name)

    def write_data_to_json_file(self,valid_path,valid_data):
        """
            This method will write the product data into data.json file 
        """
        self.data_file_name = "data"+".json"
        create_file_saving_path  = valid_path +"/"+ self.data_file_name
        try:
            with open(create_file_saving_path, 'w') as fo:
                json.dump(valid_data, fo)
                print(f"msg: Data dumped !!")     
        except IOError as e:
            Logger.logrecord(str(e))
            print(f"msg : Error while dumping data on {create_file_saving_path} file")

    def folderimage(self):
        self.folder_images = "images"
        current_directory = os.getcwd()
        saving_data_dir = os.path.join(current_directory, self.folder_images)
        self.varify_the_folder_path(saving_data_dir)
        return saving_data_dir

    def download_images(self,images_folder_path,product_image_link,product_id):
        """
            This method download the images and save it locally in raw_data/images folder
        """
        image_path = images_folder_path +"/"+ product_id + '.jpg'
        urllib.request.urlretrieve(product_image_link, image_path)

    def __get_each_element(self, places_locate) -> object:
        elements = self.driver.find_element(by=By.XPATH, value=places_locate) 
        return elements 

    def __get_elements_list(self, places_locate) -> list:
        elements = self.driver.find_elements(by=By.XPATH, value=places_locate)
        return elements  
    
if __name__ == "__main__":
    scraper = Scraper()
    scraper.load_page('https://www.johnlewis.com')
    images_folder = scraper.folderimage()
    product_info = scraper.get_product_information()
    
    for item in range(len(product_info)):
        product_id = product_info[item]['product_id'] 
        product_image_src = product_info[item]['src']
        current_directory = os.getcwd() 
        saving_data_dir = os.path.join(current_directory, product_id)
        scraper.varify_the_folder_path(saving_data_dir)
        scraper.write_data_to_json_file(saving_data_dir,product_info[item])
        scraper.download_images(images_folder,product_image_src,product_id)
        
       
       


        
