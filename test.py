from bs4 import BeautifulSoup


with open('aa.html', 'r', encoding='utf-8') as file:
    data: str = file.read()
    soup = BeautifulSoup(data, 'lxml')
    b = soup.find_all(attrs={'class': 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24'})
    l = []
    for i in b:
        # print(i)
        try:
            l.append((i.find('a')['href'], i.find_all('span')[6].text))
        except TypeError:
            pass
        print(l)
    print(len(l))



'''https://www.facebook.com/marketplace/item/340434674575201/?ref=category_feed&referral_code=undefined&referral_story_type=listing&tracking=%7B%22qid%22%3A%22-3497024834978816708%22%
2C%22mf_story_key%22%3A%224518818171580204%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A4518818171580204%2C%5C%22target_type%5C%22%3A0%2C%5C%22primary_position%5C%2
2%3A0%2C%5C%22ranking_signature%5C%22%3A1361672643362684928%2C%5C%22commerce_channel%5C%22%3A504%2C%5C%22value%5C%22%3A7.3058303511076e-5%2C%5C%22candidate_retrieval_source_map%5C%
22%3A%7B%5C%224518818171580204%5C%22%3A3001%7D%7D%22%2C%22ftmd_400706%22%3A%22111112l%22%7D'''
'''/marketplace/item/776781477509534/?ref=category_feed&referral_code=undefined&referral_story_type=listing&tracking=%7B%22qid%22%3A%22-3497046343910656631%22%2C%22mf_story_key%22%3A%226792679374127693%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A6792679374127693%2C%5C%22target_type%5C%22%3A0%2C%5C%22primary_position%5C%22%3A0%2C%5C%22ranking_signature%5C%22%3A2477519509234122752%2C%5C%22commerce_channel%5C%22%3A504%2C%5C%22value%5C%22%3A8.5229380357917e-5%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%226792679374127693%5C%22%3A3003%7D%7D%22%2C%22ftmd_400706%22%3A%22111112l%22%7D&__tn__=!%3AD'''