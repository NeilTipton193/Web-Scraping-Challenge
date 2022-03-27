#Load Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url ='https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    #Save latest news title and teaser to variables
    title = soup.find("div", class_="content_title").text
    teaser = soup.find('div',class_="article_teaser_body").text

    #Setup browser and Beautiful Soup for https://spaceimages-mars.com
    pic_url = 'https://spaceimages-mars.com'
    browser.visit(pic_url)
    time.sleep(5)
    pic_html = browser.html
    pic_soup = BeautifulSoup(pic_html,'html.parser')



    #use .find() to scrape source 
    url_end = pic_soup.find("img", class_="headerimage fade-in")['src']
    full_url = pic_url + '/' +url_end

    #Use Pandas to scrape https://galaxyfacts-mars.com
    table_url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(table_url)
    df = table[0]
    df.columns = df.iloc[0]
    df = df[1:]
    #Convert to html table string
    result = df.to_html(index=False)
    result = result.replace('\n','')

    #Set up for scrape of https://marshemispheres.com/
    mars_url = 'https://marshemispheres.com/'

    browser.visit(mars_url)
    time.sleep(5)
    # Create BeautifulSoup object; parse with 'html.parser'
    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')

    #Create list to hold dictionaries of images and titles
    mars_list = []
    mars_item = mars_soup.find_all('div', class_='item')

    #For loop to extract link and title
    for i in range(0,4):
        try:
            mars_img = mars_url+mars_item[i].img['src']
            mars_title =mars_item[i].img['alt']
            mars_dict = {} 
            mars_dict = {'title':mars_title,'img_url': mars_img}
            # mars_dict['title']=mars_title 
            # mars_dict['img_url']= mars_img
            mars_list.append(mars_dict)
        except Exception as e:
            print(e)

    #Consolidate all scraped data into one dictionary
    consolidated_dict = {'News title': title,
                'News teaser': teaser,
                'Featured image': full_url,
                'Mars-Earth comparison': result, 
                'Mars_Hemispheres': mars_list}
    browser.quit()
    return consolidated_dict