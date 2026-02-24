from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestPreliumPartnerNotes(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestPreliumPartnerNotes, cls).setUpClass()
        
        # Create users
        cls.user_base = cls.env['res.users'].create({
            'name': 'Base User',
            'login': 'base_user_test',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])]
        })
        cls.user_admin = cls.env['res.users'].create({
            'name': 'Admin User',
            'login': 'admin_user_test',
            'groups_id': [(6, 0, [cls.env.ref('base.group_system').id])]
        })

        # Create category
        cls.category = cls.env['prelium_partner_notes.category'].create({
            'name': 'Test Category'
        })

        # Create partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner'
        })

    def test_note_creation(self):
        """Verifier qu'on peut creer une note liee a un partenaire avec les champs obligatoires."""
        note = self.env['prelium_partner_notes.note'].with_user(self.user_base).create({
            'name': 'Test Note 1',
            'content': '<p>Content</p>',
            'category_id': self.category.id,
            'partner_id': self.partner.id,
        })
        self.assertTrue(note.id)
        self.assertEqual(note.state, 'open')
        self.assertEqual(note.priority, 'normal')

    def test_note_state_transition(self):
        """Verifier que la modification d'etat fonctionne correctement."""
        note = self.env['prelium_partner_notes.note'].create({
            'name': 'Test Note State',
            'content': '<p>Content</p>',
            'category_id': self.category.id,
            'partner_id': self.partner.id,
        })
        self.assertEqual(note.state, 'open')
        
        note.action_set_in_progress()
        self.assertEqual(note.state, 'in_progress')
        
        note.action_set_closed()
        self.assertEqual(note.state, 'closed')

    def test_partner_note_count(self):
        """Verifier que le compteur sur res.partner se met a jour."""
        self.assertEqual(self.partner.partner_note_count, 0)
        
        note = self.env['prelium_partner_notes.note'].create({
            'name': 'Test Note Count',
            'content': '<p>Content</p>',
            'category_id': self.category.id,
            'partner_id': self.partner.id,
        })
        self.assertEqual(self.partner.partner_note_count, 1)

        note2 = self.env['prelium_partner_notes.note'].create({
            'name': 'Test Note Count 2',
            'content': '<p>Content</p>',
            'category_id': self.category.id,
            'partner_id': self.partner.id,
        })
        self.partner.invalidate_recordset(['partner_note_count'])
        self.assertEqual(self.partner.partner_note_count, 2)
        
        note.unlink()
        self.partner.invalidate_recordset(['partner_note_count'])
        self.assertEqual(self.partner.partner_note_count, 1)

    def test_security_access(self):
        """Controller que base.group_user ne peut pas supprimer de note, alors que group_system le peut."""
        note = self.env['prelium_partner_notes.note'].create({
            'name': 'Test Delete Note',
            'content': '<p>Content</p>',
            'category_id': self.category.id,
            'partner_id': self.partner.id,
        })

        # base.group_user cannot unlink
        with self.assertRaises(AccessError):
            note.with_user(self.user_base).unlink()

        # base.group_system can unlink
        note.with_user(self.user_admin).unlink()
        self.assertFalse(note.exists())
