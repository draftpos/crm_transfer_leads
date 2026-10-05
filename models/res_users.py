# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    crm_lead_count = fields.Integer(
        string='CRM Lead Count',
        compute='_compute_crm_leads_stats',
        help='Total number of CRM leads and opportunities currently owned by this user.'
    )
    has_active_leads = fields.Boolean(
        string='Has Active Leads',
        compute='_compute_crm_leads_stats',
        search='_search_has_active_leads',
        help='True if the user is active and has at least one CRM lead assigned.'
    )

    def _compute_crm_leads_stats(self):
        # Batch compute for performance
        Lead = self.env['crm.lead']
        for user in self:
            count = Lead.search_count([('user_id', '=', user.id)])
            user.crm_lead_count = count
            user.has_active_leads = bool(user.active and count > 0)

    def _search_has_active_leads(self, operator, value):
        if operator not in ('=', '!='):
            return []
        
        # Find all user IDs who own at least 1 lead
        self.env.cr.execute("""
            SELECT DISTINCT user_id 
            FROM crm_lead 
            WHERE user_id IS NOT NULL
        """)
        user_ids_with_leads = [row[0] for row in self.env.cr.fetchall()]

        # Active users with leads
        active_users_with_leads = self.env['res.users'].search([
            ('id', 'in', user_ids_with_leads),
            ('active', '=', True)
        ]).ids

        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('id', 'in', active_users_with_leads)]
        else:
            return [('id', 'not in', active_users_with_leads)]

    def action_open_transfer_wizard(self):
        """Opens the CRM Lead Transfer Wizard pre-filled with this user as source."""
        self.ensure_one()
        return {
            'name': _('Transfer Leads & Offboard User'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source_user_id': self.id,
            }
        }
