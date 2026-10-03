# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = 'material.material'
    _description = 'Material'
    _order = 'id desc'

    code = fields.Char(
        string='Material Code',
        required=True,
        copy=False,
        trim=True,
        help='Kode unik identifikasi material.',
    )
    name = fields.Char(
        string='Material Name',
        required=True,
        trim=True,
        help='Nama material yang akan dijual.',
    )
    material_type = fields.Selection(
        selection=[
            ('fabric', 'Fabric'),
            ('jeans', 'Jeans'),
            ('cotton', 'Cotton'),
        ],
        string='Material Type',
        required=True,
        help='Tipe material: Fabric, Jeans, atau Cotton.',
    )
    buy_price = fields.Float(
        string='Material Buy Price',
        required=True,
        digits=(16, 2),
        help='Harga beli material (minimal 100).',
    )
    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Related Supplier',
        required=True,
        ondelete='restrict',
        domain="[('supplier_rank', '>', 0)]",
        help='Supplier rekanan penyedia material ini.',
    )

    _sql_constraints = [
        (
            'code_unique',
            'UNIQUE(code)',
            'Material Code harus unik!',
        ),
        (
            'check_buy_price',
            'CHECK(buy_price >= 100)',
            'Material Buy Price tidak boleh kurang dari 100!',
        ),
    ]

    @api.constrains('buy_price')
    def _check_buy_price(self):
        """Memastikan harga beli material tidak boleh kurang dari 100."""
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(
                    _('Material Buy Price tidak boleh bernilai kurang dari 100 (Nilai saat ini: %s).')
                    % record.buy_price
                )

    def to_dict(self):
        """Serialisasi record ke dictionary untuk output JSON REST API."""
        self.ensure_one()
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'material_type': self.material_type,
            'buy_price': self.buy_price,
            'supplier': {
                'id': self.supplier_id.id,
                'name': self.supplier_id.name,
            } if self.supplier_id else None,
        }
