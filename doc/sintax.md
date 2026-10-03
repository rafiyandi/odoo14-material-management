docker-compose up -d


automated unit testing:
docker-compose run --rm web odoo -d odoo_test -i material_management --test-enable --stop-after-init
