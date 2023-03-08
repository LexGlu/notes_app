from django.test import TestCase
from .models import Note, Category
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
import pytz


def create_test_user():
    """Creates a test user"""
    return User.objects.create_user(username='test_user', password='password')


def create_test_note(category=None, reminder=None):
    """Creates a test note with user and optional category and reminder"""
    return Note.objects.create(title='Test note', text='Test text', author=create_test_user(), category=category,
                               reminder=reminder)


class TestNotes(TestCase):
    def test_note_creation(self):
        """Test that note is created correctly"""
        note = create_test_note()
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'test_user')
        self.assertEqual(note.category, None)
        self.assertEqual(note.reminder, None)

    def test_note_creation_with_category(self):
        """Test that note is created correctly with category"""
        category = Category.objects.create(title='Test category')
        note = create_test_note(category=category)
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'test_user')
        self.assertEqual(note.category.title, 'Test category')
        self.assertEqual(note.reminder, None)

    def test_note_creation_with_reminder(self):
        """Test that note is created correctly with reminder"""
        reminder = datetime.datetime(2023, 11, 11, 11, 11, 11, tzinfo=pytz.UTC)
        note = create_test_note(reminder=reminder)
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'test_user')
        self.assertEqual(note.category, None)
        self.assertEqual(note.reminder, reminder)


class TestViews(TestCase):

    def test_new_note_view_when_user_logged_in(self):
        """Test that new note view returns 200 when user is logged in and that it uses the correct template"""
        create_test_user()
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('notes:new_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_new_note_view_when_user_not_logged_in(self):
        """Test that new note view returns 302 when user is not logged in and redirects to login page"""
        response = self.client.get(reverse('notes:new_note'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:login'))

    def test_new_note_main(self):
        """
        Test that new note is created and saved to the database when user is logged in when new_note view is used
        """

        test_user = create_test_user()
        self.client.login(username='test_user', password='password')
        note_content = {
            'title': 'New note',
            'text': 'New text',
        }
        request = self.client.post(reverse('notes:new_note'), note_content)
        note = Note.objects.get(author=test_user)
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('notes:note_detail', args=[note.id]))
        self.assertEqual(note.title, 'New note')
        self.assertEqual(note.text, 'New text')
        self.assertEqual(note.author.username, 'test_user')

    def test_edit_note_view_when_user_logged_in(self):
        """Test that edit note view returns 200 when user is logged in and that it uses the correct template"""
        note = create_test_note()
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('notes:edit_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_edit_note_view_main(self):
        """
        Test that changes made to note are saved when user is logged in and edit note view is used
        """
        note = create_test_note()
        self.client.login(username='test_user', password='password')
        changes = {
            'title': 'New title',
            'text': 'New text',
        }
        request = self.client.post(reverse('notes:edit_note', args=[note.id]), changes)
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('notes:note_detail', args=[note.id]))
        note.refresh_from_db()
        self.assertEqual(note.title, 'New title')
        self.assertEqual(note.text, 'New text')

    def test_edit_note_view_when_user_not_logged_in(self):
        """Test that edit note view returns 302 when user is not logged in and redirects to note detail page"""
        note = create_test_note()
        response = self.client.get(reverse('notes:edit_note', args=[note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:note_detail', args=[note.id]))

    def test_delete_note_view_when_user_logged_in(self):
        """
        Test that ensures that delete_note view (if user IS logged in):
        1) deletes note
        2) redirects to homepage
        """
        note = create_test_note()
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('notes:delete_note', args=[note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=note.id).exists())
        self.assertEqual(response.url, reverse('notes:homepage'))

    def test_delete_note_view_when_user_not_logged_in(self):
        """
        Test that ensures that delete_note view (if user is NOT logged in):
        1) does not delete note
        2) redirects to note detail page
        """
        note = create_test_note()
        response = self.client.get(reverse('notes:delete_note', args=[note.id]))
        self.assertTrue(Note.objects.filter(pk=note.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:note_detail', args=[note.id]))
