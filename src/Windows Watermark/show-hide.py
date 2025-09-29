import ctypes


def main():
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    # Different values for ShowWindow
    SW_HIDE = 0
    SW_SHOW = 5

    # Find the Windows watermark window
    hwnd = ctypes.windll.user32.FindWindowW("Worker Window", None)
    
    if not hwnd:
        print("Couldn't find watermark window")
        return 1

    # Toggle watermark visibility
    if ctypes.windll.user32.IsWindowVisible(hwnd):
        ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
    else:
        ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)

    return 0


if __name__ == "__main__":
    main()
