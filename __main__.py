# Copyright 2016-2020, Pulumi Corporation.  All rights reserved.

from typing import Protocol
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, ContainerPortArgs, PodSpecArgs, PodTemplateSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_kubernetes.apps.v1 import Service, ServiceSpecArgs

config = pulumi.Config()

def nginx(config):
    nginxLabels = {"app": "nginx"}
    nginxDeployment = Deployment(
        "nginx-deployment",
        spec=DeploymentSpecArgs(
            selector=LabelSelectorArgs(match_labels=nginxLabels),
            replicas=2 if config.get_int("replicas") is None else config.get_int("replicas"),
            template=PodTemplateSpecArgs(
                metadata=ObjectMetaArgs(labels=nginxLabels),
                spec=PodSpecArgs(
                    containers=[ContainerArgs(
                        name="nginx",
                        image="nginx:1.7.9",
                        ports=[ContainerPortArgs(container_port=80)],
                    )],
                ),
            ),
        ))
    return nginxDeployment

nginxDeployment = nginx(config)
pulumi.export("nginx", nginxDeployment.metadata.apply(lambda m: m.name))

def nginx_svc(config):
    nginxLabels = {"app": "nginx"}
    nginxService = Service(
        "nginx-svc",
        spec=ServiceSpecArgs(
            type="ClusterIP",
            selector=LabelSelectorArgs(match_labels=nginxLabels),
            ports=[ServicePortsSpecArgs(
                name="80-80",
                protocol="TCP",
                port="80",
                targetPort="80",
            )],
        ))
    return nginxService
     
nginxService = nginx_svc(config)
pulumi.export("nginx_svc", nginxDeployment.metadata.apply(lambda m: m.name))
