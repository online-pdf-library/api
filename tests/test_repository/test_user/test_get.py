import uuid

from api import domain
from api.repository.user import UserRepository
from tests import factories


async def test_user_retrieved_by_id_successfully(user_repository: UserRepository) -> None:
    db_user = await factories.UserFactory.create()

    user = await user_repository.get(domain.UserGetFilter(id=db_user.id))

    assert user is not None
    assert db_user.to_dict() == user.model_dump()


async def test_user_retrieved_by_email_successfully(user_repository: UserRepository) -> None:
    db_user = await factories.UserFactory.create()

    user = await user_repository.get(domain.UserGetFilter(email=db_user.email))

    assert user is not None
    assert db_user.to_dict() == user.model_dump()


async def test_none_returned_for_unexisting_id_successfully(
    user_repository: UserRepository,
) -> None:
    await factories.UserFactory.create()

    user = await user_repository.get(domain.UserGetFilter(id=uuid.uuid4()))

    assert user is None


async def test_none_returned_for_unexisting_email_successfully(
    user_repository: UserRepository,
) -> None:
    await factories.UserFactory.create()

    user = await user_repository.get(domain.UserGetFilter(email=str(uuid.uuid4())))

    assert user is None
