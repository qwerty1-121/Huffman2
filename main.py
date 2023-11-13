import heapq
import pickle


class TreeNode:
    def __init__(self) -> None:
        self.symbol = None
        self.left = None
        self.right = None

    def __lt__(self, other):
        return True


# Функция для построения дерева Хаффмана
def build_huffman_tree(symbols_count):
    heap = []

    # Создание узлов для каждого символа с их приоритетами и добавление их в приоритетную очередь (heap)
    for symbol, count in symbols_count.items():
        temp_node = TreeNode()
        temp_node.symbol = symbol
        heapq.heappush(heap, (count, temp_node))

    # Объединение узлов с наименьшими приоритетами, пока не останется только корневой узел
    while len(heap) > 1:
        priority1, node1 = heapq.heappop(heap)
        priority2, node2 = heapq.heappop(heap)
        new_node = TreeNode()
        new_node.left = node1
        new_node.right = node2
        heapq.heappush(heap, (priority1 + priority2, new_node))

    # Получение корневого узла, который является корнем дерева Хаффмана
    root = heapq.heappop(heap)
    return root[1]


# Функция для построения словаря кодирования
def build_encoding_dict(data):
    symbols_count = {}

    # Подсчет частоты встречаемости каждого символа в данных
    for symbol in data:
        if symbols_count.get(symbol) is None:
            symbols_count[symbol] = 1
        else:
            symbols_count[symbol] += 1

    # Построение дерева Хаффмана и словаря кодирования
    root = build_huffman_tree(symbols_count)
    return traverse_tree(root, "", {})


# Рекурсивная функция для обхода дерева и создания словаря кодирования
def traverse_tree(node, code, encoding_dict):
    if node.symbol is None:
        # Рекурсивный обход левого и правого поддеревьев
        traverse_tree(node.left, code + "1", encoding_dict)
        traverse_tree(node.right, code + "0", encoding_dict)
    else:
        # Достигнута листовая вершина дерева, добавляем символ и его код в словарь кодирования
        code = '1' + code  # Префикс '1' используется для удобства отделения символов в битовых строках
        if node.symbol == '\n':
            print("\'\\n\': ", code, " (", int(code, 2), ")", sep='')  # Вывод информации о коде символа
        else:
            print("\'", node.symbol, "\' : ", code, " (", int(code, 2), ")", sep='')  # Вывод информации о коде символа
        encoding_dict[node.symbol] = code
    return encoding_dict


# Функция для чтения текстового файла
def read_text_file(file_name):
    with open(file_name, "rt", encoding="utf-8-sig") as text_file:
        return text_file.read()


# Функция для записи в текстовый файл
def write_text_file(file_name, data):
    with open(file_name, "w") as text_file:
        text_file.write(data)


# Функция для кодирования данных
def encode_data(data, encoding_dict):
    encoded_data = ""
    for char in data:
        encoded_data += encoding_dict.get(char)
    return bitstring_to_bytes(encoded_data)


# Функция для преобразования битовой строки в байты
def bitstring_to_bytes(bitstring):
    value = int(bitstring, 2)
    bytes_data = bytearray()
    while value:
        bytes_data.append(value & 0xff)
        value >>= 8
    return bytes(bytes_data[::-1])


# Функция для декодирования данных
def decode_data(data, decoding_dict):
    code = ''
    decoded_data = ''
    bitstring = bin(data[0])[2:]
    for i in range(1, len(data)):
        bitstring += bin(data[i])[2:].zfill(8)
    for bit in bitstring:
        code += bit
        if decoding_dict.get(code) is not None:
            decoded_data += decoding_dict[code]
            code = ''
    return decoded_data


# Функция для разворота словаря кодирования
def reverse_encoding_dict(encoding_dict):
    return {code: char for char, code in encoding_dict.items()}


# Функция для сохранения словаря кодирования и закодированных данных
def save_encoding_and_data(encoding_dict, encoded_data, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(encoding_dict, file)
        pickle.dump(encoded_data, file)


# Функция для загрузки словаря кодирования и закодированных данных
def load_encoding_and_data(file_name):
    with open(file_name, 'rb') as file:
        encoding_dict = pickle.load(file)
        encoded_data = pickle.load(file)
        return encoding_dict, encoded_data


# Основная функция
def main():
    while True:
        choice = int(input(
            "Для кодирования файла введите 1\nДля декодирования файла введите 2\nДля выхода введите 0\nВыбор режима: "))
        if choice == 0:
            break
        elif choice == 1:
            data = read_text_file("original.txt")
            encoding_dict = build_encoding_dict(data)
            encoded_data = encode_data(data, encoding_dict)
            save_encoding_and_data(encoding_dict, encoded_data, 'huffman_data.pkl')
            print("Файл успешно закодирован.")
        elif choice == 2:
            encoding_dict, encoded_data = load_encoding_and_data('huffman_data.pkl')
            decoded_data = decode_data(encoded_data, reverse_encoding_dict(encoding_dict))
            write_text_file("decoded.txt", decoded_data)
            print(reverse_encoding_dict(encoding_dict))
            print("Файл успешно декодирован.")
        else:
            print("Некорректный выбор. Пожалуйста, выберите 0, 1 или 2.")
        print('-' * 20)


if __name__ == "__main__":
    main()
