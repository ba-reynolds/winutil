import ctypes
import time


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long)
    ]


class RECT(ctypes.Structure):
    # https://learn.microsoft.com/en-us/windows/win32/api/windef/ns-windef-rect
    _fields_ = [
        ("left", ctypes.c_int),
        ("right", ctypes.c_int),
        ("top", ctypes.c_int),
        ("bottom", ctypes.c_int)
    ]


def move_window_keep_size(hwnd, x, y):
    # `RECT()` instance which will hold the position of the watermark window
    rect = RECT()

    # Save pos of watermark window to the instance created above
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

    # Calculate width and height of the window
    # width = 281, height = 48... for windows watermark
    width, height = rect.top - rect.left, rect.bottom - rect.right

    # Move watermark window
    ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height)


def main():
    # http://computer-programming-forum.com/1-vba/cfd80bf1592b3f2b.htm
    # Second comment, difference between functions ending with "A" and "W".

    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    # Different values for ShowWindow
    SW_HIDE = 0
    SW_SHOW = 5

    # Find the Windows watermark window
    hwnd = ctypes.windll.user32.FindWindowW("Worker Window", None)
    
    if not hwnd:
        print("Couldn't find watermark window")
        return 1

    mouse_pos = POINT()
    while True:
        ctypes.windll.user32.GetCursorPos(ctypes.byref(mouse_pos))
        move_window_keep_size(hwnd, mouse_pos.x, mouse_pos.y)
        # time.sleep(0.05)



if __name__ == "__main__":
    main()


# https://stackoverflow.com/a/47164844
# EnumWindows done right

# https://devblogs.microsoft.com/oldnewthing/20031125-00/?p=41713
# what does WPARAM and LPARAM mean