from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Scope


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        tags_dict = {}
        for c in self.forms:
            if c.cleaned_data.get('is_main'):
                count += 1
                if count == 2:
                    raise ValidationError('Основным может быть только один раздел')
            if c.cleaned_data.get('tag'):
                tag = c.cleaned_data.get('tag').id
                tags_dict[tag] = tags_dict.get(tag, 0) + 1
                if tags_dict[tag] == 2:
                    raise ValidationError('Не повторяйте разделы')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    verbose_name = 'Тематика статьи'
    verbose_name_plural = 'Тематики статьи'
    formset = ArticleScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]


@admin.register(Scope)
class Scope(admin.ModelAdmin):
    list_display = ['id', 'name']
