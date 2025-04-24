
def test_backend_starts(page, backend_app):
    page.goto(backend_app.url)

    assert page.title() == 'ILS Labs Experiments Admin'


def test_frontend_starts(page, frontend_app):
    page.goto(frontend_app.url)

    assert page.title() == 'Experimenten ILS Labs'
