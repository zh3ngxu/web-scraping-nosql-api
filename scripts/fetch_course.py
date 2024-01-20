from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests,csv,time
from random import randint
import requests

output_file_path = 'data/output.csv'
website = "https://hackr.io/blog/tag/courses"
csv_header = [
    "course_title",
    "course_tag",
    "author",
    "course_date",
    "course_link",
    "article_content_first_4_graph",
]

def write_csv_header(file_path,csv_header):
    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(csv_header)

def write_to_csv(file_path,*args):
    with open(file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(args)

def get_single_course_info(url):
    time.sleep(randint(0, 4))
    response = requests.get(url)
    if response.status_code==200:
        course_content = BeautifulSoup(response.text, 'html.parser')

        author_tag = course_content.find("a", {"class":"align-middle inline-block text-hackr-blue text-p14 font-medium"})
        author = author_tag.get_text().strip()
        print("author: ", author)

        course_date_tags = course_content.findAll("span", {"class":"align-middle inline-block text-hackr-black text-p14 font-medium"})
        for course_date_tag in course_date_tags:
            course_date = course_date_tag.get_text().strip()
            if course_date != "|":
                course_date
        print("course date: ", course_date)

        article_content_tag = course_content.find("article",{"class":"article-content"})
        article_paragraphs=[ article_paragraph.get_text() for article_paragraph in article_content_tag.findAll("p")[:4]]
        article_content_first_4_graph = "".join(article_paragraphs)
        print("article content: ", article_content_first_4_graph[:30], "...")
        print("---------")
    
    return course_content, author, course_date, article_content_first_4_graph


response = requests.get(website)
soup_data = BeautifulSoup(response.text, 'html.parser')
course_cards = soup_data.find_all("div", {"class":"col-md-4 col-sm-6"})

write_csv_header(output_file_path, csv_header)

for course_card in course_cards:
    
    course_title = course_card.find("h3",{"class":"card-title"}).get_text()
    print("course title: ", course_title)

    course_tag = course_card.find("div",{"class":"tags"}).get_text()
    print("course tag: ", course_tag)

    course_link = course_card.find("a",{"class":"js-post-link"}).attrs.get("href",None)
    print("course link: ", course_link)

    course_content, author, course_date, article_content_first_4_graph = get_single_course_info(url=course_link)

        
    write_to_csv(output_file_path, course_title, course_tag, author, course_date, course_link, article_content_first_4_graph)
    

