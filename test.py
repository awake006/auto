import unittest
import xmlrunner
import os


def PATH(path):
    return os.path.abspath(path)


def run():
    suit = unittest.TestSuite()
    case_dir = os.path.join(os.getcwd(), 'auto/test')
    discover = unittest.defaultTestLoader.discover(start_dir=PATH(case_dir), pattern='test_*.py')
    for d in discover:
        suit.addTest(d)
    runner = xmlrunner.XMLTestRunner(output='report')
    runner.run(suit)

if __name__ == "__main__":
    run()
