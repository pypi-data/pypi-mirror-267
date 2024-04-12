# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
# type: ignore
import unittest
import pya

from pdkmaster.io import klayout as _kl

from ...dummy import dummy_layoutfab, dummy_gdslayers

class PCellTest(unittest.TestCase):
    def test_pcell(self):
        # Run the library generation for code coverage

        # Generate library
        _kl.PCellLibrary(name="PCells", layoutfab=dummy_layoutfab, gds_layers=dummy_gdslayers)

        # Generate some actual layouts
        pya_layout = pya.Layout()

        pya_layout.create_cell("nmos", "PCells", {})
        pya_layout.create_cell("nmos", "PCells", {"_w": 0.0, "_l": 0.0})

        pya_layout.create_cell("pmos$fingers", "PCells", {"_w": 2.0, "fingers": 3})
        pya_layout.create_cell("pmos$fingers", "PCells", {"_w": 0.0, "_l": 0.0})

        chs = pya_layout.create_cell("contact$array", "PCells", {})
        pya_layout.create_cell("via$array", "PCells", {"_enct": 1})
        pya_layout.create_cell(
            "via$array", "PCells",
            {"_enct": 2, "_padw": 2.0, "_padh": 2.0, "_mins": False, "_space": 0.3},
        )
        pya_layout.create_cell(
            "via$array", "PCells", {"_enct": 2, "_padw": 0.0, "_padh": 0.0, "_space": 0.0},
        )

        # Check some computed parameters
        chs_params = chs.pcell_parameters_by_name()
        self.assertEqual(chs_params["_enct"], 0)
        self.assertEqual(chs_params["_rows"], 2)
        self.assertEqual(chs_params["_cols"], 1)
        self.assertAlmostEqual(chs_params["_padh"], 1.55)
