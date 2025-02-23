import requests
import csv
import bs4
import streamlit as st
from selenium import webdriver

def generate_links(url):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    REQUEST_HEADER ={
    'User-Agent' : USER_AGENT,
    'Accept-Language' : 'en-US, en; q=0.5',
    }

    def get_page_html(url):
        res = requests.get(url=url, headers=REQUEST_HEADER)
        return res.content

    def get_school_link(soup):
        school_list = soup.find('table', id="myTable")
        links = []
    
        school_row = school_list.find_all('tr')
        for row in school_row:
            cells = row.find_all('td')
            for cell in cells:
                link = cell.find('a')
           
            if link:
                href = link.get('href')
                if href:
                    links.append(href)
        return links

    def get_schools(url):
        school_links = []
        html = get_page_html(url=url)
        soup = bs4.BeautifulSoup(html,'lxml')
        return (get_school_link(soup))
    
    


  



    if __name__ == '__main__':
        school_links = []
        output_file = state+"_state.csv"
        school_links.append(get_schools(url))

   
 

        with open(output_file,'w', newline='') as output:
            writer = csv.writer(output)
        # writer.writerow("Links")
            for list in school_links:
                for link in list:
                    writer.writerow([link])
            
    



states_in_nigeria = [
    "Abia",
    "Adamawa",
  
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara"
]

def scrape(state):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    REQUEST_HEADER ={
    'User-Agent' : USER_AGENT,
    'Accept-Language' : 'en-US, en; q=0.5',
}
    def get_page_html(url):
        res = requests.get(url=url, headers=REQUEST_HEADER)
        return res.content

    def get_school_address(soup):
        main_school_address = soup.find('div', attrs={
        'class': 'property-title'   
        })
        school_add = main_school_address.find('a')
        address = school_add.text.strip()
        return address


    def get_school_name(soup):
        main_school_name = soup.find('div', attrs={
        'class': 'property-title'
    })
   
        school_n = main_school_name.find('h2')
        name = school_n.text.strip()
        return name



    def get_school_mail(url):
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html,'lxml')
        main_school_mail = soup.find_all('td')
    # print(main_school_mail)
        try:
            for td in main_school_mail:
                if "@" in td.text:
                    email_value = td.text.strip()
                    return email_value
        except:
            return "Not found"

   


    def get_school_info(url):
    
        school_info = {}
        st.write(f"Scrapping URL: {url}")
        html = get_page_html(url=url)
        soup = bs4.BeautifulSoup(html,'lxml')
        school_info['School_Name'] = get_school_name(soup)
        school_info['Email'] = get_school_mail(url)
        school_info['Address'] = get_school_address(soup)

        return(school_info)


    if __name__ == "__main__":
        school_data = []
        place = state
        with open(f'{place}_state.csv', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:

                url = "https://napps.com.ng/"+row[0]
                school_data.append(get_school_info(url))

        final_file = f'{state}.csv'
        with open(final_file,'w') as output:
            writer = csv.writer(output)
            writer.writerow(school_data[0].keys())
            for school in school_data:
                writer.writerow(school.values())
    return (final_file)

state = st.selectbox("Choose State",options=states_in_nigeria)
state = state.lower()


url = f'https://napps.com.ng/branches-details.php?ab_id=napps_{state}'
st.write(url)
links = st.button(f"Generate {state.capitalize()} school links ")
if links:
    generate_links(url)
    st.write(f"Now, we can Scrap {state.capitalize} data and save in a CSV file")

st.write(f"Choose the state")
place = st.selectbox("Choose State to scrape", options=states_in_nigeria)
place = place.lower()
scraper = st.button(f"Scrap {place.capitalize()}")
if scraper:
    final_file = scrape(place)
    st.success("Successfully Scraped")

    with open(final_file,"rb") as file:
        btn= st.download_button(
            label=f"Download {place} School info",
            data=file,
            file_name=final_file,
            mime ='text/csv'
        )


    
