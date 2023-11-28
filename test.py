with open('urls.txt', 'r', encoding='utf-8') as file:
    url_list = []
    for line in file:
        url_list.append(line.rstrip())

print(url_list)


with open('urls.txt', 'a', encoding='utf-8') as file:
    url_list = ['1','2',"3"]
    for line in url_list:
        file.write(line + '\n')






    
