from workers.gearman import JSONGearmanClient as GearmanClient

gm_client = GearmanClient(["localhost:4730"])
