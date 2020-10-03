from faker import Faker
fake = Faker()
password = 'test12345'


class Helper:
    def make_username():

        username = fake.profile(fields=['username'])['username']
        return username

    def make_email():

        email = fake.email()
        return email

