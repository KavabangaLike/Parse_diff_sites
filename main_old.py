from parse_sites import parse


def main():
    re = parse('https://www.vseinstrumenti.ru/product/lazernyj-uroven-ada-cube-mini-basic-edition-a00461-736291/#searchQuery=%D0%9B%D0%B0%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D0%B9+%D0%BD%D0%B8%D0%B2%D0%B5%D0%BB%D0%B8%D1%80+ADA+Cube+Mini+Basic+Edition&searchType=srp')
    print(re)


if __name__ == '__main__':
    main()
