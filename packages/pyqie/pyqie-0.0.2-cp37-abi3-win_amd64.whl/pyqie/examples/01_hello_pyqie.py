import asyncio

import pyqie

class App:
    def __init__(self):
        pyqie.init(1000)
        pyqie.run(self.update, self.draw,self.close)

    def update(self):
        sq4 = pyqie.sqrt(4)
        print(sq4)
        print("update")

    def draw(self):
        print("draw")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.consumer())

    def close(self):
        print("close")

    async def consumer(self):
        print("consumer")


def main():
    print("123")
    App()


if __name__ == "__main__":
    main()
