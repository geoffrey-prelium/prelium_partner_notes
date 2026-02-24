from odoo import models, fields

class PreliumPartnerNotesCategory(models.Model):
    _name = 'prelium_partner_notes.category'
    _description = 'Partner Note Category'
    _order = 'name'

    name = fields.Char(string='Nom de la categorie', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom de la categorie doit etre unique !')
    ]
