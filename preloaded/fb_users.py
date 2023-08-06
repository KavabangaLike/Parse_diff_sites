from ..src.models import FbUsers

users = [
    ('xacraugihexou-5110@yopmail.com', 'kdsxe8t4'),
    ('sefasaukello-6489@yopmail.com', 'kdsxe8t4'),
    ('bofrocresuha-6968@yopmail.com', 'kdsxe8t4'),
    ('gejoppaurufri-3677@yopmail.com', 'kdsxe8t4'),
    ('toifocauvauzu-2252@yopmail.com', 'kdsxe8t4'),
]

for u in users:
    with FbUsers.session() as session:
        user = FbUsers(login=u[0],
                       password=u[1])
        session.add(user)
        session.commit()
        session.refresh(user)


