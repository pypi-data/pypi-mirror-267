# -*- coding: utf-8 -*-

class Rows_print:
    def __init__(self, text: str = '', align: str = '<', start: int = None) -> None:
        ''' #### 多行输出
        > 可以指定输出起始行次、对齐方式
        ##### @ input
        - text：准备输出的文本，单行多行皆可
        - align：对齐方式，< 左对齐、^ 居中、> 右对齐，根据最长行次对齐，整体左对齐
        - start：起始行次，-1为上一行、-2为上两行，依此类推；0为正常输出、2为下一行输出，依此类推；缺省为自动识别，按文本行次向上
        ##### @ print_str() 直接输出至控制台
        ##### @ get_str() 不输出，将整理好的待输出字符串返回'''
        from .Unicode_len import Unicode_len
        from .Respacing import Respacing
        textList = text.split('\n')
        start = start if start else -len(textList)
        maxLenght = max([Unicode_len(i).length for i in textList])
        textList = [Respacing([i, maxLenght, align]).get_str() for i in textList]
        space = f'\n{self._clr_row()}'
        reText = space.join(textList)
        if start < 0:
            self.formatStr = f'{self._up(-start)}{self._clr_row()}{reText}'
        elif start > 0:
            self.formatStr = f'{self._clr_row()}{reText}'
        else:
            self.formatStr = f'{self._down(start)}{self._clr_row()}{reText}'
        
    def _up(self, n: int = 1) -> str:
        return f'\033[{n}A'
    
    def _down(self, n: int = 1) -> str:
        return f'\033[{n}B'
    
    def _right(self, n: int = 1) -> str:
        return f'\033[{n}C'
    
    def _left(self, n: int = 1) -> str:
        return f'\033[{n}D'
    
    def _clr_row(self) -> str:
        return '\033[2K'
    
    def print_str(self) -> None:
        print(self.formatStr)
        return
    
    def get_str(self) -> str:
        '''get_str()与formatStr等价，但建议使用get_str()'''
        return self.formatStr