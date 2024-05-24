from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='test@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_get_session():
    response = next(get_session())
    assert isinstance(response, Session)
