from django.db import models
import re


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 4 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 4 characters'
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required'
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 4:
            errors['password'] = 'Password must be at least 4 characters'
        if postData['password'] != postData['confirmPw']:
            errors['confirmPw'] = 'Passwords must match'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
