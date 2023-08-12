from src.models import Product, TgUser, FbUser, SearchLink, Land, Currency, ProductFacility, Facility, Picture, \
    UserGroup
from sqlalchemy import select, or_
from datetime import datetime


# from src.utils.google_sheet import gh_prepare_data, gh_insert


def pg_insert_product(data):  ##
    with Product.session() as session:
        product = Product(
            product_id=data[0].split('/')[5],
            product_link=data[0],
            title=data[1],
            price=data[2],
            currency=session.scalar(select(Currency.id).filter(Currency.symbol == 'rp')),  ##
            in_month=True,  ##

            description=data[4],
            profile_url=data[5],
            expose_datetime=data[7],
        )

        pictures = [Picture(link=i) for i in data[6].split(',')]
        product.pictures = pictures
        facilities = [Facility(name=i, type=3) for i in data[3]]  ##
        # product.facilities = facilities
        session.add(product)
        session.commit()
        session.refresh(product)


def pg_select_product_links():  #
    with Product.session() as session:
        query = select(Product.product_id)
        return [*session.scalars(query).all()]


def pg_select_products(limit: int, offset: int):  ##
    with Product.session() as session:
        query = session.query(Product.product_id,
                              Product.title,
                              Product.product_link,
                              Product.price,
                              Product.description,
                              Product.profile_url,
                              Product.expose_datetime,
                              Picture.link).join(Picture, Picture.product_id == Product.id).limit(limit).offset(
            offset)  ##

        result = query.all()
        return [*result]


def pg_insert_new_user(user_id: str, access_expire: datetime, username: str, role='newbies'):  #
    with TgUser.session() as session:
        user = TgUser(id=user_id, access_expire=access_expire, username=username)
        user.user_group_id = session.scalar(select(UserGroup.id).filter(UserGroup.name == role))
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_select_users_id(groups: list[str]) -> list[str]:  #
    users = []
    for group in groups:
        with TgUser.session() as session:
            query = session.query(TgUser.id).join(UserGroup) \
                .filter(UserGroup.name == group) \
                .filter(or_(datetime.now() < TgUser.access_expire, TgUser.access_expire == None)) \
                .filter(TgUser.show_products == True)
            users.extend(query.all())
    return [i[0] for i in users]


def pg_select_fb_users():  #
    with FbUser.session() as session:
        query = select(FbUser.login,
                       FbUser.password)
        users = session.execute(query)
        return [*users]


def pg_select_links():  #
    with SearchLink.session() as session:
        links = session.query(
            SearchLink.link,
            SearchLink.query,
            Land.name).join(Land, Land.id == SearchLink.land_id, isouter=True).all()
        return [*links]


def pg_change_user_group(user_id, group: str):
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.user_group_id = session.scalar(select(UserGroup.id).filter(UserGroup.name == group))
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_change_user_access_period(user_id, period: datetime | None) -> None:
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.access_expire = period
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_show_ads(user_id, action: bool) -> None:
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.show_products = action
        session.add(user)
        session.commit()
        session.refresh(user)

# gh_insert(*gh_prepare_data(*pg_select_products(1, 45)))
