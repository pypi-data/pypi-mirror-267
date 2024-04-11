"""config module for moop."""

from pathlib import Path

# import click
from dynaconf import Dynaconf
# from dynaconf import ValidationError
# from dynaconf import Validator

settings = Dynaconf(
    envvar_prefix='MOOP',
    settings_files=list(Path('configs').glob('**/*.yaml')),
    DEBUG=False,
)

# settings.validators.register(
#     Validator('TIMESTAMP_FORMANT', must_exist=True),
#     Validator('SERVER.HOST', must_exist=True),
#     Validator('SERVER.PORT', must_exist=True),
#     Validator('OUTPUT_RUN', must_exist=True),
#     Validator('OUTPUT_TMP', must_exist=True),
#     Validator('STATIC_ZIP', must_exist=True),
# )
#
# try:
#     settings.validators.validate_all()
# except ValidationError as e:
#     accumulative_errors = e.details
#     click.echo(e)
#     exit(-1)
