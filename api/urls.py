from tastypie.api import Api

def get_api(version_name):

    api = Api(api_name=version_name)

    return api