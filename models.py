from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Launch(models.Model):
    """
    The Launch model
    """
    id = fields.UUIDField(pk=True)
    reference_id=fields.CharField(max_length=50,null=False,unique=True)
    title  = fields.CharField(max_length=100)
    rocket = fields.CharField(max_length=100)
    missionTitle = fields.CharField(max_length=150)
    missionDescription = fields.CharField(max_length=1000)
    launchPad = fields.CharField(max_length=100)
    orbit = fields.CharField(max_length=100)
    latitude = fields.CharField(max_length=15)
    longitude = fields.CharField(max_length=15)
    location = fields.CharField(max_length=100)
    imageUrl =fields.CharField(max_length=200)
    takeOff = fields.CharField(max_length=50)
    

launch_Pydantic = pydantic_model_creator(Launch, name="launchPydantic")
launch_pydantic_in = pydantic_model_creator(Launch, name="launchPydanticIn", exclude=('id',))
