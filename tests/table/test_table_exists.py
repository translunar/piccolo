import asyncio
from unittest import TestCase

from ..example_project.tables import Pokemon


class TestTableExists(TestCase):

    def setUp(self):
        asyncio.run(Pokemon.create().run())

    def test_table_exists(self):
        response = asyncio.run(Pokemon.table_exists().run())
        self.assertTrue(response is True)

    def tearDown(self):
        asyncio.run(Pokemon.drop().run())
