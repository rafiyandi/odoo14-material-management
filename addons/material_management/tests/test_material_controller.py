# -*- coding: utf-8 -*-
import json
import odoo
from odoo.tests.common import HttpCase, tagged, HOST


@tagged('-at_install', 'post_install')
class TestMaterialController(HttpCase):

    def setUp(self):
        super(TestMaterialController, self).setUp()
        # Setup supplier rekanan
        self.supplier = self.env['res.partner'].create({
            'name': 'PT Garment Indah Perkasa',
            'email': 'garment@indahperkasa.com',
        })

    def _make_http_request(self, path, method='GET', data=None):
        """Helper untuk eksekusi HTTP request ke controller."""
        self.env['base'].flush()
        if path.startswith('/'):
            url = f"http://{HOST}:{odoo.tools.config['http_port']}{path}"
        else:
            url = path

        headers = {}
        encoded_data = None
        if data is not None:
            headers['Content-Type'] = 'application/json'
            encoded_data = json.dumps(data)

        response = self.opener.request(method, url, data=encoded_data, headers=headers)
        try:
            resp_body = response.json()
        except Exception:
            resp_body = response.text
        return response.status_code, resp_body

    def test_01_api_create_material_success(self):
        """Memastikan API POST /api/v1/materials berhasil membuat material."""
        payload = {
            'code': 'API-MAT-001',
            'name': 'Denim Washed Blue',
            'material_type': 'jeans',
            'buy_price': 185000.0,
            'supplier_id': self.supplier.id,
        }
        status, body = self._make_http_request('/api/v1/materials', method='POST', data=payload)
        self.assertEqual(status, 201)
        self.assertEqual(body.get('status'), 'success')
        self.assertEqual(body['data']['code'], 'API-MAT-001')

    def test_02_api_create_material_price_below_100_rejected(self):
        """Memastikan API POST /api/v1/materials menolak harga < 100."""
        payload = {
            'code': 'API-MAT-FAIL-01',
            'name': 'Kain Murah',
            'material_type': 'fabric',
            'buy_price': 85.0,  # Kurang dari 100
            'supplier_id': self.supplier.id,
        }
        status, body = self._make_http_request('/api/v1/materials', method='POST', data=payload)
        self.assertEqual(status, 400)
        self.assertEqual(body.get('status'), 'error')
        self.assertIn('100', body.get('message', ''))

    def test_03_api_create_material_missing_fields_rejected(self):
        """Memastikan API POST /api/v1/materials menolak jika ada field wajib yang kosong."""
        payload = {
            'code': 'API-MAT-MISSING',
            # 'name' sengaja dihilangkan
            'material_type': 'fabric',
            'buy_price': 150000.0,
            'supplier_id': self.supplier.id,
        }
        status, body = self._make_http_request('/api/v1/materials', method='POST', data=payload)
        self.assertEqual(status, 400)
        self.assertEqual(body.get('status'), 'error')

    def test_04_api_list_and_filter_materials(self):
        """Memastikan API GET /api/v1/materials dan filter material_type berfungsi."""
        # Buat dummy material
        self.env['material.material'].create([
            {
                'code': 'MAT-FILTER-FABRIC',
                'name': 'Silk Fabric',
                'material_type': 'fabric',
                'buy_price': 200000.0,
                'supplier_id': self.supplier.id,
            },
            {
                'code': 'MAT-FILTER-JEANS',
                'name': 'Black Jeans 12oz',
                'material_type': 'jeans',
                'buy_price': 220000.0,
                'supplier_id': self.supplier.id,
            }
        ])

        # Test ambil seluruh data
        status, body = self._make_http_request('/api/v1/materials', method='GET')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('status'), 'success')
        self.assertGreaterEqual(body.get('count', 0), 2)

        # Test filter jeans
        status, body_jeans = self._make_http_request('/api/v1/materials?material_type=jeans', method='GET')
        self.assertEqual(status, 200)
        for item in body_jeans.get('data', []):
            self.assertEqual(item['material_type'], 'jeans')

    def test_05_api_update_material(self):
        """Memastikan API PUT /api/v1/materials/<id> berhasil mengubah data."""
        mat = self.env['material.material'].create({
            'code': 'MAT-UPD-001',
            'name': 'Cotton Asli',
            'material_type': 'cotton',
            'buy_price': 130000.0,
            'supplier_id': self.supplier.id,
        })

        update_payload = {
            'name': 'Cotton Combed 24s Premium',
            'buy_price': 145000.0,
        }
        status, body = self._make_http_request(f'/api/v1/materials/{mat.id}', method='PUT', data=update_payload)
        self.assertEqual(status, 200)
        self.assertEqual(body['data']['name'], 'Cotton Combed 24s Premium')
        self.assertEqual(body['data']['buy_price'], 145000.0)

    def test_06_api_delete_material(self):
        """Memastikan API DELETE /api/v1/materials/<id> berhasil menghapus data."""
        mat = self.env['material.material'].create({
            'code': 'MAT-DEL-001',
            'name': 'Material To Delete',
            'material_type': 'fabric',
            'buy_price': 110000.0,
            'supplier_id': self.supplier.id,
        })
        mat_id = mat.id

        status, body = self._make_http_request(f'/api/v1/materials/{mat_id}', method='DELETE')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('status'), 'success')

        # Cek database apakah record sudah terhapus
        self.env['material.material'].invalidate_cache()
        deleted = self.env['material.material'].browse(mat_id)
        self.assertFalse(deleted.exists())
