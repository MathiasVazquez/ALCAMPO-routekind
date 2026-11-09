from typing import Any
from django.core.exceptions import ValidationError
from django.db import models
from geopy.geocoders import Nominatim
from datetime import datetime

from kind.custom_fields.crypted_json_field import CryptedJSONField


class CoordsJSONField(CryptedJSONField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.track_address = kwargs.pop('track_address', True)
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        if not isinstance(value, dict):
            raise ValidationError("The value must be an object.")

        if 'latlng' not in value:
            raise ValidationError("'latlng' property is required.")

        # Validar que 'latlng' es una lista de floats
        latlng = value['latlng']
        if (
            not isinstance(latlng, list) or
            not all(isinstance(item, float) for item in latlng) or
            len(latlng) != 2
        ):
            raise ValidationError("'latlng' property must be a list of two floats.")

        return super().clean(value, model_instance)

    def pre_save(self, model_instance: models.Model, add: bool) -> Any:
        new_coords = super().pre_save(model_instance, add)
        if new_coords is None:
            return None

        new_latlng = new_coords.get("latlng", None)
        new_address = new_coords.get("address", None)

        if not add:
            old_coords = self.get_old_info(model_instance)
            if CoordsJSONField.are_same_coords(new_coords, old_coords):
                old_coords['lastUpdate'] = datetime.now().isoformat()
                return old_coords

        if new_latlng is not None:
            return self.get_info_by_latlng(new_latlng)

        return self.get_info_by_address(new_address)

    def get_old_info(self, model_instance):
        current_instance = type(model_instance).objects.filter(pk=model_instance.pk).first()
        encrypted_data = getattr(current_instance, self.attname) if current_instance else None
        return self.decrypt_data(encrypted_data)

    def get_info_by_latlng(self, new_latlng: list):
        if not new_latlng or not all(new_latlng):
            return None

        new_coords = {
            "latlng": new_latlng,
            "address": None,
            "formatedAddress": None,
            "addressType": None,
            "lastUpdate": datetime.now().isoformat(),
        }

        if not self.track_address:
            return new_coords

        # Get new geolocation information
        print("#### using Nominatim!")
        geolocator = Nominatim(user_agent="kindV2SuperAwesomeAppGeocoder")
        location = geolocator.reverse((new_latlng[0], new_latlng[1]), exactly_one=True)
        if location is None:
            raise ValidationError(f"Coordinates latlng [{new_latlng[0]}, {new_latlng[1]}] not found")

        _address = location.address.replace("Paraguay / Paraguái", "Paraguay")

        return {
            **new_coords,
            "address": _address,
            "formatedAddress": _address,
            "addressType": location.raw.get('type'),
            "raw": location.raw.get("address", None) if location.raw else None
        }

    def get_info_by_address(self, address: str):
        if not address:
            return None

        geolocator = Nominatim(user_agent="kindV2AwesomeAppGeocoder")
        try:
            location = geolocator.geocode(address, exactly_one=True)
            if location is None:
                raise ValidationError({"coords": f"Address '{address}' not found"})
        except:
            raise ValidationError({"coords": f"Address '{address}' not found"})

        new_coords = {
            "latlng": [location.latitude, location.longitude],
            "address": address,
            "addressType": location.raw.get('type'),
            "lastUpdate": datetime.now().isoformat(),
            "formatedAddress": location.address.replace("Paraguay / Paraguái", "Paraguay"),
        }

        raw = location.raw.get('address', {})
        raw["country"] = raw.get("country", "").replace("Paraguay / Paraguái", "Paraguay")
        raw["countryCode"] = raw.get("country_code")
        raw.pop("country_code", None)  # Elimina country_code si existe
        new_coords["raw"] = raw

        return new_coords

    @classmethod
    def are_same_coords(cls, coords1: dict, coords2: dict):
        if not coords1 or not coords2:
            return False

        latlng1 = coords1.get('latlng')
        latlng2 = coords2.get('latlng')
        if latlng1 and latlng2:
            return latlng1[0] == latlng2[0] and latlng1[1] == latlng2[1]

        address1 = coords1.get('address')
        address2 = coords2.get('address')
        if address1 and address2:
            return address1 == address2

        return False
