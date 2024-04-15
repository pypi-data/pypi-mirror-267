# -*- coding: utf-8 -*-

from typing import Union, List, Tuple

class Rehuman:
    def __init__(self, num: Union[int, float]) -> None:
        ''' #### 数字格式化
        > 将整数或浮点数格式化为对应格式的字符串
        ##### @ input
        - num：任意数字，整数或浮点数
        ##### @ from_size() 根据num，以字节B为单位，返回格式化后的字节大小
        ##### @ from_seconds() 根据num，以秒为单位，返回格式化后的计时'''
        self.num = num

    def from_size(self, base: int = 1024, unit: Union[List[str], Tuple[str]] = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']) -> str:
        ''' #### 字节格式化
        > 根据num，以字节B为单位，返回格式化后的字节大小，可指定进制、单位
        ##### @ input
        - base：进制，缺省值1024
        - unit：单位，允许字符串类型的列表或元组，单位应由小至大排序，缺省最大单位至PB'''
        for n, i in enumerate(unit):
            if self.num < base ** (n + 1):
                return '{0:0.2f}{1}'.format(self.num / base ** n, i)
    
    def from_seconds(self, maxUnit: str = 'd', maxSeconds: int = 86400, remainFormat: str = '%Hh%Mm%Ss') -> str:
        ''' #### 计时器格式化
        > 根据num，以秒为单位，返回格式化后的计时
        ##### @ input
        - maxUnit：最大单位，当计时秒数超过格式化范围时，超出的时间将全部转换为该单位显示
        - maxSeconds：最大单位对应的秒数，num每超出一个maxSeconds，最大单位计数加1
        - remainFormat：格式化要求，使用标准strftime格式'''
        import datetime
        maxNum = self.num // maxSeconds
        remainNum = datetime.datetime.fromtimestamp(self.num % maxSeconds, tz=datetime.timezone.utc).strftime(remainFormat)
        if maxNum:
            return '{0:0.0f}{1}{2}'.format(maxNum, maxUnit, remainNum)
        else:
            return remainNum
