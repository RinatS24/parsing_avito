
import requests
from bs4 import BeautifulSoup
import sys
import time
import random
import sqlite3

telegram_api_url = "https://api.telegram.org"
telegram_token = "TOKEN"  
telegram_chat_id = "CHAT_ID"

PROXIES = [
    {"http": "http://yNYZvu:ePFyXgeN4SYD@mproxy.site:11620", "https": "http://yNYZvu:ePFyXgeN4SYD@mproxy.site:11620"}
]

CHANGE_IP_URL = "https://changeip.mobileproxy.space/?proxy_key=02c0aa0616c3ed7115a845c8a0a03df0"

def create_table():
    """Создает таблицу viewed, если она не существует."""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS viewed (
                id INTEGER,
                price INTEGER
            )
            """
        )
        conn.commit()

def add_record(record_id, price):
    """Добавляет новую запись в таблицу viewed."""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO viewed (id, price) VALUES (?, ?)",
            (record_id, price),
        )
        conn.commit()

def record_exists(record_id, price):
    """Проверяет, существует ли запись с заданными id и price."""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM viewed WHERE id = ? AND price = ?",
            (record_id, price),
        )
        return cursor.fetchone() is not None
        
with open("user_agent_pc.txt", "r") as file:
    USER_AGENTS = [x.strip() for x in file]

cookie = '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c654.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.1610912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5RLYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_419506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZMbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c77052689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1ea5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2da10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b'

def send_telegram_message(message):
        url = f"{telegram_api_url}/bot{telegram_token}/sendMessage"
        data = {
            "chat_id": telegram_chat_id,
            "text": message
        }
       
        requests.post(url, json=data)

def change_ip():
    """Функция для смены IP"""
    try:
        response = requests.get(CHANGE_IP_URL, timeout=5)
        if response.status_code == 200:
            print("IP успешно изменен")
        else:
            print("Ошибка при смене IP")
    except Exception as e:
        print(f"Ошибка при смене IP: {e}")

def get_random_proxy():
    """Возвращает случайный прокси из списка"""
    return random.choice(PROXIES)

def random_headers():
    """Генерирует случайные заголовки"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "ru-RU,ru;q=0.9",
        "cookie": cookie
    }

def create_url(pattern):
    """Формирует URL для поиска на Авито"""
    return f"https://www.avito.ru/volgograd/telefony?q=iphone+{pattern.replace(' ', '+')}&s=104&user=1"

def get_soup(pattern, attempt=1):
    """Парсит страницу, автоматически меняя IP при блокировке"""
    if attempt > 5: 
        print("Превышено число попыток, пропускаем запрос")
        return None
    
    url = create_url(pattern)
    proxy = get_random_proxy()
    
    try:
        res = requests.get(url, headers=random_headers(), proxies=proxy, timeout=10)
        
        if res.status_code in [403, 429]: 
            print(f"Блокировка (код {res.status_code}), меняем IP и повторяем запрос...")
            change_ip()
            time.sleep(random.randint(5, 15))
            return get_soup(pattern, attempt + 1)

        return BeautifulSoup(res.text, "html.parser")

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}, пробуем снова...")
        change_ip()
        time.sleep(random.randint(5, 15))
        return get_soup(pattern, attempt + 1)

def get_ads_count(pattern):
    """Получает количество объявлений"""
    soup = get_soup(pattern)
    if soup:
        count_tag = soup.find("span", {"data-marker": "page-title/count"})
        if count_tag:
            return int(count_tag.text)
    return 0

def get_link_and_title(pattern):
    """Получает ссылку и заголовок первого объявления"""
    soup = get_soup(pattern)
    if soup:
        div = soup.find("div", class_="items-items-pZX46")
        if div:
            a_tag = div.find("a")
            div_tag = div.find("div")
            cost_tag = div.find("strong", class_="styles-module-root-LEIrw")
            if a_tag and div_tag and cost_tag:
                return (f"https://www.avito.ru{a_tag.get('href')}", a_tag.get("title"),int(div_tag.get("data-item-id")),cost_tag.text)
    return None, None, None, None

def main(pattern):
    create_table()
    current_count = get_ads_count(pattern)
    while True:
        new_count = get_ads_count(pattern)
        print(new_count)
        if new_count > current_count:
            link, title, id, price = get_link_and_title(pattern)
            if link and title and id and price:
                if not(record_exists(id,price)):
                    print(title, price,"\n",link)
                    add_record(id, price)
                    send_telegram_message(f"{title} {price}\n{link}")
        current_count = new_count
        time.sleep(random.randint(10, 30)) 

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
