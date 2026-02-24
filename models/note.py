from odoo import models, fields, api, _

class PreliumPartnerNotesNote(models.Model):
    _name = 'prelium_partner_notes.note'
    _description = 'Partner Note'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Titre de la note', required=True, tracking=True)
    content = fields.Html(string='Contenu explicatif', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, tracking=True)
    priority = fields.Selection([
        ('0', 'Normale'),
        ('1', 'Haute'),
        ('2', 'Urgente')
    ], string='Priorite', required=True, default='0', tracking=True)
    category_id = fields.Many2one('prelium_partner_notes.category', string='Categorie', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partenaire', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.uid, tracking=True)
    state = fields.Selection([
        ('open', 'Ouverte'),
        ('in_progress', 'En cours'),
        ('closed', 'Cloturee')
    ], string='Statut', required=True, default='open', tracking=True)

    _sql_constraints = []

    def action_set_in_progress(self):
        """Met la note en cours d'avancement."""
        for record in self:
            record.state = 'in_progress'

    def action_set_closed(self):
        """Cloture la note."""
        for record in self:
            record.state = 'closed'
