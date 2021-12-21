import os

if __name__ == '__main__':
    print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(__file__)))
    print(os.getcwd())