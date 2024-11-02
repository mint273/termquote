from abc import ABC, abstractmethod

import pandas as pd






class Stack:

    def __init__(self, w1: 'BaseWidget', w2: 'BaseWidget', align_left: bool=True, space: int | None=None):

        self.w1 = w1
        self.w2 = w2

        self.align_left = align_left
        self.space = space


    def __call__(self, src: pd.DataFrame) -> list[list[str]]:
        
        m1 = self.w1(src)
        m2 = self.w2(src)

        return m2 + [[] * self.space] + m1
       



class HorisontalStack:

    def __init__(self, w1: 'BaseWidget', w2: 'BaseWidget', align_bottom: bool=True, space: int | None=None):

        self.w1 = w1
        self.w2 = w2

        self.align_bottom = align_bottom
        self.space = space


    def __call__(self, src: pd.DataFrame) -> list[list[str]]:

        return [r1 + ' ' * self.space + r2 for r1, r2 in zip(self.w1(src), self.w2(src))]




class BaseWidget(ABC):


    def stack(self, widget: 'BaseWidget', align_left: bool=True, space: int | None=None) -> 'BaseWidget':

        widget = BaseWidget()
        widget.__call__ = Stack(self, widget, align_left=align_left, space=space)

        return widget


    def hstack(self, widget: 'BaseWidget', align_bottom: bool=True, space: int | None=None) -> 'BaseWidget':

        widget = BaseWidget()
        widget.__call__ = HorisontalStack(self, widget, align_bottom=align_bottom, space=space)

        return widget


    @abstractmethod
    def __call__(self, src: pd.DataFrame) -> list[list[str]]:

        pass


    def plot(self, src: pd.DataFrame, *args, **kwargs) -> None:

        for row in self(src, *args, **kwargs):

            for cell in row:

                print(cell, end='')

            print('')





