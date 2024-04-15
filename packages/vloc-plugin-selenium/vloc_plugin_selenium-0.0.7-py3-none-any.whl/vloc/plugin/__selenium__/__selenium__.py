from vloc.module import VlocModule
from vloc.plugin.__info__ import DetectInfo


class Action:
    __size = VlocModule.windows_size
    __method = VlocModule.screenshot_method.__self__

    @classmethod
    def slide_up(cls, start: float = 0.8, end: float = 0.1, duration=0):
        x = int(cls.__size['width']*0.5)
        y1 = int(cls.__size['height']*start)
        y2 = int(cls.__size['height']*end)
        cls.__method.swipe(start_x=x, start_y=y1, end_x=x, end_y=y2, duration=duration)

    @classmethod
    def slide_down(cls,start: float = 0.1, end: float = 0.8, duration=0):
        x = int(cls.__size['width']*0.5)
        y1 = int(cls.__size['height']*start)
        y2 = int(cls.__size['height']*end)
        cls.__method.swipe(start_x=x, start_y=y1, end_x=x, end_y=y2, duration=duration)

    @classmethod
    def slide_e2e(cls,start: DetectInfo, end: DetectInfo, duration=1000):
        cls.__method.swipe(start_x=start.x, 
                           start_y=start.y, 
                           end_x=end.x, 
                           end_y=end.y, 
                           duration=duration)





