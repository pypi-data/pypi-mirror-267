import pyqie

class App:
    def __init__(self):
        pyqie.init(1000)
        pyqie.run(self.update, self.draw)

    def update(self):
        sq4 = pyqie.sqrt(4)
        print(sq4)
        print("update")

    def draw(self):
        print("draw")


def main():
    print("123")
    App()


if __name__ == "__main__":
    main()
