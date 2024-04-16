from typing import Type
from unittest import TestCase
from src.aero_svo_api import models
from . import payload


class TestModels(TestCase):
    def _compare_model_with_dump(self,
                                 payload: Type[payload.Payload],
                                 model: Type[models.Base],
                                 exclude_fields: set[str] = None
                                 ):
        """
        :param payload: Valid payload pydantic model
        :param model: Testing pydantic model
        :param exclude_fields: Set of undeclared (directly) aliases of fields in testing models
        :return:
        """
        valid_response = payload().model_dump_json(warnings=False)
        valid_model = payload.model_validate_json(valid_response)
        model_dump = model.model_validate_json(valid_response).model_dump(by_alias=True)

        for field, value in valid_model:
            if value is not None and field not in (exclude_fields or set()):
                with self.subTest(field=field, value=value):
                    self.assertIsNotNone(model_dump.get(field))

    def test_aircraft_on_valid(self):
        self._compare_model_with_dump(payload.AircraftPayload, models.Aircraft)

    def test_country_on_valid(self):
        self._compare_model_with_dump(payload.CountryPayload, models.Country)

    def test_city_on_valid(self):
        self._compare_model_with_dump(payload.CityPayload, models.City)

    def test_airport_on_valid(self):
        self._compare_model_with_dump(
            payload.AirportPayload,
            models.Airport,
            exclude_fields={'region', 'country', 'city_eng', 'timezone'}
        )

    def test_company_on_valid(self):
        self._compare_model_with_dump(payload.CompanyPayload, models.Company)

    def test_flight_on_valid(self):
        self._compare_model_with_dump(
            payload.FlightPayload,
            models.Flight,
            exclude_fields={'aircraft_type_id', 'aircraft_type_name', 'term_gate', 'old_term_gate'}
        )
