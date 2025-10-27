/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

const REMINDER_INTERVAL = 5 * 60 * 1000; // 5 minutes
const STORAGE_KEY = "onboarding_last_popup";

const onboardingReminderService = {
    dependencies: ["user", "orm", "dialog"],
    async start(env, { user, orm, dialog: dialogService }) {
        if (!dialogService || !user) {
            console.warn("Onboarding reminder: Required services not available");
            return;
        }

        const userId = user.userId;
        if (!userId || userId === 1) {
            return;
        }

        let dialogActive = false;

        const getEmployeeId = async () => {
            if (user.employee_id) {
                return user.employee_id;
            }

            try {
                const userData = await orm.read("res.users", [userId], ["employee_id"]);
                if (userData[0]?.employee_id) {
                    return userData[0].employee_id[0];
                }
            } catch (error) {
                console.warn("Onboarding reminder: Could not read user data", error);
            }

            const employees = await orm.searchRead(
                "hr.employee",
                [["user_id", "=", userId]],
                ["id"]
            );

            return employees.length > 0 ? employees[0].id : false;
        };

        const showReminder = async () => {
            if (dialogActive) {
                return;
            }

            const lastPopup = parseInt(localStorage.getItem(STORAGE_KEY)) || 0;
            const now = Date.now();

            if (now - lastPopup < REMINDER_INTERVAL) {
                setTimeout(showReminder, REMINDER_INTERVAL - (now - lastPopup));
                return;
            }

            const employeeId = await getEmployeeId();
            if (!employeeId) {
                setTimeout(showReminder, REMINDER_INTERVAL);
                return;
            }

            try {
                const pending = await orm.call(
                    "hr.employee",
                    "get_pending_onboarding_docs",
                    [[employeeId]]
                );

                if (pending && pending.pending_count > 0) {
                    dialogActive = true;

                    // Create formatted text without HTML
                    const docsList = pending.pending_docs.map(doc => `• ${doc}`).join('\n');
                    const bodyText = `You still have ${pending.pending_count} pending onboarding document(s):\n\n${docsList}`;

                    dialogService.add(ConfirmationDialog, {
                        title: "Onboarding Reminder",
                        body: bodyText,
                        confirmLabel: "Click Here To Upload",
                        cancelLabel: "Later",
                        confirm: async () => {
                            dialogActive = false;
                            localStorage.setItem(STORAGE_KEY, Date.now().toString());

                            await env.services.action.doAction({
                                type: "ir.actions.act_window",
                                name: "Onboarding Upload Wizard",
                                res_model: "onboarding.upload.wizard",
                                views: [[false, "form"]],
                                target: "new",
                                context: {
                                    default_employee_id: await getEmployeeId(),
                                },
                            });

                            setTimeout(showReminder, REMINDER_INTERVAL);
                        },
                        // confirm: () => {
                        //     dialogActive = false;
                        //     localStorage.setItem(STORAGE_KEY, Date.now().toString());
                        //     setTimeout(showReminder, REMINDER_INTERVAL);
                        // },
                        cancel: () => {
                            dialogActive = false;
                            setTimeout(showReminder, REMINDER_INTERVAL);
                        },
                    });
                } else {
                    setTimeout(showReminder, REMINDER_INTERVAL);
                }
            } catch (err) {
                console.warn("Onboarding reminder error:", err);
                setTimeout(showReminder, REMINDER_INTERVAL);
            }
        };

        setTimeout(showReminder, 2000);
    },
};

registry.category("services").add("onboarding_reminder_popup", onboardingReminderService);