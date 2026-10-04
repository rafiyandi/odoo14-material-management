# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

VALID_MATERIAL_TYPES = ['fabric', 'jeans', 'cotton']

# Monkey-patch http.Root.get_request agar REST API (/api/) tidak diintersepsi
# oleh JsonRequest (Odoo JSON-RPC 2.0) ketika client mengirim Content-Type: application/json.
_original_get_request = http.Root.get_request


def _custom_get_request(self, httprequest):
    if httprequest.path.startswith('/api/'):
        return http.HttpRequest(httprequest)
    return _original_get_request(self, httprequest)


http.Root.get_request = _custom_get_request


def _json_response(data, status=200):
    """Utility helper untuk mengembalikan response JSON berstandar HTTP."""
    response = request.make_response(
        json.dumps(data),
        headers=[
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Cache-Control', 'no-store'),
        ],
    )
    response.status_code = status
    return response


def _error_response(message, status=400, errors=None):
    """Utility helper untuk format error response terstandar."""
    payload = {
        'status': 'error',
        'message': message,
    }
    if errors:
        payload['errors'] = errors
    return _json_response(payload, status=status)


class MaterialController(http.Controller):

    def _parse_body(self):
        """Helper untuk membaca payload JSON dari HTTP request."""
        try:
            raw_data = request.httprequest.get_data() or request.httprequest.data
            if not raw_data:
                return {}
            return json.loads(raw_data.decode('utf-8'))
        except Exception as e:
            _logger.warning("Gagal parse request body JSON: %s", str(e))
            return None

    # --------------------------------------------------------------------------
    # 1. CREATE MATERIAL (POST /api/v1/materials)
    # --------------------------------------------------------------------------
    @http.route(
        '/api/v1/materials',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False,
    )
    def create_material(self, **kwargs):
        """Endpoint registrasi material baru."""
        body = self._parse_body()
        if body is None:
            return _error_response("Format JSON tidak valid.", status=400)

        # 1. Validasi keberadaan seluruh field wajib
        required_fields = ['code', 'name', 'material_type', 'buy_price', 'supplier_id']
        missing = [f for f in required_fields if body.get(f) in (None, '')]
        if missing:
            return _error_response(
                "Semua informasi material harus terisi.",
                status=400,
                errors={f: "Field ini wajib diisi" for f in missing},
            )

        # 2. Validasi material_type
        material_type = str(body.get('material_type', '')).lower()
        if material_type not in VALID_MATERIAL_TYPES:
            return _error_response(
                "Material Type tidak valid. Pilihan: Fabric, Jeans, Cotton.",
                status=400,
                errors={'material_type': f"Harus salah satu dari: {', '.join(VALID_MATERIAL_TYPES)}"},
            )

        # 3. Validasi buy_price
        try:
            buy_price = float(body.get('buy_price'))
        except (ValueError, TypeError):
            return _error_response(
                "Material Buy Price harus berupa angka numerik.",
                status=400,
                errors={'buy_price': "Nilai harus berupa angka"},
            )

        if buy_price < 100:
            return _error_response(
                "Material Buy Price tidak boleh nilainya < 100.",
                status=400,
                errors={'buy_price': "Nilai minimal adalah 100"},
            )

        # 4. Validasi supplier_id (res.partner)
        supplier_id = body.get('supplier_id')
        supplier = request.env['res.partner'].sudo().browse(supplier_id)
        if not supplier.exists():
            return _error_response(
                "Supplier yang dipilih tidak ditemukan.",
                status=404,
                errors={'supplier_id': f"Partner dengan ID {supplier_id} tidak ada"},
            )

        # 5. Simpan record
        try:
            vals = {
                'code': str(body.get('code')).strip(),
                'name': str(body.get('name')).strip(),
                'material_type': material_type,
                'buy_price': buy_price,
                'supplier_id': supplier.id,
            }
            new_material = request.env['material.material'].sudo().create(vals)
            return _json_response(
                {
                    'status': 'success',
                    'message': 'Material berhasil didaftarkan.',
                    'data': new_material.to_dict(),
                },
                status=201,
            )
        except ValidationError as ve:
            return _error_response(str(ve), status=400)
        except Exception as e:
            _logger.exception("Error saat pembuatan material: %s", str(e))
            return _error_response("Gagal menyimpan material. Kemungkinan kode material sudah terdaftar.", status=400)

    # --------------------------------------------------------------------------
    # 2. GET LIST & FILTER MATERIALS (GET /api/v1/materials)
    # --------------------------------------------------------------------------
    @http.route(
        '/api/v1/materials',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
    )
    def list_materials(self, **kwargs):
        """Endpoint mengambil seluruh material, dengan opsional filter Material Type."""
        domain = []
        material_type = kwargs.get('material_type')

        if material_type:
            material_type_clean = str(material_type).lower().strip()
            if material_type_clean not in VALID_MATERIAL_TYPES:
                return _error_response(
                    "Filter material_type tidak valid. Pilihan: Fabric, Jeans, Cotton.",
                    status=400,
                )
            domain.append(('material_type', '=', material_type_clean))

        try:
            materials = request.env['material.material'].sudo().search(domain)
            return _json_response({
                'status': 'success',
                'count': len(materials),
                'filter': {'material_type': material_type.lower() if material_type else None},
                'data': [m.to_dict() for m in materials],
            })
        except Exception as e:
            _logger.exception("Error list materials: %s", str(e))
            return _error_response("Terjadi kesalahan internal server.", status=500)

    # --------------------------------------------------------------------------
    # 3. GET DETAIL MATERIAL (GET /api/v1/materials/<id>)
    # --------------------------------------------------------------------------
    @http.route(
        '/api/v1/materials/<int:material_id>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
    )
    def get_material_detail(self, material_id, **kwargs):
        """Endpoint mengambil detail satu material berdasarkan ID."""
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            return _error_response(f"Material dengan ID {material_id} tidak ditemukan.", status=404)

        return _json_response({
            'status': 'success',
            'data': material.to_dict(),
        })

    # --------------------------------------------------------------------------
    # 4. UPDATE MATERIAL (PUT /api/v1/materials/<id>)
    # --------------------------------------------------------------------------
    @http.route(
        '/api/v1/materials/<int:material_id>',
        type='http',
        auth='public',
        methods=['PUT', 'PATCH'],
        csrf=False,
    )
    def update_material(self, material_id, **kwargs):
        """Endpoint melakukan update terhadap satu material."""
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            return _error_response(f"Material dengan ID {material_id} tidak ditemukan.", status=404)

        body = self._parse_body()
        if body is None:
            return _error_response("Format JSON tidak valid.", status=400)

        vals = {}

        # Validasi update name/code jika ada
        if 'code' in body:
            if not body['code']:
                return _error_response("Material Code tidak boleh kosong.", status=400)
            vals['code'] = str(body['code']).strip()

        if 'name' in body:
            if not body['name']:
                return _error_response("Material Name tidak boleh kosong.", status=400)
            vals['name'] = str(body['name']).strip()

        # Validasi update material_type jika ada
        if 'material_type' in body:
            m_type = str(body['material_type']).lower()
            if m_type not in VALID_MATERIAL_TYPES:
                return _error_response(
                    "Material Type tidak valid. Pilihan: Fabric, Jeans, Cotton.",
                    status=400,
                )
            vals['material_type'] = m_type

        # Validasi update buy_price jika ada
        if 'buy_price' in body:
            try:
                price = float(body['buy_price'])
            except (ValueError, TypeError):
                return _error_response("Buy price harus berupa angka.", status=400)
            if price < 100:
                return _error_response("Material Buy Price tidak boleh nilainya < 100.", status=400)
            vals['buy_price'] = price

        # Validasi update supplier_id jika ada
        if 'supplier_id' in body:
            supp_id = body['supplier_id']
            supplier = request.env['res.partner'].sudo().browse(supp_id)
            if not supplier.exists():
                return _error_response(f"Supplier dengan ID {supp_id} tidak ditemukan.", status=404)
            vals['supplier_id'] = supplier.id

        if not vals:
            return _error_response("Tidak ada data yang dikirim untuk diupdate.", status=400)

        try:
            material.write(vals)
            return _json_response({
                'status': 'success',
                'message': f"Material ID {material_id} berhasil diperbarui.",
                'data': material.to_dict(),
            })
        except ValidationError as ve:
            return _error_response(str(ve), status=400)
        except Exception as e:
            _logger.exception("Error update material: %s", str(e))
            return _error_response("Gagal memperbarui material. Kemungkinan duplikasi kode.", status=400)

    # --------------------------------------------------------------------------
    # 5. DELETE MATERIAL (DELETE /api/v1/materials/<id>)
    # --------------------------------------------------------------------------
    @http.route(
        '/api/v1/materials/<int:material_id>',
        type='http',
        auth='public',
        methods=['DELETE'],
        csrf=False,
    )
    def delete_material(self, material_id, **kwargs):
        """Endpoint melakukan delete terhadap satu material."""
        material = request.env['material.material'].sudo().browse(material_id)
        if not material.exists():
            return _error_response(f"Material dengan ID {material_id} tidak ditemukan.", status=404)

        try:
            code = material.code
            name = material.name
            material.unlink()
            return _json_response({
                'status': 'success',
                'message': f"Material '{name}' ({code}) dengan ID {material_id} berhasil dihapus.",
            })
        except Exception as e:
            _logger.exception("Error delete material: %s", str(e))
            return _error_response("Gagal menghapus material.", status=400)
