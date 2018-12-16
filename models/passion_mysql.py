from peewee import *
import settings

db = MySQLDatabase(settings.DB_NAME,
                   user=settings.MYSQL_USER,
                   password=settings.MYSQL_PASS,
                   host=settings.MYSQL_HOST,
                   port=settings.MYSQL_PORT)


class Category(Model):
    id = PrimaryKeyField()
    category = TextField()
    link = TextField()
    url_hash = TextField()
    updated_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'category'


class LinkPage(Model):
    id = PrimaryKeyField()
    link = TextField()
    url_hash = TextField()
    updated_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'link_page'


class LinkProduct(Model):
    id = PrimaryKeyField(default=0)
    title = TextField()
    name = TextField()
    link = TextField()
    category = TextField()
    image = TextField()
    url_hash = TextField()
    updated_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'link_product'


def parse_cmd_args_to_cls_method(arg):
    pass


_all_tables = [
    Category,
    LinkPage,
    LinkProduct,
]


def create_tables():
    db.create_tables(_all_tables, safe=True)
    print('Create table successfully')


def delete_tables():
    db.drop_tables(_all_tables, safe=True)
    print('Delete table successfully')


if __name__ == '__main__':
    delete_tables()
    create_tables()
