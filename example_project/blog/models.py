from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    follow_up = models.ForeignKey("Post", related_name="initial_post", null=True, on_delete=models.SET_NULL)


class Comment(models.Model):
    blog = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
