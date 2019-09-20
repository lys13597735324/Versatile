def read_keywords_list():
    row_words = []
    with open("keywords_list.txt", 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line[-1] == "\n":
                row_words.append(line[0:-1])
            else:
                row_words.append(line)
    return row_words