from src.models import SearchingLinks, FbUsers

urls_for_parser = [
    ('Ubud', 'Rent house ubud',
     'https://www.facebook.com/marketplace/112356482109204/search/?query=Rent%20house%20ubud',
     ),
    ('Ubud', 'villa ubud',
     'https://www.facebook.com/marketplace/112356482109204/search/?query=villa%20ubud&exact=false',
     ),
    ('Ubud', 'Rent house',
     'https://www.facebook.com/marketplace/112356482109204/search?query=Rent%20house',
     ),
    ('Ubud', 'ubud apartment',
     'https://www.facebook.com/marketplace/112356482109204/search?query=ubud%20apartment',
     ),
    ('Ubud', '2 bedroom',
     'https://www.facebook.com/marketplace/112356482109204/search?query=2%20bedroom',
     ),
    ('Ubud', '3 bedroom',
     'https://www.facebook.com/marketplace/112356482109204/search?query=3%20bedroom',
     )
]


users = [
    ('xacraugihexou-5110@yopmail.com', 'kdsxe8t4'),
    ('sefasaukello-6489@yopmail.com', 'kdsxe8t4'),
    ('bofrocresuha-6968@yopmail.com', 'kdsxe8t4'),
    ('gejoppaurufri-3677@yopmail.com', 'kdsxe8t4'),
    ('toifocauvauzu-2252@yopmail.com', 'kdsxe8t4'),
]


for l in urls_for_parser:
    with SearchingLinks.session() as session:
        link = SearchingLinks(link=l[2], geo=l[0], query=l[1])
        session.add(link)
        session.commit()
        session.refresh(link)

for u in users:
    with FbUsers.session() as session:
        user = FbUsers(login=u[0],
                       password=u[1])
        session.add(user)
        session.commit()
        session.refresh(user)
