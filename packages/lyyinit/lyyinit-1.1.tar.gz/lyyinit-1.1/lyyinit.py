import os,sys
import ctypes

def disable_quick_edit_mode():
    """关闭快速编辑模式，避免鼠标终端界面导致程序暂停"""
    if os.name == "nt":
        stdin_handle = ctypes.windll.kernel32.GetStdHandle(-10)
        mode = ctypes.c_ulong()
        ctypes.windll.kernel32.GetConsoleMode(stdin_handle, ctypes.byref(mode))
        ENABLE_QUICK_EDIT_MODE = 0x0040
        ENABLE_INSERT_MODE = 0x0020
        new_mode = mode.value & ~(ENABLE_QUICK_EDIT_MODE | ENABLE_INSERT_MODE)
        ctypes.windll.kernel32.SetConsoleMode(stdin_handle, new_mode)



def get_screen_width_height():
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screen_width, screen_height

def get_geometry_dynamic(rate_width=0.15, rate_height=0.6, rate_x=0.5,rate_y=0.3):
    screen_width, screen_height = get_screen_width_height()
    # 创建窗口的几何布局
    geometry = "%dx%d+%d+%d" % (screen_width * rate_width, screen_height * rate_height, screen_width * rate_x, screen_height * rate_y)
    return geometry