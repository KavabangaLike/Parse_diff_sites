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
    ('geifadetteuwoi-2186@yopmail.com', 'kdsxe8t5'),
    ('seiyoupeiviwoi-8695@yopmail.com', 'kdsxe8t5'),
    ('kugreufraweti-9375@yopmail.com', 'kdsxe8t5'),
    ('taffousseheze-7383@yopmail.com', 'kdsxe8t5'),
    ('hugiveyada-5236@yopmail.com', 'kdsxe8t5'),
    ('coihollocewe-6078@yopmail.com', 'kdsxe8t5'),
    ('xeixotteiquissau-7998@yopmail.com', 'kdsxe8t5'),
    ('vouyulilloicu-2430@yopmail.com', 'kdsxe8t5'),
    ('loijedebaubrei-8212@yopmail.com', 'kdsxe8t5'),
]


for l in urls_for_parser:
    with SearchingLinks.session() as session:
        link = SearchingLinks(link=l[2], geo=l[0], query=l[1])
        try:
            session.add(link)
            session.commit()
            session.refresh(link)
        except:
            pass

for u in users:
    with FbUsers.session() as session:
        user = FbUsers(login=u[0],
                       password=u[1])
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except:
            pass
