from apiflask import APIBlueprint

api_v1 = APIBlueprint('api_v1', __name__)

from co2.api.v1 import resources
