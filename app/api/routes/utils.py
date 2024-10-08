from app.api.deps import get_current_active_superuser
from app.users.models import Message
from app.utils.emails import generate_test_email, send_email
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")
