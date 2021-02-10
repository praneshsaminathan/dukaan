from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator
from accounts.models import BaseModel, Store


class Category(BaseModel):
    name = models.CharField(verbose_name=_('Category Name'), max_length=255, help_text=_('Category name'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)


class Product(BaseModel):
    name = models.CharField(verbose_name=_('Products Name'), max_length=255, help_text=_('Product name'))
    description = models.TextField(verbose_name=_('Product Description'), blank=True, help_text=_('Product Description'))
    mrp = models.FloatField(verbose_name=_('MRP'), help_text=_('MRP'))
    sale_price = models.FloatField(verbose_name=_('Sale Price'), help_text=_('Sale Price'))
    image = models.FileField(verbose_name=_('product_image'), upload_to='product_image', blank=True,
                             null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'pdf'])])
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, help_text=_('Category'))
    store = models.ForeignKey(Store,  on_delete=models.DO_NOTHING, help_text=_('Store'), related_name='products')

    def __str__(self):
        return f'{self.name} - {self.store.slug}'

    class Meta:
        db_table = 'product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('name',)


class Cart(BaseModel):
    line_items = models.TextField(verbose_name=_('Line Items'), help_text=_('Line Items'))

    def __str__(self):
        return f'{self.id}s'

    class Meta:
        db_table = 'cart'
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')


class Order(BaseModel):
    line_items = models.TextField(verbose_name=_('Line Items'), help_text=_('Line Items'))

    def __str__(self):
        return f'{self.id} '

    class Meta:
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
