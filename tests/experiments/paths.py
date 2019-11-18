from tests import conftest as ct

if __name__ == "__main__":
    # path1 = ct.get_test_path()
    # path2 = ct.get_test_path_alt()
    # print(path1, path1.exists())
    # print(path2)
    # print(path1 == path1)
    # print('hello' == 'hello')
    # print(path1 == path2)
    path = ct._get_test_path('csv')
    print(type(path))
    suf = path.suffix
    print(suf, suf=='.csv')
