from db.alembic_orm.add import Users, Medications, Orders, Demands, Session

session = Session()

users = [
    Users(email='nicik@gmail.com', username='Anatoliy Zakharchenko',
          password_hash='EF797C8118F02DFB649607DD5D3F8C7623048C9C063D532CC95C5ED7A898A64F'),
    Users(email='supercolor@gmail.com', username='Anatoliy Zakharchenko',
          password_hash='9377935330AC2D6DF60B8040C482E839286B91AF0C3CF44CC14621EC13DF26EF'),
    Users(email='ohimnewuser@ukr.net', username='Romeo Gospodiowych',
          password_hash='9B8769A4A742959A2D0298C36FB70623F2DFACDA8436237DF08D8DFD5B37374C'),
    Users(email='pdurov@mail.ru', username='Rick Romeos',
          password_hash='05F03A7011D2E3F0738F6E0E1C9491A1C0FAD74AA16528B4414A7F4A5978A641'),
    Users(email='linakilchenko@mail.ru', username='Lina Romarko',
          password_hash='131E27B7715C43825F14696B907812D34FB86A529DD8C98FEDBF87016F5D9149'),
]

medicatioms = [
    Medications(name='Smekta',
                description='Super-puper preparat likue wid raku, straxu wysoty, daje wminnia keruwaty helicopterom, widprawliae na Weneru',
                cost=2, quantity=12, in_stock=True),
    Medications(name='Wedmeszujky',
                description='Shcob strybaty wyshche neba bihaty dopomahaty treba smachni Wedmeszuyki koszen den usim szuwaty! Wedmeszujki - weseli vitaminy dla rozwytku dytyny!',
                cost=0.25, quantity=1000, in_stock=True),
    Medications(name='Amizon',
                description='Pryvit a de vsi? - Zahworily _ A ty? - Amizon _Ukrainskoju bud laska - Amizon', cost=22,
                quantity=0, in_stock=False),
    Medications(name='Ozvirin', description='Lets live friendly', cost=12, quantity=123, in_stock=True),
    Medications(name='Waleriana', description='For nerwy (AntyOzviryn)', cost=13, quantity=121, in_stock=True),
]

orders = [
    Orders(user_id=2, med_id=4, amount=5, completed=True),
    Orders(user_id=2, med_id=5, amount=10, completed=False),
    Orders(user_id=1, med_id=2, amount=1, completed=False),
    Orders(user_id=4, med_id=3, amount=1, completed=True),
    Orders(user_id=3, med_id=1, amount=3, completed=False),
]

demands = [
    Demands(user_id=2, med_id=5, amount=100000),
    Demands(user_id=1, med_id=3, amount=10),
    Demands(user_id=2, med_id=5, amount=1000000),
    Demands(user_id=4, med_id=4, amount=1),
    Demands(user_id=3, med_id=1, amount=1),
]

session.add_all(users)
session.add_all(medicatioms)
session.add_all(orders)
session.add_all(demands)
session.commit()
session.close()

