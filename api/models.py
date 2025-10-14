from tortoise import fields
from tortoise.models import Model

class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True, null=False)
    comment = fields.CharField(max_length=255, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    category = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} ({self.category})"