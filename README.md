# Datacollection_pipeline_johnlewis
This data collection pipeline project mainly focus on collecting/scraping data of https://www.johnlewis.com website. 
Using selenium module/library of python. 

All the actions and steps are taken to implement this project from scraping the website to uploading the data on aws cloud services,that all mentioned on this README.md file.

Technologies that are used in this project : Python and its modules (boto3, math, os, selenium, urllib, uuid, json, unittest, patch, MagicMock).

From now onwards, the file describe each and every milestone of this project with detail descriptions.
## Milestone 1 - Decide the website that I am passionate about
I chose https://www.johnlewis.com website to satisfy the requirement of my first milestone. And of course, this website contains various type of data.

## Milestone 2 - Prototype finding the indivisual page for each entry
In this milestone I explored the python OOPS concept and tried to implement project in the same. To scrape the data it requires selenium library and specific browser in my case, I used chrome. and using selenium I imported the chromedriver module. To download the chromedriver find the below link.
https://chromedriver.chromium.org/downloads

once the installation is done, the next task is to navigate to the website, by passing the cookies and automatic search content "mobile" using selenium scraper code.

## Milestone 3 - Retrieve data from details page
I personally feel that I developed my programming skills during this module. 
Once the chrome automatic search the term "mobile", it gives bunch of mobile phones result. There are 48 records of mobile on the site which are in stock and it displyed accordingly. My job is to get the detail of each mobile such as mobile name, mobile price, mobile image link, mobile id number, UUID which is universal unique key generated for each record. And this task can be done using for loop over div class of product(mobile result) container.And once it is done I created a dictionary of each mobile phone details and append it to the single list. Now, that list contains all the informations of all the mobile phones. Further, I iterate over that list and save that each dictionary data into json file under raw_data/productID folders. And in the same iteration extract the link of each mobile phone and download that image and dumped it into raw_data/images folder.

## Milestone 4 - Documentation and testing
This milestone is very crucial to implement. This section gives the depth knowladge of Docsting in python. How to create a comment in each method what are the formats of Docstring all are mentioned in this section. Testing the public method of this project using unittest in python is something I explored and it gives ac brief idea that developer should use it for unittesting before releasing it into testing environment.

These are Docstring method: In this project I used Numpydoc format.
- [Google](https://google.github.io/styleguide/pyguide.html)
- [Sphinx or reStructuredText](http://sphinx-doc.org/markup/desc.html)
- [Numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Epytext](https://epytext.readthedocs.io/en/latest/format.html)




