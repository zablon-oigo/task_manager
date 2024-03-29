from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse


class TaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='secret'
        )
        cls.task=Task.objects.create(
            title='New task',
            slug='new-task',
            body='testing task app',
            status='pending',
            created_by=cls.user
        )

    def test_model_content(self):
        self.assertEqual(self.task.title, "New task")
        self.assertEqual(self.task.slug, "new-task")
        self.assertEqual(self.task.body, "testing task app")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.created_by.username, "testuser")
        self.assertEqual(str(self.task), "New task")
        self.assertEqual(self.task.get_absolute_url(), "/detail/1/new-task/")

    
    def test_task_list_view(self):
        self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New task")
        self.assertTemplateUsed(response, "task/list.html")
        
    
    def test_task_detail_view(self):
        self.client.login(username='testuser', password='secret')
        response=self.client.get(reverse("detail", kwargs={"pk": self.task.pk, "slug": self.task.slug}))
        no_response=self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "New task")
        self.assertTemplateUsed(response, "task/detail.html")
    
    def test_task_create_view(self):
        self.client.login(username='testuser', password="secret")
        response=self.client.post(reverse("create", {
            "title":"another task",
            "body":"new task",
            "slug":"another-task",
            "created_by":self.user.pk,
            "status":"pending"
        }))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().title, "another task")
        self.assertEqual(Task.objects.last().body, "new task")

    
    def test_task_update_view(self):
        self.client.login(username="testuser", password="secret")
        response=self.client.post(reverse("update", args="1"),{
            "title":"updated task title",
            "body":"updated task"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().title, "updated task title")
        self.assertEqual(Task.objects.last().body, "updated task")

    
    def test_task_delete_view(self):
        self.client.login(username="testuser", password="secret")
        response=self.client.post(reverse("delete", args="1"))
        self.assertEqual(response.status_code, 302)

