name = "Workshop PC heartbeat"    # Friendly display name
unique_id = "workshop_pc_heartbeat"    # Technical identifier
period = 20

manufacturer = "Spas Tech"
model = "Heartbeat v1"
class broker:
    host = "192.168.100.70"
    port = 1883
    username = None
    password = None
    use_tls = False
    tls_key = None
    tls_certfile = None
    tls_ca_cert = None
    discovery_prefix = "homeassistant"
    state_prefix = "hmd"
    client = None
