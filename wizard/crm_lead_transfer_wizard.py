# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class CrmLeadTransferWizard(models.TransientModel):
    _name = 'crm.lead.transfer.wizard'
    _description = 'CRM Lead Transfer & User Disable Wizard'

    source_user_id = fields.Many2one(
        'res.users',
        string='Source Salesperson',
        required=True,
        help='The sales representative whose leads will be transferred.'
    )
    target_user_id = fields.Many2one(
        'res.users',
        string='Target Salesperson',
        domain="[('id', '!=', source_user_id), ('active', '=', True)]",
        help='The existing active sales representative who will receive the leads.'
    )
    transfer_mode = fields.Selection([
        ('all', 'Transfer All Leads'),
        ('selected', 'Transfer Selected Leads Only'),
    ], string='Transfer Scope', default='all', required=True)

    lead_ids = fields.Many2many(
        'crm.lead',
        string='Leads to Transfer',
        help='Specific leads selected for transfer.'
    )
    lead_count = fields.Integer(
        string='Total Leads to Transfer',
        compute='_compute_lead_count'
    )
    transfer_activities = fields.Boolean(
        string='Transfer Scheduled Activities',
        default=True,
        help='Reassign open activities and to-dos to the new salesperson.'
    )
    transfer_customers = fields.Boolean(
        string='Transfer Customer Contacts',
        default=False,
        help='Reassign customer records (res.partner) where Salesperson is the source user.'
    )
    disable_source_user = fields.Boolean(
        string='Disable Source User Account',
        default=False,
        help='Deactivate the source user account after successful transfer.'
    )

    @api.onchange('source_user_id')
    def _onchange_source_user_id(self):
        if self.source_user_id:
            leads = self.env['crm.lead'].search([('user_id', '=', self.source_user_id.id)])
            self.lead_ids = [(6, 0, leads.ids)]
        else:
            self.lead_ids = [(5, 0, 0)]

    @api.depends('source_user_id', 'transfer_mode', 'lead_ids')
    def _compute_lead_count(self):
        for rec in self:
            if rec.transfer_mode == 'all' and rec.source_user_id:
                rec.lead_count = self.env['crm.lead'].search_count([('user_id', '=', rec.source_user_id.id)])
            elif rec.transfer_mode == 'selected':
                rec.lead_count = len(rec.lead_ids)
            else:
                rec.lead_count = 0

    def action_transfer_leads(self):
        """Transfers the leads without disabling the user."""
        return self._execute_transfer(disable_user=False)

    def action_transfer_and_disable(self):
        """Transfers the leads and immediately deactivates the source user."""
        return self._execute_transfer(disable_user=True)

    def _execute_transfer(self, disable_user=False):
        self.ensure_one()
        if not self.target_user_id:
            raise UserError(_("Please select an existing target Sales Representative."))

        if not self.source_user_id:
            raise UserError(_("Please select a source Sales Representative."))

        # Identify leads to transfer
        if self.transfer_mode == 'all':
            leads = self.env['crm.lead'].search([('user_id', '=', self.source_user_id.id)])
        else:
            leads = self.lead_ids

        total_leads = len(leads)
        if total_leads == 0 and not disable_user:
            raise UserError(_("The selected source user '%s' has no leads to transfer.") % self.source_user_id.name)

        # Perform lead transfer
        if leads:
            leads.transfer_ownership(
                target_user=self.target_user_id,
                log_chatter=True,
                transfer_activities=self.transfer_activities
            )

        # Transfer customers if option selected
        if self.transfer_customers and self.source_user_id:
            partners = self.env['res.partner'].search([('user_id', '=', self.source_user_id.id)])
            if partners:
                partners.write({'user_id': self.target_user_id.id})

        # Disable source user if requested
        if disable_user or self.disable_source_user:
            self.source_user_id.write({'active': False})
            _logger.info("CRM Transfer: Disabled user '%s' (ID: %s)", self.source_user_id.name, self.source_user_id.id)

        msg = _("Successfully transferred %d leads from %s to %s.") % (
            total_leads, self.source_user_id.name, self.target_user_id.name
        )
        if disable_user or self.disable_source_user:
            msg += _(" User '%s' has been disabled.") % self.source_user_id.name

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('CRM Ownership Transfer Completed'),
                'message': msg,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }

    def action_execute_company_migration(self):
        """
        Executes the full company-wide sales-rep ownership transfer and cleanup:
        - Transfers all specified mapped leads.
        - Disables specified users (Monica, Rosemary Mupandavana, Munesu).
        - Ensures zero duplicate users are created.
        - Preserves all historical records.
        """
        # User Mapping Definitions (Source Name / Identifier -> Target User Name / Identifier)
        mapping_rules = [
            ({'name_patterns': ['Gerrylynn', 'Gerryln']}, {'name': 'Chiedza Gwature', 'login': 'chiedza@maypack.co.zw'}),
            ({'name_patterns': ['Angel Mavangira']}, {'name': 'Chiedza Gwature', 'login': 'chiedza@maypack.co.zw'}),
            ({'name_patterns': ['Sly']}, {'name': 'Kundai  Chikomba', 'login': 'kundaic@showline.co.zw'}),
            ({'name_patterns': ['Kuppakwashe', 'Kupakwashe']}, {'name': 'Kundai  Chikomba', 'login': 'kundaic@showline.co.zw'}),
            ({'name_patterns': ['Makomborero'], 'login_not': 'graig@showline.co.zw'}, {'name': 'Kundai  Chikomba', 'login': 'kundaic@showline.co.zw'}),
            ({'name_patterns': ['Kundai Chikomba'], 'id': 17}, {'name': 'Kundai  Chikomba', 'login': 'kundaic@showline.co.zw'}),
            ({'name_patterns': ['Alson Musarurwa', 'Allison']}, {'name': 'Mitchel Fish', 'login': 'mitchel@gmail.com'}),
            ({'name_patterns': ['Munesu']}, {'name': 'Mitchel Fish', 'login': 'mitchel@gmail.com'}),
            ({'name_patterns': ['Sandra']}, {'name': 'Mitchel Fish', 'login': 'mitchel@gmail.com'}),
            ({'name_patterns': ['Tapfuma1', 'Tapfuma']}, {'name': 'Mitchel Fish', 'login': 'mitchel@gmail.com'}),
            ({'name_patterns': ['Tawedzerwa1', 'Tawedzerwa']}, {'name': 'Mitchel Fish', 'login': 'mitchel@gmail.com'}),
        ]

        # Target cache to prevent duplicates
        target_cache = {}
        report_lines = []

        for src_rule, tgt_rule in mapping_rules:
            # Find target user
            tgt_key = tgt_rule['login']
            if tgt_key not in target_cache:
                tgt_user = self.env['res.users'].search([('login', '=', tgt_rule['login'])], limit=1)
                if not tgt_user:
                    tgt_user = self.env['res.users'].search([('name', 'ilike', tgt_rule['name'])], limit=1)
                target_cache[tgt_key] = tgt_user

            target_user = target_cache[tgt_key]
            if not target_user:
                _logger.warning("CRM Migration: Target user %s not found!", tgt_rule)
                continue

            # Find source users
            domain = []
            if 'id' in src_rule:
                domain = [('id', '=', src_rule['id'])]
            else:
                name_conditions = ['|'] * (len(src_rule['name_patterns']) - 1)
                for pat in src_rule['name_patterns']:
                    domain.append(('name', 'ilike', pat))
                domain = name_conditions + domain

            src_users = self.env['res.users'].search(domain)
            for src_user in src_users:
                if src_user.id == target_user.id:
                    continue
                if 'login_not' in src_rule and src_user.login == src_rule['login_not']:
                    continue

                leads = self.env['crm.lead'].search([('user_id', '=', src_user.id)])
                count = len(leads)
                if count > 0:
                    leads.transfer_ownership(target_user=target_user, log_chatter=True, transfer_activities=True)
                    report_lines.append(f"• {src_user.name} ({count} leads) ➔ {target_user.name}")

        # Disable specified users
        users_to_disable = ['Monica', 'Rose Mupandawana', 'Rosemary Mupandavana', 'Munesu']
        disabled_names = []
        for uname in users_to_disable:
            found_users = self.env['res.users'].search([('name', 'ilike', uname), ('active', '=', True)])
            for u in found_users:
                u.write({'active': False})
                disabled_names.append(u.name)

        summary_msg = _("Company Migration Summary:\n%s\n\nDisabled Users:\n%s") % (
            "\n".join(report_lines) if report_lines else _("No pending leads to transfer."),
            ", ".join(disabled_names) if disabled_names else _("None")
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Full Lead Cleanup & Migration Finished'),
                'message': summary_msg,
                'type': 'success',
                'sticky': True,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
