    # csv_file_path = "/Users/anastasiatrubina/Desktop/address.csv"
    # xml_file_path = "/Users/anastasiatrubina/Desktop/address.xml"


import csv
import xml.etree.ElementTree as ET
import time
from collections import Counter
import os

def load_csv_file(file_path):
    data = {}
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader)
        city_index = header.index("city")
        floors_index = header.index("floor")
        for row in csv_reader:
            city = row[city_index].strip('" ')
            floors = int(row[floors_index]) if row[floors_index].isdigit() else 0
            if city in data:
                data[city].append(floors)
            else:
                data[city] = [floors]
    return data

def load_xml_file(file_path):
    data = {}
    tree = ET.parse(file_path)
    root = tree.getroot()
    for item in root.findall('item'):
        city = item.get('city')
        floors = int(item.get('floor'))
        if city in data:
            data[city].append(floors)
        else:
            data[city] = [floors]
    return data

def process_data(data):
    city_counts = Counter(data.keys())
    duplicate_cities = [city for city, count in city_counts.items() if count > 1]

    if duplicate_cities:
        print("Дублирующиеся записи:")
        for city in duplicate_cities:
            count = city_counts[city]
            print(f"{city}: {count} повторений")
    else:
        print("Дублирующихся записей не найдено.")

    floor_counts = {city: Counter(floors) for city, floors in data.items()}
    
    for city, counts in floor_counts.items():
        print(f'\nГород: {city}')
        for i in range(1, 6):
            print(f'Количество {i}-этажных зданий: {counts[i]}')

if __name__ == "__main__":
    csv_file_path = "/Users/anastasiatrubina/Desktop/address.csv"
    xml_file_path = "/Users/anastasiatrubina/Desktop/address.xml"
    
    if not (os.path.exists(csv_file_path) and os.path.exists(xml_file_path)):
        print("Файлы не найдены. Убедитесь, что они находятся в текущей директории.")
    else:
        csv_data = load_csv_file(csv_file_path)
        xml_data = load_xml_file(xml_file_path)
        
        merged_data = {**csv_data, **xml_data}
        
        start_time = time.time()
        process_data(merged_data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f"Время обработки файлов: {processing_time} секунд")
