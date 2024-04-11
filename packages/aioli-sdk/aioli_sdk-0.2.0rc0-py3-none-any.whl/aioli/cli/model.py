# © Copyright 2023-2024 Hewlett Packard Enterprise Development LP
from argparse import Namespace
from typing import Any, Dict, List

from pydantic import StrictInt

import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.cli.registry import lookup_registry_name_by_id
from aioli.common import api
from aioli.common.api import authentication
from aioli.common.api.errors import NotFoundException, VersionRequiredException
from aioli.common.declarative_argparse import Arg, ArgsDescription, Cmd, Group
from aiolirest.models.configuration_resources import ConfigurationResources
from aiolirest.models.deployment_model_version import DeploymentModelVersion
from aiolirest.models.packaged_model import PackagedModel
from aiolirest.models.packaged_model_request import PackagedModelRequest
from aiolirest.models.resource_profile import ResourceProfile


@authentication.required
def list_models(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        response = api_instance.models_get()

    registries_api = aiolirest.RegistriesApi(session)

    if args.json:
        format_json(response, registries_api)
    else:
        format_models(response, args, registries_api)


def format_json(response: List[PackagedModel], registries_api: aiolirest.RegistriesApi) -> None:
    models = []
    for m in response:
        # Don't use the m.to_json() method as it adds backslash escapes for double quote
        d = m.to_dict()
        d.pop("id")
        d.pop("modifiedAt")
        rname = lookup_registry_name_by_id(m.registry, registries_api)
        d["registry"] = rname
        models.append(d)

    render.print_json(models)


def format_models(
    response: List[PackagedModel], args: Namespace, registries_api: aiolirest.RegistriesApi
) -> None:
    def format_model(e: PackagedModel, reg_api: aiolirest.RegistriesApi) -> List[Any]:
        rname = lookup_registry_name_by_id(e.registry, reg_api)
        result = [
            e.name,
            e.description,
            e.version,
            e.url,
            e.image,
            rname,
        ]
        return result

    headers = [
        "Name",
        "Description",
        "Version",
        "URI",
        "Image",
        "Registry",
    ]
    values = [format_model(r, registries_api) for r in response]
    render.tabulate_or_csv(headers, values, args.csv)


def construct_environment(args: Namespace) -> Dict[str, str]:
    environment: Dict[str, str] = {}
    if args.env is None:
        return environment

    for entry in args.env:
        # split to name & value
        the_split = entry.split("=", maxsplit=1)
        name: str = the_split[0]
        value: str = ""
        if len(the_split) > 1:
            value = the_split[1]
        environment[name] = value
    return environment


def construct_arguments(args: Namespace) -> List[str]:
    arguments: List[str] = []
    if args.arg is None:
        return arguments

    for entry in args.arg:
        arguments.append(entry.strip())
    return arguments


@authentication.required
def create(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        requests = ResourceProfile(
            cpu=args.requests_cpu, gpu=args.requests_gpu, memory=args.requests_memory
        )
        limits = ResourceProfile(
            cpu=args.limits_cpu, gpu=args.limits_gpu, memory=args.limits_memory
        )
        resources = ConfigurationResources(gpuType=args.gpu_type, requests=requests, limits=limits)
        r = PackagedModelRequest(
            name=args.name,
            description=args.description,
            url=args.url,
            image=args.image,
            registry=args.registry,
            resources=resources,
            environment=construct_environment(args),
            modelFormat=args.format,
            arguments=construct_arguments(args),
        )
        api_instance.models_post(r)


def lookup_model(name: str, api: aiolirest.PackagedModelsApi) -> PackagedModel:
    model = None
    for r in api.models_get():
        if r.name == name:
            if model is not None:
                raise VersionRequiredException(
                    f"please specify model version as {name} matches more than one model"
                )
            model = r

    if model is None:
        raise NotFoundException(f"model {name} not found")
    return model


def lookup_model_and_version(
    name: str, version: int, api: aiolirest.PackagedModelsApi
) -> PackagedModel:
    for r in api.models_get():
        if r.name == name and r.version == StrictInt(version):
            return r
    raise NotFoundException(f"model {name} version {version} not found")


@authentication.required
def show_model(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)

    if args.version:
        model = lookup_model_and_version(args.name, args.version, api_instance)
    else:
        model = lookup_model(args.name, api_instance)

    registries_api = aiolirest.RegistriesApi(session)

    rname = lookup_registry_name_by_id(model.registry, registries_api)

    d = model.to_dict()
    d["registry"] = rname

    if args.json:
        render.print_json(d)
    else:
        print(render.format_object_as_yaml(d))


@authentication.required
def update(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        if args.version:
            found = lookup_model_and_version(args.modelname, args.version, api_instance)
        else:
            found = lookup_model(args.modelname, api_instance)
        request = PackagedModelRequest(
            description=found.description,
            image=found.image,
            name=found.name,
            registry=found.registry,
            url=found.url,
            arguments=found.arguments,
            resources=found.resources,
            environment=found.environment,
            modelFormat=found.format,
        )

        if (
            request.resources is None
            or request.resources.requests is None
            or request.resources.limits is None
        ):
            # Not likely, but testing these prevents complaints from mypy
            raise api.errors.BadResponseException("Unexpected null result")

        if args.name is not None:
            request.name = args.name

        if args.description is not None:
            request.description = args.description

        if args.url is not None:
            request.url = args.url

        if args.image is not None:
            request.image = args.image

        if args.registry is not None:
            request.registry = args.registry

        if args.format is not None:
            request.format = args.format

        if args.requests_cpu is not None:
            request.resources.requests.cpu = args.requests_cpu

        if args.requests_memory is not None:
            request.resources.requests.memory = args.requests_memory

        if args.requests_gpu is not None:
            request.resources.requests.gpu = args.requests_gpu

        if args.limits_cpu is not None:
            request.resources.limits.cpu = args.limits_cpu

        if args.limits_memory is not None:
            request.resources.limits.memory = args.limits_memory

        if args.limits_gpu is not None:
            request.resources.limits.gpu = args.limits_gpu

        if args.gpu_type is not None:
            request.resources.gpu_type = args.gpu_type

        if args.env is not None:
            request.environment = construct_environment(args)

        if args.arg is not None:
            request.arguments = construct_arguments(args)

        headers = {"Content-Type": "application/json"}

        assert found.id is not None
        api_instance.models_id_put(found.id, request, _headers=headers)


@authentication.required
def delete_model(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        found = lookup_model_and_version(args.name, args.version, api_instance)

        assert found.id is not None
        api_instance.models_id_delete(found.id)


@authentication.required
def auth_token(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        found = lookup_model(args.name, api_instance)
        assert found.id is not None
        response = api_instance.models_id_token_get(found.id)
    t = response.to_dict()
    print(render.format_object_as_yaml(t))


@authentication.required
def list_versions(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.PackagedModelsApi(session)
        if args.version:
            found = lookup_model_and_version(args.name, args.version, api_instance)
        else:
            found = lookup_model(args.name, api_instance)
        assert found.id is not None
        response = api_instance.models_versions_get(found.id)

    def format_versions(e: DeploymentModelVersion) -> List[Any]:
        result = [
            e.deployed,
            e.native_app_name,
            e.model,
            e.mdl_version,
        ]
        return result

    headers = [
        "Deployed",
        "Native App Name",
        "Model",
        "Model\nVersion",
    ]

    values = [format_versions(r) for r in response]
    render.tabulate_or_csv(headers, values, args.csv)


common_model_args: ArgsDescription = [
    Arg("--description", help="Description of the packaged model"),
    Arg("--url", help="Reference within the specified registry"),
    Arg("--registry", help="The name or ID of the packaged model registry"),
    Arg(
        "--format",
        "--modelformat",
        help="Model format for downloaded models (bento-archive, openllm, nim, unspecified)",
    ),
    Arg(
        "-a",
        "--arg",
        help="Argument to be added to the service command line. "
        "If specifying an argument that starts with a '-', use the form --arg=<your-argument>",
        action="append",
    ),
    Arg(
        "-e",
        "--env",
        help="Specifies an environment variable & value as name=value, "
        "to be passed to the launched container",
        action="append",
    ),
    Arg("--gpu-type", help="GPU type required"),
    Arg("--limits-cpu", help="CPU limit"),
    Arg("--limits-memory", help="Memory limit"),
    Arg("--limits-gpu", help="GPU limit"),
    Arg("--requests-cpu", help="CPU request"),
    Arg("--requests-memory", help="Memory request"),
    Arg("--requests-gpu", help="GPU request"),
]

main_cmd = Cmd(
    "m|odel",
    None,
    "manage packaged models",
    [
        # Inspection commands.
        Cmd(
            "list ls",
            list_models,
            "list packaged models",
            [
                Arg("--csv", action="store_true", help="print as CSV"),
                Arg("--json", action="store_true", help="print as JSON"),
            ],
            is_default=True,
        ),
        # Create command.
        Cmd(
            "create",
            create,
            "create a packaged model",
            [
                Arg(
                    "name",
                    help="The name of the packaged model. Must begin with a letter, but may "
                    "contain letters, numbers, underscore, and hyphen",
                ),
                Arg("--image", help="Docker container image servicing the packaged model"),
            ]
            + common_model_args,
        ),
        # Show command.
        Cmd(
            "show",
            show_model,
            "show a packaged model",
            [
                Arg(
                    "name",
                    help="The name of the packaged model.",
                ),
                Group(
                    Arg("--yaml", action="store_true", help="print as YAML", default=True),
                    Arg("--json", action="store_true", help="print as JSON"),
                ),
                Arg("--version", help="The packaged model version to show"),
            ],
        ),
        # Update command
        Cmd(
            "update",
            update,
            "modify a packaged model",
            [
                Arg("modelname", help="The name of the packaged model"),
                Arg(
                    "--name",
                    help="The new name of the packaged model. Must begin with a letter, but may "
                    "contain letters, numbers, underscore, and hyphen",
                ),
                Arg("--image", help="Docker container image servicing the packaged model"),
                Arg("--version", help="The packaged model version to update"),
            ]
            + common_model_args,
        ),
        Cmd(
            "delete",
            delete_model,
            "delete a packaged model",
            [
                Arg("name", help="The name of the packaged model"),
                Arg("version", help="The packaged model version to delete"),
            ],
        ),
        Cmd(
            "token",
            auth_token,
            "get packaged model auth token",
            [
                Arg("name", help="The name of the packaged model"),
            ],
        ),
        Cmd(
            "versions lv",
            list_versions,
            "list of deployment versions for a packaged model",
            [
                Arg("--csv", action="store_true", help="print as CSV"),
                Arg("name", help="The name of the packaged model"),
                Arg("--version", help="The version of the packaged model"),
            ],
        ),
    ],
)

args_description = [main_cmd]  # type: List[Any]
