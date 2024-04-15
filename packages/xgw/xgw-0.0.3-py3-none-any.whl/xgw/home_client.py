from enum import IntEnum

from .gw_client import GatewayClient, GatewaySemaphore
from .model import *


class Device:
    def __init__(self, did, mac, name, zone):
        self.did = did
        self.mac = mac
        self.name = name
        self.zone = zone


class HomeClient:
    def __init__(self):
        self._gw_client = GatewayClient()
        self._gw_client.on_message = self._on_gw_message
        self._gw_client.on_close = self._on_gw_close
        self.entities = []
        self.scenes = []

    def open(self, ip: str, password: str):
        self._gw_client.open(ip, password)
        self.get_home()

    def close(self):
        self._gw_client.close()

    def set_scene(self, sid: int):
        self._semamphore = GatewaySemaphore()
        self._gw_client.send({"method": "set-scenes", "scenes": [{"sid": sid}]})
        self._semamphore.acquire(2)

    def set_attribute(self, did: int, sid: int, typ: int, value):
        self._semamphore = GatewaySemaphore()
        self._gw_client.send(
            {
                "method": "set-attributes",
                "attributes": [{"did": did, "sid": sid, "type": typ, "value": value}],
            }
        )
        self._semamphore.acquire(2)

    def get_home(self):
        self._semamphore = GatewaySemaphore()
        self._gw_client.send({"method": "get-home"})
        self._semamphore.acquire(5)

    def _on_gw_message(self, message):
        method = message["method"]
        if method == "response":
            if message["client"] == "get-home":
                self.home = message
                self._create_home_model()
            self._semamphore.release()
        elif method == "event-reachable":
            self._on_event_reachable(message["devices"])
        elif method == "event-attributes":
            self._on_event_attributes(message["attributes"])
        elif method == "event-home":
            self.on_home_change()

    def _on_event_reachable(self, devices):
        for device in devices:
            did, reachable = device["did"], device["reachable"]
            for entity in self.entities:
                if entity.did == did:
                    if entity.reachable != reachable:
                        entity.reachable = reachable
                        self.on_reachable_change(entity, reachable)

    def _on_event_attributes(self, attributes):
        for attribute in attributes:

            did, sid, typ, value = (
                attribute["did"],
                attribute["sid"],
                attribute["type"],
                attribute["value"],
            )

            entity = self._find_entity(did, sid)
            if not entity:
                continue

            if typ in attributes_map:
                attr = attributes_map[typ]
                if getattr(entity, attr) != value:
                    setattr(entity, attr, value)
                    self.on_attribute_change(entity, typ, value)
            elif typ == AttrType.HSV:
                hsv = (value["hue"], value["saturation"], value["brightness"])
                if entity._hsv != hsv:
                    entity._hsv = hsv
                    self.on_attribute_change(entity, typ, hsv)

    def _on_gw_close(self):
        self.on_close()

    def _create_home_model(self):
        self.entities = []
        self.scenes = []

        for device in self.home["devices"]:
            for service in device["services"]:

                did, reachable, zone, service_type, sid = (
                    device["did"],
                    device["reachable"],
                    self._find_zone(device["zid"]),
                    service["type"],
                    service["sid"],
                )
                if service_type in services_map:
                    args = (
                        self,
                        service_type,
                        Device(did, device["mac"], device["name"], zone),
                        sid,
                        service["attributes"],
                        reachable,
                    )
                    self.entities.append(services_map[service_type](*args))

        for scene in self.home["scenes"]:
            sid = scene["sid"]
            self.scenes.append(Scene(self, scene["name"], sid))

    def _find_entity(self, did, sid):
        for entity in self.entities:
            if entity.did == did and entity.sid == sid:
                return entity
        return None

    def _find_zone(self, zid):
        for zone in self.home["zones"]:
            if zone["zid"] == zid:
                return zone["name"]
        return "null"


class Scene:
    def __init__(self, client, name, sid):
        self._client = client
        self.name = name
        self.sid = sid

    def set(self):
        self._client.set_scene(self.sid)


class Entity:
    def __init__(self, typ, client, device, sid, attrs, reachable):
        self.type = typ
        self._client = client
        self.name = device.name
        self.did = device.did
        self.mac = device.mac
        self.zone = device.zone
        self.sid = sid
        self.reachable = reachable

        for attr in attrs:
            typ = attr["type"]
            value = attr["value"] if "value" in attr else None
            if typ in attributes_map:
                setattr(self, attributes_map[typ], value)
            elif typ == AttrType.HSV:
                self._hsv = (value["hue"], value["saturation"], value["brightness"])


class Switch(Entity):
    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, attrs, reachable)

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._onoff = value
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    def toggle(self):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, 2)


class Light(Entity):
    class Mode(IntEnum):
        White = 0x00
        Color = 0x01

    def __init__(self, client, service, device, sid, attrs, reachable):
        super().__init__(service, client, device, sid, attrs, reachable)

        self.supported_modes = []

        for attr in attrs:
            typ = attr["type"]
            if typ == AttrType.COLOR_TEMPERATURE:
                self.supported_modes.append(Light.Mode.White)
            elif typ == AttrType.HSV:
                self.supported_modes.append(Light.Mode.Color)

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._onoff = value
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, value)

    def toggle(self):
        self._client.set_attribute(self.did, self.sid, AttrType.ONOFF, 2)

    @property
    def color_mode(self):
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.LIGHT_MODE, value)
        self._color_mode = value
        self._onoff = True

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._client.set_attribute(self.did, self.sid, AttrType.BRIGHTNESS, value)
        self._brightness = value
        self._color_mode = Light.Mode.White
        self._onoff = True

    @property
    def color_temperature(self):
        return self._color_temperature

    @color_temperature.setter
    def color_temperature(self, value):
        self._client.set_attribute(
            self.did, self.sid, AttrType.COLOR_TEMPERATURE, value
        )
        self._color_temperature = value
        self._color_mode = Light.Mode.White
        self._onoff = True

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, value):
        self._client.set_attribute(
            self.did,
            self.sid,
            AttrType.HSV,
            {"hue": value[0], "saturation": value[1], "brightness": value[2]},
        )
        self._hsv = value
        self._color_mode = Light.Mode.Color
        self._onoff = True


services_map = {
    ServiceType.SWITCH: Switch,
    ServiceType.LIGHT: Light,
}

attributes_map = {
    AttrType.ONOFF: "_onoff",
    AttrType.BRIGHTNESS: "_brightness",
    AttrType.COLOR_TEMPERATURE: "_color_temperature",
    AttrType.LIGHT_MODE: "_color_mode",
}

if __name__ == "__main__":
    client = HomeClient("192.168.31.114", "mxchip-gateway-admin")
    for i in range(100):
        print(f"Connecting")
        client.open()
        print("Connected")
        client.set_scene(13220 + i % 2)
        print("Closing")
        client.close()
        print("Closed")
