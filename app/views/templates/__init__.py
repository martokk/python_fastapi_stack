from datetime import datetime

from fastapi.templating import Jinja2Templates

from app import paths
from app.models.settings import Settings as _Settings
from app.views.templates.filters import filter_humanize

settings = _Settings()  # type: ignore


def get_templates() -> Jinja2Templates:
    """
    Create Jinja2Templates object and add global variables to templates.

    Returns:
        Jinja2Templates: Jinja2Templates object.
    """
    # Create Jinja2Templates object
    templates = Jinja2Templates(directory=paths.TEMPLATES_PATH)

    # Add custom filters to templates
    templates.env.filters["humanize"] = filter_humanize

    # Add global variables to templates
    templates.env.globals["PROJECT_NAME"] = settings.PROJECT_NAME
    templates.env.globals["ENV_NAME"] = settings.ENV_NAME
    templates.env.globals["PACKAGE_NAME"] = settings.PACKAGE_NAME
    templates.env.globals["PROJECT_DESCRIPTION"] = settings.PROJECT_DESCRIPTION
    templates.env.globals["BASE_DOMAIN"] = settings.BASE_DOMAIN
    templates.env.globals["BASE_URL"] = settings.BASE_URL
    templates.env.globals["VERSION"] = settings.VERSION
    templates.env.globals["current_year"] = datetime.now().year

    # Override the TemplateResponse to include request state context
    original_template_response = templates.TemplateResponse

    def template_response(name, context, *args, **kwargs):
        request = context.get("request")
        if request and hasattr(request.state, "template_context"):
            context.update(request.state.template_context)
        return original_template_response(name, context, *args, **kwargs)

    templates.TemplateResponse = template_response

    return templates
