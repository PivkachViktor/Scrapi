from requests import get

#2. Переконатись, що сторінки є статичними. Використовуючи бібліотеку requests завантажити сторінку зі списком та вивести в консоль.
url = "https://www.cusu.edu.ua/ua/"
response_page = get(url)

# print(response_page.text)
# print(f"Status code: {response_page.status_code}")
# print("========================================")


from bs4 import BeautifulSoup

soup = BeautifulSoup(response_page.content, 'html.parser')

# 5. Зберегти результати скрапінгу до текстового файлу.
FILE_NAME = "lab1.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    faculties = soup.find_all('ul', class_='sp-dropdown-items')  # Знаходимо всі елементи підрозділів
    for faculty in faculties[2].find_all('li'):
        faculty_a = faculty.find('a')
        faculty_name = faculty_a.find(string = True)
        file.write(f"\nНазва факультету: {faculty_name}\n")
        faculty_href = faculty_a.get('href')
        file.write(f"   URL: {faculty_href}\n")
        print(faculty_name)
        print(faculty_href)
        print("")
        print("")
        print("")
        print("")

        #4. Використовуючи запити отримати списки із кожної зі сторінок підрозділів.
        response_faculty_page = get("https://www.cusu.edu.ua/"+faculty_href)
        faculty_soup = BeautifulSoup(response_faculty_page.content, 'html.parser')
        menu_li = faculty_soup.find_all('a', class_="accordeonck")
        for li in menu_li:
            department_name = li.find(string=True)
            if 'Кафедра' in department_name:
                department_name = li.find(string=True)
                print(department_name)
                file.write(f"\nНазва кафедри: {department_name}\n")


