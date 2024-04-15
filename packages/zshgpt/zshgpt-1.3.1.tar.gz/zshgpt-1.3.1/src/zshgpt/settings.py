import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type

from pydantic import model_validator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

JSON_PATH: Path = Path('~/.zshgpt/config.json').expanduser()


class JsonConfigSettingsSource(
    PydanticBaseSettingsSource
):  # Copied form https://docs.pydantic.dev/latest/concepts/pydantic_settings/#adding-sources
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        if not JSON_PATH.exists():
            return None, field_name, False
        encoding = self.config.get('env_file_encoding')
        file_content_json = json.loads(JSON_PATH.read_text(encoding))
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    model: str = 'gpt-3.5-turbo'
    assistant_name: str = 'ZSHGPT'
    assistant_id: Optional[str] = None
    thread_id: Optional[str] = None

    @model_validator(mode='after')
    def update_json(self) -> 'Settings':
        if not JSON_PATH.exists():
            JSON_PATH.parent.mkdir(parents=True, exist_ok=False)
        with open(JSON_PATH, 'w') as f:
            f.write(self.model_dump_json(indent=4))
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
        )


settings = Settings()
