from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date,datetime
import uuid

def main():

    now = datetime.now()

    chrome_options=Options()
    
    chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    def jobsAnalyze(soup,company104Code):
        rows = soup.find_all('div', {'class': 'job-list-container'})
        for row in rows:
            data={"_id":str(uuid.uuid4()),"code":company104Code}
            # 工作名稱
            data["title"] = row.find('a', {'class': 'info-job__text'}).get_text()
            # 工作地區、經歷、學歷
            infoTags = row.find_all('span', {'class': 'info-tags__text'})
            data["area"] = infoTags[0].get_text()
            data["workExp"] = infoTags[1].get_text()
            data["education"] = infoTags[2].get_text()

            # 待遇
            infoOtherTagText = row.find('span', {'class': 'info-othertags__text'}).get_text()
            data["payInfo"] = infoOtherTagText

            # 最少應徵人數
            actionApplyRangeText = row.find('a', {'class': 'action-apply-range'}).get_text()
            data["applyRangeInfo"] = actionApplyRangeText

            data["date"]=now
            print(data)
        
    def get104(company104Code,page):
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(f'https://www.104.com.tw/company/{company104Code}?page={page}&pageSize=100')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        jobsAnalyze(soup,company104Code)

        if page==1:
            pageCount =  len(soup.find_all('label', {'class': 'form-control-outer--paging'})[0].find_all('option'))    
            if pageCount > 1 :
                for i in range(2,pageCount+1):
                    get104(company104Code,i)
        else:
            jobsAnalyze(soup,company104Code)

        browser.close()
        browser.quit()

    #ExampleUrl will be https://www.104.com.tw/company/a5h92m0
    get104("a5h92m0",1)

main()
