from typing import Dict, Optional

from pydantic import BaseModel


class Resource(BaseModel):
    num_cpus: Optional[int]
    num_gpus: Optional[int]
    num_gpus_per_node: Optional[int]
    max_bundle_gpus: Optional[int]
    gpu_label: Optional[str]
    cpu_gpu_multiple: Optional[int]
    extra: Optional[Dict] = {}


class JobConf(BaseModel):
    job_id: str
    driver_name: str = ""
    resource_name: str
    env_name: str
    arguments: Optional[Dict] = {}
    environment_variables: Optional[Dict] = {}
    resource: Optional[Resource] = None

    entrypoint_path: Optional[str] = ""
    ray_address: Optional[str] = ""
    env_path: Optional[str] = ""


class TaskConf(BaseModel):
    environment_variables: Optional[Dict] = {}
    arguments: Optional[Dict] = {}
