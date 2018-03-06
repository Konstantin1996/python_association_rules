"""
    Входные данные:
        -q733.txt файл
    Выходные данные:
        -Файл log.csv
        -Вывод в консоль ассоциативных правил
        -Вывод в консоль времени работы программы
"""

import pandas as pd
import pyfpgrowth as fp
import numpy as np
import time

start_time = time.time()

number_of_id = 0 # для индексирования таблицы заказов

resourse = pd.read_csv("q733.txt",sep=";") # читаем входной файл
resourse.drop(["y","m","d","activity_type","partner_id","pos_id","remain"],axis=1,inplace=True) # удаляем все ненужные колонки

header = pd.DataFrame(data=None,columns=["co_date","id","good_id","price","cnt"]) # создаем заголовочный Dataframe
header.to_csv("log.csv",sep=";",header=True) # записываем его в первую строку


transactions = [] # лист из листов: здесь будут лежать все товары для каждого заказа
grouping_by = resourse.groupby("id") # группируем по id
for key,value in grouping_by: # для каждого Dataframe сгруппированного по id
    single_data = grouping_by.get_group(key) # извлекаем сам Dataframe
    c_date = single_data["co_date"].iloc[0] # из него извлекаем дату
    c_id = single_data["id"].iloc[0] # извлекаем id
    c_good_id = pd.unique(single_data["good_id"]) # извлекаем лист товаров
    number_of_id = number_of_id+1 # количество id
    c_price = single_data["price"].sum() # суммируем цену для Dataframe и записываем её в переменную
    c_cnt = single_data["cnt"].sum() # аналогично с количеством
    l_strings = [] # лист со строками good_id_N для данного заказа
    l_of_goods = [] # лист с товарами для данного заказа
    for x in c_good_id: # для каждого элемента в good_id
        l_of_goods.append(x) # добавляем товар
        l_strings.append("good_id_" + str(x)) # преобразуем элемент в строку и сохраняем в лист l_strings
    transactions.append(l_of_goods) # добавляем лист заказов
    all_columns = {"co_date": c_date,"id": c_id,"good_id": l_strings,"price": c_price,"cnt": c_cnt} # словарь всех данных
    single_shop_info = pd.DataFrame([all_columns],columns=["co_date","id","good_id","price","cnt"], index=[number_of_id]) # создаем Dataframe
    single_shop_info.to_csv("log.csv",sep=";",mode="a",header=False) # записываем данные в файл

patterns = fp.find_frequent_patterns(transactions,3) # передаем все товары и задаем параметр support
association_rules = fp.generate_association_rules(patterns,0.5) # передаем FP-дерево и задаем вероятность

print("Ассоциативные правила",association_rules)

alg_time = time.time() - start_time # рассчитываем время

print("Время:",alg_time)
