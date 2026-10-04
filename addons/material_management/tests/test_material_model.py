# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger


@tagged('at_install', 'post_install')
class TestMaterialModel(TransactionCase):

    def setUp(self):
        super(TestMaterialModel, self).setUp()
        # Setup supplier rekanan
        self.supplier = self.env['res.partner'].create({
            'name': 'PT Mitra Tekstil Sejahtera',
            'email': 'supplier@mitratekstil.com',
        })

    def test_01_create_valid_material(self):
        """Memastikan material dengan data valid berhasil dibuat."""
        material = self.env['material.material'].create({
            'code': 'MAT-TEST-001',
            'name': 'Fabric Katun Rayon',
            'material_type': 'cotton',
            'buy_price': 150000.0,
            'supplier_id': self.supplier.id,
        })
        self.assertTrue(material.id, "Material harus memiliki ID setelah dibuat.")
        self.assertEqual(material.code, 'MAT-TEST-001')
        self.assertEqual(material.name, 'Fabric Katun Rayon')
        self.assertEqual(material.material_type, 'cotton')
        self.assertEqual(material.buy_price, 150000.0)
        self.assertEqual(material.supplier_id.id, self.supplier.id)

    def test_02_buy_price_below_100_raises_validation_error(self):
        """Memastikan validasi menolak harga beli < 100."""
        with self.assertRaises(ValidationError):
            self.env['material.material'].create({
                'code': 'MAT-FAIL-001',
                'name': 'Jeans Murah',
                'material_type': 'jeans',
                'buy_price': 99.9,  # < 100
                'supplier_id': self.supplier.id,
            })

    def test_03_buy_price_update_below_100_raises_validation_error(self):
        """Memastikan update harga menjadi < 100 memicu ValidationError."""
        material = self.env['material.material'].create({
            'code': 'MAT-TEST-002',
            'name': 'Fabric Premium',
            'material_type': 'fabric',
            'buy_price': 200.0,
            'supplier_id': self.supplier.id,
        })
        with self.assertRaises(ValidationError):
            material.write({'buy_price': 50.0})

    def test_04_duplicate_code_fails(self):
        """Memastikan kode material harus unik."""
        self.env['material.material'].create({
            'code': 'MAT-UNIQUE-001',
            'name': 'Jeans Hitam 1',
            'material_type': 'jeans',
            'buy_price': 250000.0,
            'supplier_id': self.supplier.id,
        })

        with mute_logger('odoo.sql_db'):
            with self.assertRaises(Exception):
                self.env['material.material'].create({
                    'code': 'MAT-UNIQUE-001',  # Duplikat
                    'name': 'Jeans Hitam 2',
                    'material_type': 'jeans',
                    'buy_price': 300000.0,
                    'supplier_id': self.supplier.id,
                })

    def test_05_to_dict_method(self):
        """Memastikan helper method to_dict menghasilkan format yang benar."""
        material = self.env['material.material'].create({
            'code': 'MAT-DICT-001',
            'name': 'Cotton Combed 30s',
            'material_type': 'cotton',
            'buy_price': 120000.0,
            'supplier_id': self.supplier.id,
        })
        data = material.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['code'], 'MAT-DICT-001')
        self.assertEqual(data['supplier']['id'], self.supplier.id)
        self.assertEqual(data['supplier']['name'], self.supplier.name)
