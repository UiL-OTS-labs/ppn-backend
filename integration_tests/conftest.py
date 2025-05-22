import email
import glob
import importlib
import os
import random
import re
import requests
import shutil
import string
import subprocess
from collections import namedtuple
from datetime import date

import django
import pytest

from playwright.sync_api import Page, Browser

BACK_PORT = 18000
FRONT_PORT = 19000


class DjangoServerProcess:
    def __init__(self, name, path, port):
        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = "."
        self.name = name
        self.path = path
        self.port = port
        self.settings = f"{name}_settings"
        self.db_conn = None

    def migrate(self):
        # delete existing db
        try:
            os.unlink(f"{self.name}.int.db.sqlite3")
        except FileNotFoundError:
            pass

        cmd = [
            "python",
            "-m",
            "django",
            "migrate",
            "--noinput",
            "--settings",
            self.settings,
        ]
        process = subprocess.run(cmd, env=self.env)

        if process.returncode != 0:
            raise RuntimeError(f"could not migrate app in {self.path}")

    def load(self, path):
        """load a data fixture"""
        cmd = [
            "python",
            "-m",
            "django",
            "loaddata",
            path,
            "--settings",
            self.settings,
        ]
        print(cmd)
        process = subprocess.run(cmd, env=self.env)

        if process.returncode != 0:
            raise RuntimeError(f"could not load data from {path}")

    def start(self):
        cmd = [
            "python",
            "-m",
            "django",
            "runserver",
            str(self.port),
            "--settings",
            self.settings,
        ]
        self.process = subprocess.Popen(cmd, env=self.env)
        for attempt in range(5):
            try:
                requests.get(self.url)
                # server is ready and answering requests
                break
            except requests.ConnectionError:
                # server isn't ready, keep trying
                pass

            try:
                self.process.wait(1)
            except subprocess.TimeoutExpired:
                # this is good, the process is still running
                pass

        if self.process.returncode is not None:
            raise RuntimeError(f"could not start app in {self.path}")

    def shutdown(self):
        if self.db_conn:
            self.db_conn.close()
        self.process.terminate()

    @property
    def url(self):
        return f"http://localhost:{self.port}/"

    def get_model(self, app_name: str, model: str):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.settings
        django.setup()
        from django.db import connection
        self.db_conn = connection
        module = importlib.import_module(f'{app_name}.models')
        return module.__dict__[model]


@pytest.fixture(scope="module")
def backend_app():
    server = DjangoServerProcess("backend", "../backend", BACK_PORT)
    server.migrate()
    server.start()
    yield server
    server.shutdown()


@pytest.fixture(scope="module")
def frontend_app():
    server = DjangoServerProcess("frontend", "../frontend", FRONT_PORT)
    server.migrate()
    server.start()
    yield server
    server.shutdown()


@pytest.fixture(scope="module")
def apps(backend_app, frontend_app):
    return namedtuple("Apps", "backend,frontend")(backend_app, frontend_app)


def set_language_english(page):
    loc = page.locator("button").get_by_text("English")
    if loc.count():
        loc.click()


@pytest.fixture
def as_admin(browser: Browser, backend_app):
    backend_app.load("admin")
    context = browser.new_context()
    page_admin = context.new_page()
    page_admin.goto(backend_app.url + '/login')
    set_language_english(page_admin)
    page_admin.click('#djHideToolBarButton')
    page_admin.fill("#id_username", "admin")
    page_admin.fill("#id_password", "admin")
    page_admin.locator('button').get_by_text("Log in").click()
    return page_admin


def read_mail(address):
    messages = []
    for path in sorted(glob.glob(EMAIL_FILE_PATH + "/*")):
        # filename includes timestamp, so sorting by name also sorts by time
        with open(path) as f:
            msg = email.message_from_file(f)
            if msg["To"] == address:
                messages.append(msg)

    return messages


@pytest.fixture
def mailbox():
    yield read_mail
    # delete emails
    shutil.rmtree(EMAIL_FILE_PATH, ignore_errors=True)


@pytest.fixture(scope="function", autouse=True)
def _dj_autoclear_mailbox() -> None:
    # Override the `_dj_autoclear_mailbox` test fixture in `pytest_django`.
    pass


@pytest.fixture
def link_from_mail(mailbox):

    def _delegate(email: str, subject=None):
        for message in mailbox(email):
            if subject is None or subject in message['subject']:
                html = message.get_payload()[1].get_payload()
                # find link in email
                link = re.search(r'<a href="([^"]+)"', html).group(1)
                return link

    return _delegate
