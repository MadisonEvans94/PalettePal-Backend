# Set up the Django environment

import os
import random  # noqa
import django  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # noqa
django.setup()  # noqa

from django.contrib.auth.models import User
from image_processor.models import Palette, ClusterData
from faker import Faker

fake = Faker()


def delete_existing_data():
    # Be careful with this in a production environment!
    ClusterData.objects.all().delete()
    Palette.objects.all().delete()
    User.objects.all().delete()  # Caution: This will delete all users!


def create_users(num_users=5):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()

        user, created = User.objects.get_or_create(
            username=username, email=email)
        if created:
            user.set_password(password)
            user.save()


def create_main_user():
    username = "main_user"
    email = "main_user@gmail.com"
    password = "password1234"
    user, created = User.objects.get_or_create(
        username=username, email=email)
    if created:
        user.set_password(password)
        user.save()


def create_palettes_and_cluster_data(num_palettes=10, palettes_for_main_user=3):
    users = User.objects.all()
    main_user = User.objects.get(username='main_user')

    for _ in range(num_palettes):
        user = random.choice(
            users) if _ >= palettes_for_main_user else main_user
        name = fake.word().capitalize() + " " + fake.word().capitalize()
        date = fake.date_between(start_date='-1y', end_date='today')
        imageUrl = fake.image_url()

        palette, _ = Palette.objects.get_or_create(
            name=name, date=date, imageUrl=imageUrl, user=user)

        # Generate cluster data
        for cluster_index in range(1, 7):  # 6 rounds of clustering
            # Now we'll create lists of colors and ratios directly
            colors = [fake.hex_color() for _ in range(cluster_index)]
            ratios = [random.randint(1000, 10000)
                      for _ in range(cluster_index)]

            # If you're using PostgreSQL and JSONField in your model
            ClusterData.objects.create(
                palette=palette,
                cluster_index=cluster_index,
                colors=colors,  # Directly assign the list of colors
                ratios=ratios   # Directly assign the list of ratios
            )

            # If you're not using PostgreSQL and need to store this as a string,
            # you'll need to serialize the list to a JSON string:
            # ClusterData.objects.create(
            #     palette=palette,
            #     cluster_index=cluster_index,
            #     colors=json.dumps(colors),  # Serialize the list to a JSON string
            #     ratios=json.dumps(ratios)   # Serialize the list to a JSON string
            # )


def main():
    delete_existing_data()  # Clears out existing data first
    create_users()
    create_main_user()
    create_palettes_and_cluster_data()


if __name__ == '__main__':
    main()
