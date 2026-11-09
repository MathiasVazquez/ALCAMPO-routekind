from .generic_base_model import GenericBaseModel


class CustomModelAbstract(GenericBaseModel):

    class Meta:
        abstract = True
