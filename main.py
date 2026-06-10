from core.banner import show_banner
from core.repl import AstraREPL


def main():

    show_banner()

    repl = AstraREPL()

    repl.run()


if __name__ == "__main__":

    main()