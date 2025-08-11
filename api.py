import structlog
from ninja import NinjaAPI
from .auth import auth_router
from .articles import articles_router
from .comments import comments_router

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

api = NinjaAPI(title="Блог API", version="1.0.0")

api.add_router("/auth/", auth_router)
api.add_router("/articles/", articles_router)
api.add_router("/", comments_router)