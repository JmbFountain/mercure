"""
types.py
========
Definitions for using TypedDicts throughout mercure.
"""

# Standard python includes
from typing import Any, Dict, List, Optional, Union, cast
from typing_extensions import Literal, TypedDict
from pydantic import BaseModel, create_model_from_typeddict
import daiquiri

# import traceback

logger = daiquiri.getLogger("test")


# TODO: Add description for the individual classes


class Compat:
    def get(self, item, els=None) -> Any:
        # logger.info(repr(traceback.format_stack()[-2].splitlines()[1]))
        return self.__dict__.get(item, els) or els


class EmptyDict(TypedDict):
    pass


class Target(BaseModel, Compat):
    target_type: Literal["dicom"] = "dicom"
    ip: Optional[str] = ""
    port: Optional[str] = ""
    aet_target: Optional[str] = ""
    aet_source: Optional[str] = ""
    contact: Optional[str] = ""
    comment: str = ""


class Module(BaseModel, Compat):
    docker_tag: Optional[str] = ""
    additional_volumes: Optional[str] = ""
    environment: Optional[str] = ""
    docker_arguments: Optional[str] = ""
    server_group: Optional[str] = ""
    settings: Dict[str, Any] = {}
    contact: Optional[str] = ""
    comment: str = ""


class UnsetRule(TypedDict):
    rule: str


class Rule(BaseModel, Compat):
    rule: str = "False"
    target: str = ""
    disabled: Literal["True", "False"] = "False"
    fallback: Literal["True", "False"] = "False"
    contact: str = ""
    comment: str = ""
    tags: str = ""
    action: Literal["route", "both", "process", "discard", "notification"] = "route"
    action_trigger: Literal["series", "study"] = "series"
    study_trigger_condition: Literal["timeout", "received_series"] = "timeout"
    study_trigger_series: str = ""
    priority: Literal["normal", "urgent", "offpeak"] = "normal"
    processing_module: str = ""
    processing_settings: Dict[str, Any] = {}
    notification_webhook: str = ""
    notification_payload: str = ""
    notification_trigger_reception: Literal["True", "False"] = "False"
    notification_trigger_completion: Literal["True", "False"] = "False"
    notification_trigger_error: Literal["True", "False"] = "False"


class Config(BaseModel, Compat):
    appliance_name: str
    port: int
    incoming_folder: str
    studies_folder: str
    outgoing_folder: str
    success_folder: str
    error_folder: str
    discard_folder: str
    processing_folder: str
    router_scan_interval: int  # in seconds
    dispatcher_scan_interval: int  # in seconds
    cleaner_scan_interval: int  # in seconds
    retention: int  # in seconds (3 days)
    retry_delay: int  # in seconds (15 min)
    retry_max: int
    series_complete_trigger: int  # in seconds
    study_complete_trigger: int  # in seconds
    study_forcecomplete_trigger: int  # in seconds
    graphite_ip: str
    graphite_port: int
    bookkeeper: str
    offpeak_start: str
    offpeak_end: str
    targets: Dict[str, Target]
    rules: Dict[str, Rule]
    modules: Dict[str, Module]
    process_runner: Literal["docker", "nomad", ""] = ""


class TaskInfo(BaseModel, Compat):
    action: Literal["route", "both", "process", "discard", "notification"]
    uid: str
    uid_type: Literal["series", "study"]
    triggered_rules: Union[Dict[str, Literal[True]], str]
    applied_rule: Optional[str]
    mrn: str
    acc: str
    mercure_version: str
    mercure_appliance: str
    mercure_server: str


class TaskDispatch(BaseModel, Compat):
    target_name: Optional[str]
    target_ip: str
    target_port: str
    target_aet_target: str
    target_aet_source: Optional[str]
    retries: Optional[int]
    next_retry_at: Optional[float]
    series_uid: Optional[str]


class TaskStudy(BaseModel, Compat):
    study_uid: str
    complete_trigger: Optional[str]
    complete_required_series: str
    creation_time: str
    last_receive_time: str
    received_series: Optional[List]
    complete_force: Literal["True", "False"]


class TaskProcessing(BaseModel, Compat):
    module_name: Optional[str]
    module_config: Optional[Module]
    settings: Dict[str, Any] = {}


class Task(BaseModel, Compat):
    info: TaskInfo
    dispatch: Union[TaskDispatch, EmptyDict] = cast(EmptyDict, {})
    process: Union[TaskProcessing, EmptyDict] = cast(EmptyDict, {})
    study: Union[TaskStudy, EmptyDict] = cast(EmptyDict, {})

    class Config:
        extra = "forbid"


class TaskHasStudy(BaseModel, Compat):
    info: TaskInfo
    dispatch: Union[TaskDispatch, EmptyDict] = cast(EmptyDict, {})
    process: Union[Module, EmptyDict] = cast(EmptyDict, {})
    study: TaskStudy
