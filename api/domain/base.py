import typing

from pydantic import BaseModel


class DomainModel(BaseModel):
    def model_update(self, data: typing.Mapping[str, typing.Any]) -> typing.Self:
        """Update model's fields with given data in-place.

        Returns:
            Updated model.
        """

        update = self.model_dump()
        update.update(data)
        for k, v in self.model_validate(update).model_dump(exclude_defaults=True).items():
            setattr(self, k, v)
        return self
