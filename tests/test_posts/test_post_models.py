import pytest

from posts.models import Post

pytestmark = pytest.mark.django_db


class TestPostModel:
    """
    Test Post model
    """

    def test_post_creation(self):
        """
        Test post creation
        """
        post = Post.objects.create(
            title="Test Post",
            content={"test": "test"},
            author_id=1,
        )
        assert post.title == "Test Post"
        assert post.content == {"test": "test"}
        assert post.author_id == 1