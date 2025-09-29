import time
import ctypes


def main():
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_SHOW = 5


    # Find the Windows watermark window
    hwnd = ctypes.windll.user32.FindWindowW("Worker Window", None)

    if not hwnd:
        print("Couldn't find watermark window")
        return 1

    while True:

        # Toggle watermark visibility
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
        
        time.sleep(0.5)

    return 0


if __name__ == "__main__":
    main()
