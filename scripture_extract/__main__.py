from dotenv import load_dotenv

from . import main as program


def main():
    load_dotenv()
    program()
