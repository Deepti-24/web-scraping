#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
import re
import os
os.chdir("F:\WebScraping")


# In[2]:


def select_page(page, subject):
    containers = page.select(".bix-tbl-container")
    questions=[]
    for container in containers:
        quiz = {}
        question = container.find(class_="bix-td-qtxt").get_text(" ", strip=True)
        quiz['question'] = question
        options = {}
        raw_options = container.find(class_="bix-tbl-options").find_all("tr")
        for op in raw_options:
            op_no = op.find(id=re.compile("^tdOptionNo.*")).get_text(" ", strip=True)[0]
            op_txt = op.find(id=re.compile("^tdOptionDt.*")).get_text(" ", strip=True)
            options[op_no] = op_txt
        quiz['options'] = options
        answer = container.find(class_="jq-hdnakqb mx-bold").get_text()
        quiz['answer'] = answer
        quiz['topic'] = subject
        questions.append(quiz)
    return questions


# In[3]:


main_prefix="https://www.indiabix.com/computer-science/"
prefix = "https://www.indiabix.com"
topics = ["object-oriented-programming-using-cpp","unix","operating-systems-concepts","networking","database-systems"]
question_bank=[]
for topic in topics:
    page1 = requests.get(main_prefix+topic)
    page1 = bs(page1.content)
    question_bank.extend(select_page(page1, topic))
    scroll = page1.find(class_="ul-top-left")
    links = scroll.find_all("a")
    link_list = []
    for link in links[:2]:
        link_list.append(link['href'])

    for link in link_list:
        page2 = requests.get(prefix+link)
        page2 = bs(page2.content)
        question_bank.extend(select_page(page2, topic))
        pager = page2.find(class_="mx-pager-container").find_all("a")
        inner_link_list = []
        for i in range(6):
            inner_link_list.append(pager[i]['href'])
        for inner_link in inner_link_list:
            final_page = requests.get(prefix+inner_link)
            final_page = bs(final_page.content)
            question_bank.extend(select_page(final_page, topic))
#     break
print(question_bank)



# In[4]:


# import json
# with open("question_bank.json", 'w', encoding='utf-8') as f:
#     json.dump(question_bank, f, ensure_ascii=False, indent=2)
