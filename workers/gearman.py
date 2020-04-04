import json
import decimal

import python3_gearman as gearman


class _JSONDataEncoder(gearman.DataEncoder):
    """
        An override Gearman DataEncoder class to send/receive JSON data.
    """
    @classmethod
    def encode(cls, encodable_object):
        encoded = json.dumps(encodable_object)
        return encoded

    @classmethod
    def decode(cls, decodable_string):
        decoded = json.loads(decodable_string)
        return decoded


class JSONGearmanClient(gearman.GearmanClient):
    """
       Extend gearman.GearmanClient with our _JSONDataEncoder
    """
    data_encoder = _JSONDataEncoder


class JSONGearmanWorker(gearman.GearmanWorker):
    """
    Extend gearman.GearmanWorker with our _JSONDataEncoder
    """
    data_encoder = _JSONDataEncoder
