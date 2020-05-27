import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def human_handle(info):
    print(info)
    input("Press Enter to continue...")


username = ""
passwd = ""

driver = webdriver.Firefox()
driver.get("http://infotech.51taoshi.com")


#login

driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/span/a[1]").click()
driver.find_element_by_id("login_username").send_keys(username)
driver.find_element_by_id("login_password").send_keys(passwd)
driver.find_element_by_xpath("/html/body/div[5]/div/div/form/div/a").click()

#signup

time.sleep(2)
signup_buttons = driver.find_elements_by_xpath('//button[@class="btn btn-green btn-sm mr5"]')
print(len(signup_buttons))
for button in signup_buttons:
    time.sleep(2.5)
    try:button.click()
    except:pass

#dohomework

answertxt = ""
with open("answer", 'r', encoding="utf-8") as f:
    answertxt = f.read()
    

choicedic = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4
}

cnt = 0
while True:
    try:
        button = driver.find_element_by_xpath('//button[@class="btn btn-primary btn-sm"]')

        cnt += 1
        print("test {}".format(cnt))
        try:
            button.click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[@class="btn btn-xs btn-green"]').click()

            question_num = len(driver.find_elements_by_class_name("timu"))
            print("total {} questions".format(question_num))

            for i in range(1, question_num + 1):
                print("problem No.{}".format(i))

                #get question
                ptr = "//ul[@class='test-list']/ul[{}]/li/div/div[1]".format(i)
                question = driver.find_element_by_xpath(ptr).text
                print(question)
                question = question.split(')')[1].split('(')[0].strip()
                if len(question.splitlines()) > 1:
                    question = question.splitlines()[0]
                
                #find answer
                flag = False
                pos = answertxt.find(question)
                if pos != -1:
                    answer = answertxt[answertxt.find("[answer:]", pos) + 9]
                    print(answer)
                else:
                    pos = answertxt.find(question[0:5])
                    
                    if pos == -1:
                        human_handle("answer not found.  Please choose answer in the browser manually.")
                        answer = "none"
                    else:
                        human_handle("this is likely the question. But Im not sure. Please press enter if it IS the question\n" + 
                        answertxt[pos:pos + 50] + "\nthis is likely the question. But Im not sure. Please press enter if it IS the question")
                        answer = answertxt[answertxt.find("[answer:]", pos) + 9]
                        flag = True
                        print(answer)

                

                #fill answer
                if choicedic.get(answer) != None: #choice
                    ptr = "//ul[@class='test-list']/ul[{}]/li/div/div[2]/ul/li[{}]/label/input".format(i, choicedic[answer])
                    driver.find_element_by_xpath(ptr).click()
                elif not flag:#free response
                    ptr = "//ul[@class='test-list']/ul[{}]/li/div/div[2]/textarea".format(i)
                    #driver.find_element_by_xpath(ptr).send_keys(' ')
                    input("这网站只能输入汉字.所以这里没办法自动化.请手动粘贴一些中文内容然后按回车继续")



            #submit

            submit_button = driver.find_element_by_xpath("//*[@id='postExamAnswer']")
            submit_button.click()
            time.sleep(0.5)
            try:
                if driver.find_element_by_xpath("/html/body/div[8]/div[2]").text == "您确定要提交试卷吗？":
                    driver.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]").click()

            except: human_handle("error occur when submit. Please fix manually.")
            time.sleep(1)
                    

            driver.get("http://infotech.51taoshi.com/hw/stu/myHomework.do")
            time.sleep(2)
        except:pass
    except:break
#driver.close()