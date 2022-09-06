################################################################################################################
"""
Author : Pratiksha
File name : scraper.py
Purpose : John's lewis products data collection pipeline
 
"""
################################################################################################################
"""
Importing Libraries
"""
################################################################################################################
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from aws_boto import AWSBoto
from time import sleep
from logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import uuid
import json
import os
import urllib.request
import pandas as pd

class Scraper():
    """
            This class initialises the webscraper, that collect the data and save it locally. 
            It will initialises the variable which can be accessible anywhere in code.
            and call the method to create folder.

    """
    def __init__(self): 
        print("Start scraping the website.....")
        driver_path ="/Users/pratiksha/Documents/scratch/Datacollection_pipeline_johnlewis/src/geckodriver"
        #('/Users/pratiksha/Documents/scratch/Datacollection_pipeline_johnlewis/src/geckodriver')
        self.driver_path = driver_path
        self.search_name = "mobile"
        self.folder_name = "raw_data"
        self.image_folder_name = "images"
        #self.driver = Service("/Users/pratiksha/Documents/scratch/Datacollection_pipeline_johnlewis/src/geckodriver")
        #self.user_agent= "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"
        firefox_option = Options()
        #firefox_option.add_argument("--headless") 
        self.driver = Firefox(options=firefox_option)
        #self.driver = Firefox()
        self._create_metadata_folders(self.folder_name)
        self.create_folders(self.image_folder_name)
        self.aws = AWSBoto()
       
        
    @staticmethod
    def _create_metadata_folders(directory_name):
        current_directory = os.getcwd() 
        saving_data_dir = os.path.join(current_directory, directory_name)
        if os.path.exists(saving_data_dir):
            print(f"msg : Directory path is already exist : {saving_data_dir}")
        else:
            os.mkdir(saving_data_dir)
            print(f"msg : OS path created : {saving_data_dir}")

    def create_folders(self,folder_name_save):
        current_directory = os.getcwd() 
        check_data_dir = os.path.join(current_directory,self.folder_name)
        if os.path.exists(check_data_dir):
            folder_name = check_data_dir+"/"+folder_name_save
            self._create_metadata_folders(folder_name)
        else:
            print(f"msg : OS path is not exists : {check_data_dir}")

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
        sleep(2)
        self.__search_on_searchbar()
        sleep(3)

        
    def __accept_cookies(self):
        """
            This method is used to accept the cookies
        """
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
            sleep(3)
            self.get_product()      
        except AttributeError:
            pass
        except Exception as e:
            Logger.logrecord(str(e))
            print(f"msg : Error while searching the product {str(e)}")

    def get_product(self):
        """
            This method is to get the product info amd sava data into json format
        """
        self.scroll_page_down()
        sleep(2)
        product_info_container = []
        product_info_container = self.get_product_information()
        total_record_downloaded = self.save_json_data(product_info_container)
        print(f"Total {total_record_downloaded} record/s downloaded !!")
       
    def scroll_page_down(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_product_information(self) -> list:
        """
            This method will collect all the search result into one container and apply loop to get the product details.
            We used UUid which is universal id to identify the record.
        """

        mobile_categories_container =[]
        product_list= []
        try:
            mobile_categories_container = self.__get_elements_list("//div[@class='ProductGrid_product-grid__product__oD7Jq']") 
            if len(mobile_categories_container) != 0:
                for mobile in mobile_categories_container:
                    u_id = uuid.uuid4()
                    u_unique_id = str(u_id)
                    mobile_product_href = mobile.find_element(by=By.XPATH, value=".//a[@class='image_imageLink__1Znsz product-card_c-product-card__image__bO3kW product__image']").get_attribute("href")
                    unique_productid = mobile_product_href.split("/")
                    product_id = unique_productid[-1]
                    mobile_info_title = mobile.find_element(by=By.XPATH, value=".//span[@class='title_title__desc__ZCdyp title_title__desc--three-lines__VHz1t title_title__desc--branded__8SluU']").text
                    mobile_info_price = mobile.find_element(by=By.XPATH, value=".//span[@class='price_price__now__3B4yM']").text
                    mobile_info_price = mobile_info_price.replace('£', '')
                    mobile_info_src = mobile.find_element(by=By.XPATH, value=".//img[@class='image_image__jhaxk']").get_attribute("src")    

                    mobile_container = {
                        'uuid':u_unique_id,
                        'product_id':product_id,
                        'product_title':mobile_info_title,
                        'product_price':mobile_info_price,
                        'product_src':mobile_info_src
                    }
                    product_list.append(mobile_container)
            else:
                print(f"msg : Product container is empty : {len(mobile_categories_container)} record/s")        
        except AttributeError:
            pass
        except Exception as e:
            print(f"msg : Error found in get_product_information() method : {str(e)}")
            Logger.logrecord(str(e))        
        return product_list

    def save_json_data(self,product_container_data : list)-> int:
        """
            This method is used to save the json data. And it gives the count of product

            parameter
            ---------
                product_container_data : list
                    This parameter is a list type and it contains all information of each product
            Returns
            --------
                total_count_record : int
                    This will return count of total record
        """
        total_count_record = len(product_container_data)
        print(f"Total products count : {total_count_record}")
        #df_data = pd.DataFrame(product_container_data)
        self.aws.save_data_RDS(product_container_data)
        if len(product_container_data) != 0:
            for item in range(len(product_container_data)):
                product_id = product_container_data[item]['product_id'] 
                product_image_src = product_container_data[item]['product_src']
                current_directory = os.getcwd() 
                saving_data_path = os.path.join(current_directory,self.folder_name,product_id)
                self._create_metadata_folders(saving_data_path)
                self.write_data_to_json_file(saving_data_path,product_container_data[item])
                saving_image_path = os.path.join(current_directory,self.folder_name,self.image_folder_name)
                self.download_images(saving_image_path,product_image_src,product_id)
        else:
            print(f"msg : Product container is empty : {len(product_container_data)}")

        return total_count_record

  

        
    def write_data_to_json_file(self,valid_path : str,valid_data : dict):
        """
            This method is used to save the data into data.json file 

            parameters
            ---------
            valid_path : str
                valid_path parameter is a string type that contain the path to save the data.
            valid_data : dict
                valid_data parameter is a dictionary type that contain the product informations.

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


    def download_images(self,images_folder_path : str,product_image_link: str,product_id : str):
        """
            This method is used to download the images of products.

            parameters
            ----------
            images_folder_path : str
                images_folder_path is a string type and contain the folder path
            product_image_link : str
                product_image_link is a string type and contain the product image link
            product_id : str
                product_id is a string type and contain the product id information
            
        """
        image_path = images_folder_path +"/"+ product_id + '.jpg'
        try:
            urllib.request.urlretrieve(product_image_link, image_path)
            print("msg : Image Downloaded")
            s3_url = self.aws.upload_object_s3(image_path, product_id)
            return s3_url

        except Exception as e:
            Logger.logrecord(str(e))
            print(f"msg : Error while downloading the images {str(e)}")

    def __get_each_element(self, places_locate) -> object:
        elements = self.driver.find_element(by=By.XPATH, value=places_locate) 
        return elements 

    def __get_elements_list(self, places_locate) -> list:
        elements = self.driver.find_elements(by=By.XPATH, value=places_locate)
        return elements

if __name__ == "__main__":
    scraper = Scraper()
    scraper.load_page('https://www.johnlewis.com')
    
