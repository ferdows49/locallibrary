from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """Model repregenting a book genre."""
    name = models.CharField(max_length = 200, help_text = "Enter a book genre")

    def __str__(self):
        """String for representing the model object."""
        return self.name



class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length = 200)
    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)
    summary = models.TextField(max_length= 1000, help_text='Enter a brief discription of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text = 'Select a genre for this book.')
    language = models.ManyToManyField('Language', help_text = "Select book language.")


    def __str__(self):
        return self.title, self.author

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

    def display_language(self):
        """Create a string for book language"""
        return ', '.join(language.name for language in self.language.all()[:3])
    
    display_language.short_description = 'Language'

class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = 'Unique id for this particular book accross whole library')
    book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True, blank = True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = 'Book availiability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField('Died', null = True, blank = True)
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def get_absolute_url(self):
        return reverse('author-detail', args = [str(self.id)])
    
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Language(models.Model):
    """This model represents the book language"""

    name = models.CharField(max_length = 200, help_text = 'Enter the books language')

    def __str__(self):
        return self.name
    