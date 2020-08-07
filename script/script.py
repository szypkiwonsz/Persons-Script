import argparse

parser = argparse.ArgumentParser(description='Human data operations')
args = parser.parse_args()

if __name__ == '__main__':

    if not any(vars(args).values()):
        print('There are no arguments passed!')
