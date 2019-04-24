#!/usr/bin/env python

from gillham import gillham


def print_tables():
	table = _get_table()
	for i in range(4):
		_write_table(i, table)


def _write_table(number, table):
	array_of_bytes = []
	for row in table:
		array_of_bytes.append(_get_row_byte(row, number))

	to_write = bytearray(array_of_bytes)
	file_name = "dial{}.bin".format(number)
	with open(file_name, "w+") as f:
		f.write(to_write)


def _get_row_byte(row, number):
	return row[1][3 - number]

def _get_table():
	gillham_codes = list(range(2048))
	segment_codes = []

	for i in gillham_codes:
		altitude = gillham(i)
		if altitude == -975:
			altitude = -1000
		if altitude == -950:
			altitude == -900
		if altitude:
			altitude /= 100

		segment_codes.append(_altitude_to_7_segments(altitude))

	return zip(gillham_codes, segment_codes)


def _altitude_to_7_segments(altitude):
	minus = 0b10111111
	dial_numbers = [
		0b11000000,
		0b11111001,
		0b10100100,
		0b10110000,
		0b10011001,
		0b10010010,
		0b10000010,
		0b11111000,
		0b10000000,
		0b10010000,
	]
	turned_off = 0xff

	dials = [turned_off for i in range(4)]
	if altitude:
		if altitude < 0:
			dials[1] = minus
			altitude *= -1

		numbers = str(altitude)
		for i, n in enumerate(numbers):
			i += 4 - len(numbers)
			dials[i] = dial_numbers[int(n)]

	return dials
