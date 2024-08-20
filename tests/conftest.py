from datetime import datetime

import pytest
from app.auth.security import hash_password
from app.current_tasks.models import CurrentTask, Status
from app.mentors.models import Mentor
from app.questions.models import Question, QuestionCategory
from app.reports.models import Report
from app.tasks.models import Task, TaskCategory
from app.trainees.models import Trainee
from black.trans import defaultdict
from api.config import CONFIG
from fastapi.testclient import TestClient
from run import create_app
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from tests.auth import DEFAULT_PASSWORD


@pytest.fixture(name="session")
def session() -> Session:
    engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client(monkeypatch) -> TestClient:
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture(name="mentor")
def mentor(session, faker) -> Mentor:
    password = hash_password(DEFAULT_PASSWORD)
    mentor = Mentor(
        name=faker.first_name(),
        surname=faker.last_name(),
        email=faker.email(),
        psw=password,
        superuser=False,
    )
    session.add(mentor)
    session.commit()
    yield mentor


@pytest.fixture(name="trainee")
def trainee(session, faker) -> Trainee:
    trainee = Trainee(
        name=faker.first_name(),
        surname=faker.last_name(),
        start_intership=faker.past_datetime(),
    )
    session.add(trainee)
    session.commit()
    yield trainee


@pytest.fixture(name="trainee_list")
def trainee_list(session, faker, mentor) -> Trainee:
    trainees = []
    for _ in range(5):
        trainee = Trainee(
            mentor_id=mentor.id,
            name=faker.first_name(),
            surname=faker.last_name(),
            nickname_tg=faker.company(),
            start_intership=faker.past_datetime(),
        )
        trainees.append(trainee)
        session.add(trainee)
        session.commit()
    yield trainees


@pytest.fixture(name="task")
def task(session, faker) -> Task:
    task = Task(
        task_name=faker.text(),
        category=TaskCategory.BY_AWS,
        description=faker.sentence(),
        question=faker.sentence(),
        answer=faker.sentence(),
        days=3,
    )
    session.add(task)
    session.commit()
    yield task


@pytest.fixture(name="task_list")
def task_list(session, faker) -> Task:
    tasks = []
    for category in (None, TaskCategory.BY_AWS, TaskCategory.RU_YANDEX):
        for _ in range(3):
            task = Task(
                task_name=faker.text(),
                category=category,
                description=faker.sentence(),
                question=faker.sentence(),
                answer=faker.sentence(),
                days=3,
            )
            tasks.append(task)
            session.add(task)
            session.commit()
    yield tasks


@pytest.fixture(name="current_task")
def current_task(session, faker, trainee, task) -> CurrentTask:
    current_task = CurrentTask(
        task_id=task.id,
        trainee_id=trainee.id,
        status=Status.in_progress,
        deadline=faker.future_datetime(),
    )
    session.add(current_task)
    session.commit()
    yield current_task


@pytest.fixture(name="question_category")
def question_category(session, faker) -> QuestionCategory:
    question_category = QuestionCategory(name=faker.text())
    session.add(question_category)
    session.commit()
    yield question_category


@pytest.fixture(name="question")
def question(session, faker, question_category) -> Question:
    question = Question(category_id=question_category.id, question=faker.sentence())
    session.add(question)
    session.commit()
    yield question


@pytest.fixture(name="question_list")
def question_list(session, faker) -> dict[int, list[Question]]:
    categories = defaultdict(list)
    for _ in range(3):
        category = QuestionCategory(name=faker.text())
        session.add(category)
        session.commit()
        for _ in range(3):
            question = Question(category_id=category.id, question=faker.sentence())
            session.add(question)
            session.commit()
            categories[category.id].append(question)
    yield categories


@pytest.fixture(name="report")
def report(session, faker, mentor, trainee) -> Report:
    report = Report(
        mentor_id=mentor.id,
        trainee_id=trainee.id,
        report=faker.sentence(),
        mark=5.0,
        ready_tasks=5,
        date=datetime.now(),
    )
    session.add(report)
    session.commit()
    yield report, mentor, trainee
