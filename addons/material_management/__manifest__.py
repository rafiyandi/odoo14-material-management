# -*- coding: utf-8 -*-
{
    'name': 'Material Management',
    'version': '14.0.1.0.0',
    'category': 'Inventory/Materials',
    'summary': 'Modul Registrasi Material dan REST API Controller',
    'description': """
        Modul Odoo 14 untuk mengelola data material yang akan dijual:
        - Registrasi Material (Code, Name, Type, Buy Price, Supplier)
        - Validasi ketat (Buy price >= 100, field required, unique code)
        - Filter berdasarkan Material Type (Fabric, Jeans, Cotton)
        - REST API Controller untuk integrasi eksternal
        - Unit Testing otomatis
    """,
    'author': 'Backend Engineer Candidate',
    'website': 'https://keda-tech.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
