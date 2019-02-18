import json
import requests


class Gen3DiscoveryError(Exception):
    pass


class Gen3Discovery:

    def __init__(self, endpoint, auth_provider):
        self._auth_provider = auth_provider
        self._endpoint = endpoint
        self.record = self.Gen3DiscoveryRecord()
        self.stats = self.Gen3DiscoveryStats()
        self.histogram = self.Gen3DiscoveryHistogram()

    def get_prop_names_all(self):
        # TODO: Implementation for get_prop_names_all
        raise NotImplementedError

    def validate_query(self, query_txt):
        # TODO: Implementation for validate_query
        raise NotImplementedError

    def query(self, query_txt, variables=None, first=None, last=None, offset=None, sort_field=None, sort_order=None):
        # TODO: Implementation for query
        raise NotImplementedError


    class Gen3DiscoveryRecord:
        def get_prop_names(self):
            # TODO: Implementation for get_prop_names
            raise NotImplementedError

        def query(self, root_node, record_props, first=None, last=None, offset=None, sort_field=None, sort_order=None):
            # TODO: Implementation for query
            raise NotImplementedError


    class Gen3DiscoveryStats:
        def get_prop_names(self):
            # TODO: Implementation for get_prop_names
            raise NotImplementedError
        
        def query(self, root_node, record_props, first=None, last=None, offset=None, sort_field=None, sort_order=None):
            # TODO: Implementation for query
            raise NotImplementedError


    class Gen3DiscoveryHistogram:
        def get_prop_names(self):
            # TODO: Implementation for get_prop_names
            raise NotImplementedError
        
        def query(self, root_node, record_props, first=None, last=None, offset=None, sort_field=None, sort_order=None):
            # TODO: Implementation for query
            raise NotImplementedError
