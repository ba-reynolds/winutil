import time

from clipboard import Clipboard


def format_text(text: str) -> str:
    out = ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    for line in text.split("\n"):
        # two different chars!
        if line.endswith("-") or line.endswith("‐"):
            out += line[:-1]
        else:
            out += line + " "
    return out.rstrip(" ")


def main() -> None:
    SLEEP = 1/8

    previous = None
    while True:
        try:
            time.sleep(SLEEP)
            text = Clipboard.get()

            # User copied something that's not text, an image perhaps
            if text == "":
                continue

            if text != previous:
                text = format_text(text)
                Clipboard.set(text)
                previous = text

        except KeyboardInterrupt:
            break
    print("Out!")


if __name__ == "__main__":
    main()
