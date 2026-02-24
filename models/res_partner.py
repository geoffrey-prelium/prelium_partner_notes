from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_note_ids = fields.One2many('prelium_partner_notes.note', 'partner_id', string='Notes liees')
    partner_note_count = fields.Integer(string='Nombre de notes', compute='_compute_partner_note_count')

    @api.depends('partner_note_ids')
    def _compute_partner_note_count(self):
        for partner in self:
            partner.partner_note_count = len(partner.partner_note_ids)

    def action_view_partner_notes(self):
        """Affiche les notes associees a ce partenaire."""
        self.ensure_one()
        return {
            'name': 'Notes',
            'type': 'ir.actions.act_window',
            'res_model': 'prelium_partner_notes.note',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
