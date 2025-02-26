from gunicorn.app.wsgiapp import WSGIApplication as GunicornWSGIApplication


class _WSGIApplication(GunicornWSGIApplication):
    def __init__(
        self,
        app_uri: str,
        options: dict[str, str] | None = None,
    ) -> None:
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def run_server(
    app_uri: str = "app.wsgi",
    options: dict[str, str] | None = None,
) -> None:
    options = options or {"worker_class": "sync", "workers": 1}
    _WSGIApplication(app_uri, options).run()
