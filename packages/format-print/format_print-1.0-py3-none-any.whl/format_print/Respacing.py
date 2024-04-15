# -*- coding: utf-8 -*-

from typing import Union, List, Tuple

class Respacing:
    def __init__(self, *args: Union[List[Union[str, int, str]], Tuple[Union[str, int, str]], str], interval: str ='', space: str =' ') -> None:
        ''' #### 全半角混合对齐
        > 为同时包含全角和半角的字符串设置对齐，半角字符视为1格，全角字符视为2格
        ##### @ input
        - *args：允许为列表、元组或字符串，其中单独的字符串将保持原格式；列表与元组中应包含3个元素：
            1. 待对齐的字符串，str
            2. 输出最短长度，int，单位为半角字符的1格，待对齐字符串长度超过最短长度时不生效
            3. 对齐方式，str，< 左对齐，多余空格补在右侧；> 右对齐，多余空格补在左侧；^ 居中，多余空格一半补在左边，一半补在右边
        - interval：所有args之间的间隔内容，缺省为空字符串
        - space：可更换补足长度的符号，缺省为空格
        ##### @ get_str() 不输出，将整理好的待输出字符串返回
        ##### @ print_str() 直接输出至控制台，可指定end'''
        from .Unicode_len import Unicode_len
        textList = []
        for items in args:
            if isinstance(items, (tuple, list)):
                text = str(items[0])
                count = int(items[1])
                sign = items[2]
                uniLen = Unicode_len(text).get_len()
                count -= uniLen
                if sign == '<':
                    textList.append('{0}{1}'.format(text, space*count))
                elif sign == '>':
                    textList.append('{0}{1}'.format(space*count, text))
                elif sign == '^':
                    textList.append('{0}{1}{2}'.format(space*(count-int(count/2)), text, space*int(count/2)))
            else:
                textList.append(str(items))

        self.formatStr = interval.join(textList)
    
    def get_str(self) -> str:
        '''get_str()与formatStr等价，但建议使用get_str()'''
        return self.formatStr

    def print_str(self, end: str = '\n') -> None:
        '''可指定print方法的end参数，缺省为\\n'''
        print(self.formatStr, end = end)
        return
