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
