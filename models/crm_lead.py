# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def transfer_ownership(self, target_user, log_chatter=True, transfer_activities=True):
        """
        Safely reassigns lead ownership to target_user.
        Preserves creation date, lead history, notes, and communications.
        """
        if not target_user:
            raise UserError(_("Please specify a target Sales Representative."))

        for lead in self:
            old_user = lead.user_id
            if old_user == target_user:
                continue

            # Update salesperson
            lead.write({'user_id': target_user.id})

            # Reassign pending activities if requested
            if transfer_activities and old_user:
                activities = self.env['mail.activity'].search([
                    ('res_model', '=', 'crm.lead'),
                    ('res_id', '=', lead.id),
                    ('user_id', '=', old_user.id)
                ])
                if activities:
                    activities.write({'user_id': target_user.id})

            # Log clean chatter message
            if log_chatter:
                old_name = old_user.name if old_user else _("Unassigned")
                body = _(
                    "<b>Ownership Reassigned</b><br/>"
                    "• Previous Salesperson: <b>%s</b><br/>"
                    "• New Salesperson: <b>%s</b>"
                ) % (old_name, target_user.name)
                lead.message_post(body=body, message_type='notification', subtype_xmlid='mail.mt_note')

        return True
