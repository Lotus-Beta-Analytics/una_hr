from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class OnboardingCron(models.Model):
    _name = 'onboarding.cron'
    _description = 'Onboarding Documents Reminder Cron'

    def send_onboarding_reminders(self):
        """
        Cron job to send reminders to employees with pending documents
        Runs every 7 days and only targets affected employees
        """
        _logger.info("=== STARTING ONBOARDING REMINDER CRON JOB ===")

        # NARROWED DOMAIN: Only employees who are actually in onboarding process
        employees = self.env['hr.employee'].search([
            ('active', '=', True),
            # Only employees who have started onboarding (at least one onboarding field is set)
            '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
            ('onboarding_loe_ack', '=', False),
            ('onboarding_bond_ack', '=', False),
            ('onboarding_background_check', '=', False),
            ('onboarding_police_report', '=', False),
            ('onboarding_medical', '=', False),
            ('onboarding_employment_form', '=', False),
            ('onboarding_passport_photo', '=', False),
            ('onboarding_credentials', '=', False),
            ('onboarding_documented', '=', False),
            ('onboarding_referees', '=', False),
            ('onboarding_licenses', '=', False),
            ('onboarding_cv', '=', False),
            ('onboarding_id_card', '!=', 'yes'),
            ('onboarding_uniforms', '!=', 'yes'),
            ('onboarding_account', '!=', 'yes'),
            ('onboarding_tools', '!=', 'yes'),
            ('onboarding_handbook', '!=', 'yes'),
            ('onboarding_email', '!=', 'yes'),
        ])

        _logger.info(f"Found {len(employees)} employees in onboarding process")

        reminder_count = 0
        today = fields.Date.today()
        # seven_days_ago = today - timedelta(days=7)  # Calculate once

        for employee in employees:
            try:
                # Additional filtering: Check if employee was created recently (within last 90 days)
                if employee.create_date:
                    days_since_creation = (today - employee.create_date.date()).days
                    if days_since_creation > 70:  # Skip employees created more than 90 days ago
                        _logger.info(f"Skipping {employee.name} - created more than 90 days ago")
                        continue
                # Check if 7 days have passed since last reminder
                # if employee.last_comprehensive_reminder_date:
                #     if employee.last_comprehensive_reminder_date > seven_days_ago:
                #         continue

                # Get pending documents for this specific employee
                pending_docs = self._get_pending_documents(employee)

                if pending_docs:
                    # Additional check: Only send if employee has work email or user account
                    if not employee.work_email and not employee.user_id:
                        _logger.info(f"Skipping {employee.name} - no email or user account")
                        continue

                    # Send reminder only if there are pending documents
                    self._send_employee_reminder(employee, pending_docs)
                    employee.last_comprehensive_reminder_date = today
                    reminder_count += 1
                    _logger.info(f"Reminder sent to {employee.name} for {len(pending_docs)} pending documents")
                else:
                    _logger.info(f"No pending documents found for {employee.name}")

            except Exception as e:
                _logger.error(f"Error processing employee {employee.name}: {str(e)}")
                continue

        _logger.info(f"=== CRON JOB COMPLETED: {reminder_count} reminders sent out of {len(employees)} candidates ===")
        return True

    def _get_pending_documents(self, employee):
        """
        Get specifically which documents are pending for an employee
        Only returns documents that are REQUIRED but not uploaded
        """
        pending_docs = []

        # Document mapping with conditional logic
        document_checks = [
            # (attachment_field, document_name, required_condition)
            ('onboarding_loe_ack_attachment_ids', 'LOE Acknowledgement',
             not employee.onboarding_loe_ack),

            ('onboarding_bond_ack_attachment_ids', 'Bond Letter',
             not employee.onboarding_bond_ack),

            ('onboarding_background_check_attachment_ids', 'Background Check Form',
             not employee.onboarding_background_check),

            ('onboarding_police_report_attachment_ids', 'Police Report',
             not employee.onboarding_police_report),

            ('onboarding_medical_attachment_ids', 'Medical Report',
             not employee.onboarding_medical),

            ('onboarding_employment_form_attachment_ids', 'Employment Form',
             not employee.onboarding_employment_form),

            ('onboarding_passport_photo_attachment_ids', 'Passport Photographs',
             not employee.onboarding_passport_photo),

            ('onboarding_credentials_attachment_ids', 'Credentials Copies',
             not employee.onboarding_credentials),

            ('onboarding_documented_attachment_ids', 'Information Documentation',
             not employee.onboarding_documented),

            ('onboarding_licenses_attachment_ids', 'Professional Licenses',
             not employee.onboarding_licenses and self._is_technical_staff(employee)),

            ('onboarding_cv_attachment_ids', 'CV and Credentials',
             not employee.onboarding_cv),
        ]

        for attachment_field, doc_name, is_required in document_checks:
            if is_required:
                attachments = getattr(employee, attachment_field)
                if not attachments:  # No attachments uploaded for required document
                    pending_docs.append({
                        'name': doc_name,
                        'field': attachment_field
                    })

        return pending_docs

    def _is_technical_staff(self, employee):
        """
        Check if employee is in technical roles that require licenses
        (Pilots, Cabin Crew, Flight Dispatchers, Engineers, Planning)
        """
        technical_departments = [
            'flight operations', 'engineering', 'maintenance',
            'dispatch', 'planning', 'technical'
        ]

        if employee.department_id:
            dept_name = employee.department_id.name.lower()
            return any(tech_dept in dept_name for tech_dept in technical_departments)

        # Check job title as fallback
        technical_jobs = [
            'pilot', 'captain', 'first officer', 'cabin crew', 'flight attendant',
            'dispatcher', 'engineer', 'technician', 'planner'
        ]

        if employee.job_id and employee.job_id.name:
            job_name = employee.job_id.name.lower()
            return any(tech_job in job_name for tech_job in technical_jobs)

        return False

    def _send_employee_reminder(self, employee, pending_documents):
        """
        Send personalized reminder to employee about their specific pending documents
        """
        try:
            # Get the email template using XML ID reference
            template = self.env.ref('una_employee_details.onboarding_initial_reminder_template')

            # Create a context with the variables
            context = {
                'employee_name': employee.get_employee_name() or employee.name or 'Employee',
                'pending_documents': pending_documents or [],
                'pending_count': len(pending_documents) if pending_documents else 0,
                'company_name': self.env.user.company_id.name or 'Your Company',
            }

            # Add context to the template environment
            template = template.with_context(context)

            # Determine recipient
            recipient_ids = []
            if employee.user_id and employee.user_id.partner_id:
                recipient_ids = employee.user_id.partner_id.ids
            elif employee.work_email:
                # Create temporary partner for email
                partner = self.env['res.partner'].create({
                    'name': employee.name,
                    'email': employee.work_email
                })
                recipient_ids = partner.ids

            email_to = employee.work_email
            partner_ids = recipient_ids

            if not email_to and not partner_ids:
                _logger.warning(f"Skipping {employee.name} — no valid recipient (no work_email or linked partner).")
                return  # skip sending completely

            template.send_mail(
                employee.id,
                force_send=True,
                email_values={
                    'partner_ids': partner_ids,
                    'email_to': email_to,
                }
            )
            _logger.info(f"Reminder email sent to {employee.name}: {len(pending_documents)} pending docs")
        except Exception as e:
            _logger.error(f"Failed to send reminder to {employee.name}: {str(e)}")
            raise



