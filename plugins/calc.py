# plugins/calc.py

def run(args):

    try:

        print(eval(args))

    except Exception as e:

        print(e)