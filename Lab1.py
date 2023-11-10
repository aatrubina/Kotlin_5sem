import requests
from bs4 import BeautifulSoup
import webbrowser

def search_wikipedia(query):
    page = 1
    while True:
        url = f"https://ru.wikipedia.org/w/index.php?search={query.replace(' ', '+')}&page={page}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all("div", class_="mw-search-result-heading")
            
            if not results:
                if page == 1:
                    print("По вашему запросу ничего не найдено.")
                break

            print(f"Результаты поиска (Страница {page}):")
            for i, result in enumerate(results, 1):
                title = result.a.text
                print(f"{i}. {title}")

            while True:
                try:
                    choice = int(input("Выберите номер статьи для открытия (или 0 для перехода к следующей странице, -1 для отмены): "))
                    if choice == -1:
                        return
                    elif choice == 0:
                        break
                    elif choice >= 1 and choice <= len(results):
                        selected_result = results[choice - 1]
                        article_url = selected_result.a['href'] #извлекает URL-адрес статьи, на которую указывает ссылка внутри элемента selected_result. 
                        #После выполнения этой строки, переменная article_url будет содержать URL-адрес выбранной статьи, который затем используется для открытия этой статьи в браузере с помощью webbrowser.open().
                        webbrowser.open(f"https://ru.wikipedia.org{article_url}")
                    else:
                        print("Неверный выбор. Пожалуйста, выберите номер статьи из списка.")
                except ValueError:
                    print("Введите число.")
            
            page += 1
        else:
            print(f"Ошибка при выполнении запроса для страницы {page}.")

if __name__ == "__main__":
    user_query = input("Введите поисковый запрос: ")
    
    search_wikipedia(user_query)
