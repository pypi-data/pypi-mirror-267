# -*- coding: utf-8 -*-

class Unicode_len:
    def __init__(self, text: str) -> None:
        ''' #### 获取全半角混合字符串的长度
        > 半角字符长度为1，全角字符长度为2，以此计算总长度
        ##### @ input
        - text：任意字符串
        ##### @ get_str() 不输出，将整理好的待输出字符串返回
        ##### @ print_str() 直接输出至控制台，可指定end'''
        import unicodedata
        self.length = 0
        for t in text:
            if unicodedata.east_asian_width(t) in ['W','F']:
                self.length += 2
            elif unicodedata.east_asian_width(t) in ['Na','H']:
                self.length += 1
    
    def get_len(self):
        '''get_len()与length等价，但建议使用get_len()'''
        return self.length
