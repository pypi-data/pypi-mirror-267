from hello import init, run, sqrt


class App:
    def __init__(self):
        init(1000)
        run(self.update, self.draw)

    def update(self):
        sq4 = sqrt(4)
        print(sq4)
        print("update")

    def draw(self):
        print("draw")


def main():
    print("123")
    App()


if __name__ == "__main__":
    main()
