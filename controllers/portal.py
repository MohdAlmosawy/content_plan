from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager

class ContentPlanPortal(http.Controller):

    def _prepare_plan_portal_rendering_values(self, page=1, **kwargs):
        Plan = http.request.env['content.plan']
        user_partner_id = http.request.env.user.partner_id.id

        # Add a domain filter to retrieve plans related to the logged-in user
        domain = [
            ('partner_id', '=', user_partner_id),
            ('status', 'in', ['pending_approval', 'modification', 'approved'])
        ]
        plans_count = Plan.search_count(domain)
        pager = portal_pager(
            url="/my/plans",
            total=plans_count,
            page=page,
            step=self._items_per_page
        )
        plans = Plan.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values = {
            'plans': plans,
            'pager': pager,
        }
        return values

    _items_per_page = 10  # Number of plans per page

    @http.route(['/my/plans', '/my/plans/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_plans(self, page=1, **kwargs):
        values = self._prepare_plan_portal_rendering_values(page=page, **kwargs)
        return http.request.render("content_plan.portal_my_plans", values)

    @http.route('/my/plans/<int:plan_id>/details', type='http', auth="user", website=True)
    def portal_plan_details(self, plan_id=None, **kwargs):
        Plan = http.request.env['content.plan']
        if not plan_id:
            # Handle case where no plan_id is provided
            return http.request.redirect('/my/plans')

        plan = Plan.browse(plan_id)
        if not plan:
            # Handle case where plan_id doesn't exist
            return http.request.redirect('/my/plans')

        values = {
            'plan': plan,
        }
        return http.request.render("content_plan.portal_plan_details", values)

    @http.route(['/my/plans/approve/<int:plan_id>'], type='http', auth="user", website=True)
    def approve_plan(self, plan_id, **post):
        # Fetch the plan record
        plan = http.request.env['content.plan'].sudo().browse(plan_id)

        # Trigger the action_approved method
        plan.action_approved()

        # Redirect to some page or return a response
        return http.request.redirect('/my/plans')  # Redirect to plans page after approval

    @http.route(['/my/plans/request_modification/<int:plan_id>'], type='http', auth="user", website=True)
    def request_modification(self, plan_id, **post):
        # Fetch the plan record
        plan = http.request.env['content.plan'].sudo().browse(plan_id)

        # Trigger the modification_requested method
        plan.modification_requested()

        # Redirect to some page or return a response
        return http.request.redirect('/my/plans')