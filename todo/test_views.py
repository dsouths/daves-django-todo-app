from django.test import TestCase
from .models import Item



class TestViews(TestCase):

    def test_get_todo_list(self):
        reponse = self.client.get('/')
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        reponse = self.client.get('/add')
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'todo/add_item.html')
    
    def test_get_edit_item_page(self):
        item = Item.objects.create(name='Test Todo Item')
        reponse = self.client.get(f'/edit/{item.id}')
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'todo/edit_item.html')

    def test_can_add_item(self):
        response = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/')
    
    def test_can_delete_item(self):
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/delete/{item.id}')
        self.assertRedirects(response, '/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)
    
    def test_can_toggle_item(self):
        item = Item.objects.create(name='Test Todo Item', done=True)
        response = self.client.get(f'/toggle/{item.id}')
        self.assertRedirects(response, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)
