import pydantic

class Dog:
    def __init__(self, name):
        self.name = name

class Model(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    pet: Dog

dog_obj = Dog("小白")
m = Model(pet=dog_obj)
json_data = m.model_dump_json()
new_dog_obj = Model.model_validate_json(json_data).pet