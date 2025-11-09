class Translit:
    def __init__(self):
        # self.ru_alphabet = set('АЕИОЁУЫЭЮЯБВГДЖЗЙКЛМНПРСТФХЦЧШЩЬЪ')
        self.ru_mapping = {'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е',
                    'Z': 'З', 'I': 'И', '': '', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О',
                    'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', '"': 'Ъ',
                    'Y': 'Ы', "'": "Ь", 'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 
                    'z': 'з', 'i': 'и', 'ĭ': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
                    'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', '"': 'ъ',
                    'y': 'ы', "'": "ь", 
        }

    def ru_map(self, text, i):
        #kh -> х
        if text[i].upper() == 'K' and i < len(text)-1 and text[i+1] == 'h':
            result = 'х' if text[i].islower() else 'Х'
            return result, i+1
        
        # elif text[i].upper() == 'I' and i < len(text)-1 and text[i+1] == 'u':
        #     #iu -> ю
        #     result = 'ю' if text[i].islower() else 'Ю'
        #     return result, i+1
        
        #     #ia -> я
        # elif text[i].upper() == 'I'and i < len(text)-1 and text[i+1] == 'a':
        #     result = 'я' if text[i].islower() else 'Я'
        #     return result, i+1

        elif text[i].upper() == 'Y' and i < len(text)-1 and text[i+1] == 'a':
            #ya -> я
            result = 'я' if text[i].islower() else 'Я'
            return result, i+1
        
        elif text[i].upper() == 'Y' and i < len(text)-1 and text[i+1] == 'u':
            #yu -> ю
            result = 'ю' if text[i].islower() else 'Ю'
            return result, i+1
        
        #'TS': 'Ц'
        elif text[i].upper() == 'T' and i < len(text)-1 and text[i+1] == 's':
            result = 'ц' if text[i].islower() else 'Ц'
            return result, i+1

        # 'CH': 'Ч'
        elif text[i].upper() == 'C' and i < len(text)-1 and text[i+1] == 'h':
            result = 'ч' if text[i].islower() else 'Ч'
            return result, i+1
                
        # 'SH': 'Ш'
        elif text[i].upper() == 'S' and i < len(text)-1 and text[i+1] == 'h':
            result = 'ш' if text[i].islower() else 'Ш'
            return result, i+1
                
        # 'SHCH': 'Щ', 
        elif text[i].upper() == 'S' and i < len(text)-3 and text[i+1] == 'h' and text[i+2] == 'c' and text[i+3] == 'h':
            result = 'щ' if text[i].islower() else 'Щ'
            return result, i+4
        
        # 'ZH': 'Ж'
        elif text[i].upper() == 'Z' and i < len(text)-1 and text[i+1] == 'h':
            result = 'ж' if text[i].islower() else 'Ж'
            return result, i+1

        elif text[i] in self.ru_mapping:
            return self.ru_mapping[text[i]], i

        else:
            return text[i], i

    def russianise(text, fn=ru_map):
        out = ''
        i = 0
        while i < len(text):
            replacement, new_i = fn(text, i)
            out += replacement
            i = new_i + 1 
        
        return out