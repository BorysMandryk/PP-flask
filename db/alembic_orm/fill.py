from db.alembic_orm.add import User, Medication, Order, Session, RoleEnum

session = Session()

users = [
    User(email='nicik@gmail.com',
          password_hash='EF797C8118F02DFB649607DD5D3F8C7623048C9C063D532CC95C5ED7A898A64F', role=RoleEnum.user),
    User(email='supercolor@gmail.com',
          password_hash='9377935330AC2D6DF60B8040C482E839286B91AF0C3CF44CC14621EC13DF26EF', role=RoleEnum.user),
    User(email='ohimnewuser@ukr.net',
          password_hash='9B8769A4A742959A2D0298C36FB70623F2DFACDA8436237DF08D8DFD5B37374C', role=RoleEnum.provisor),
    User(email='pdurov@mail.ru',
          password_hash='05F03A7011D2E3F0738F6E0E1C9491A1C0FAD74AA16528B4414A7F4A5978A641', role=RoleEnum.user),
    User(email='linakilchenko@mail.ru',
          password_hash='131E27B7715C43825F14696B907812D34FB86A529DD8C98FEDBF87016F5D9149', role=RoleEnum.user),
]

# medicatioms = [
#     Medication(name='Smekta',
#                 description='Super-puper preparat likue wid raku, straxu wysoty, daje wminnia keruwaty helicopterom, widprawliae na Weneru',
#                 cost=2, quantity=12, in_stock=True),
#     Medication(name='Wedmeszujky',
#                 description='Shcob strybaty wyshche neba bihaty dopomahaty treba smachni Wedmeszuyki koszen den usim szuwaty! Wedmeszujki - weseli vitaminy dla rozwytku dytyny!',
#                 cost=0.25, quantity=1000, in_stock=True),
#     Medication(name='Amizon',
#                 description='Pryvit a de vsi? - Zahworily _ A ty? - Amizon _Ukrainskoju bud laska - Amizon', cost=22,
#                 quantity=0, in_stock=False),
#     Medication(name='Ozvirin', description='Lets live friendly', cost=12, quantity=123, in_stock=True),
#     Medication(name='Waleriana', description='For nerwy (AntyOzviryn)', cost=13, quantity=121, in_stock=True),
# ]

session.add_all(users)
# session.add_all(medicatioms)
session.commit()
session.close()

