import unittest


def out():
    print("ceshi===yang")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # self.assertEqual(True, False)
        print("ceshi")
        out()


class MyTestCase02(unittest.TestCase):
    def test_something(self):
        # self.assertEqual(True, False)
        print("ceshi02")
        out()


if __name__ == '__main__':
    unittest.main()
