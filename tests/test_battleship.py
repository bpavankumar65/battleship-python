from turtle import position
import unittest

from torpydo.battleship import parse_position, validate_ship_in_field, validate_no_gap, validate_correct_size, initialize_enemyFleet
from torpydo.ship import Position, Ship, Color, Letter

class TestBattleship(unittest.TestCase):
    def test_parse_position_true(self):
        self.assertTrue(parse_position("A1"))


    def test_valid_position(self):
        ship = Ship("", 3, 4)

        ship.add_position("A1")
        ship.add_position("B1")
        ship.add_position("C1")

        assert validate_ship_in_field(ship)

        ship = Ship("", 3, Color.RED)

        ship.add_position("A0")
        ship.add_position("B1")
        ship.add_position("C1")

        assert not validate_ship_in_field(ship)

    def test_no_gap(self):
        positions = [
            Position(Letter.A, 1),
            Position(Letter.A, 2),
            Position(Letter.A, 3),
        ]

        assert validate_no_gap(positions)

        positions = [
            Position(Letter.A, 1),
            Position(Letter.B, 1),
        ]

        assert validate_no_gap(positions)

        positions = [
            Position(Letter.A, 3),
            Position(Letter.A, 1),
            Position(Letter.A, 2),
        ]
        assert validate_no_gap(positions)

        positions = [
            Position(Letter.A, 1),
            Position(Letter.A, 2),
            Position(Letter.A, 4),
        ]

        assert not validate_no_gap(positions)

        positions = [
            Position(Letter.C, 1),
            Position(Letter.A, 2),
        ]

        assert not validate_no_gap(positions)

    def test_correct_size(self):
        ship = Ship("", 2, Color.ORANGE)
        ship.add_position("C1")
        ship.add_position("C2")

        assert validate_correct_size(ship)

        ship = Ship("", 2, Color.ORANGE)
        ship.add_position("C1")

        assert not validate_correct_size(ship)


    def test_initialize_enemyFleet(self):
        initialize_enemyFleet()

if '__main__' == __name__:
    unittest.main()
