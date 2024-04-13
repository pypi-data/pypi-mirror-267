import google.protobuf.message
import modal.client
import modal_proto.api_pb2
import typing
import typing_extensions

_Function = typing.TypeVar("_Function")

class _LocalApp:
    tag_to_object_id: typing.Dict[str, str]
    app_id: str
    app_page_url: str
    environment_name: str
    interactive: bool

    def __init__(self, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, environment_name: typing.Union[str, None] = None, interactive: bool = False):
        ...


class _ContainerApp:
    app_id: typing.Union[str, None]
    environment_name: typing.Union[str, None]
    tag_to_object_id: typing.Dict[str, str]
    object_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]
    is_interactivity_enabled: bool
    function_def: typing.Union[modal_proto.api_pb2.Function, None]
    fetching_inputs: bool

    def __init__(self):
        ...


def _reset_container_app():
    ...


_container_app: _ContainerApp

def _init_container_app(items: typing.List[modal_proto.api_pb2.AppGetObjectsItem], app_id: str, environment_name: str = '', function_def: typing.Union[modal_proto.api_pb2.Function, None] = None):
    ...


async def _interact(client: typing.Union[modal.client._Client, None] = None) -> None:
    ...


class __interact_spec(typing_extensions.Protocol):
    def __call__(self, client: typing.Union[modal.client.Client, None] = None) -> None:
        ...

    async def aio(self, *args, **kwargs) -> None:
        ...

interact: __interact_spec


def is_local() -> bool:
    ...
