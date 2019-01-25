from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from fishblog.models import Admin, Category, Post, Comment
from fishblog.extensions import db

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Fish\'s Blog',
        blog_sub_title='coding',
        name='Fish',
        about='a salted fish'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author='Fish',
            email='1136727300@qq.com',
            site='li-fish.github.io',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            from_admin=True,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(randint(1, Post.query.count())),
            replied=Comment.query.get(randint(1, Comment.query.count())),
        )
        db.session.add(comment)
    db.session.commit()
