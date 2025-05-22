from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Main(models.Model):
    """Абстрактная базовая модель с общими полями."""
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(Main):
    """Модель категории для классификации публикаций."""
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

    def __str__(self):
        """Возвращает строковое представление категории."""
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(Main):
    """Модель местоположения для связывания с публикациями."""
    name = models.CharField('Название места', max_length=256)

    def __str__(self):
        """Возвращает строковое представление местоположения."""
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(Main):
    """Модель публикации с содержимым и связями."""
    title = models.CharField('Название', max_length=256)
    text = models.TextField('Текст')
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать отложенные '
            'публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    def __str__(self):
        """Возвращает строковое представление публикации."""
        return self.title

    def get_absolute_url(self):
        """Возвращает абсолютный URL для детали публикации."""
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)


class Comments(models.Model):
    """Модель комментария к публикации."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    def __str__(self):
        """Возвращает строковое представление комментария."""
        return f'Комментарий от {self.author} к {self.post}'

    def get_absolute_url(self):
        """Возвращает абсолютный URL для детали публикации."""
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']  # Сортировка от старых к новым
