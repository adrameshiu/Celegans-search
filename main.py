from lib import options
from lib import module1

if __name__ == '__main__':
    args_parser = options.ArgsCLI()
    args = args_parser.parse()
    print(args)
    module1.func1()
    module1.func2()
    print("Im done")
