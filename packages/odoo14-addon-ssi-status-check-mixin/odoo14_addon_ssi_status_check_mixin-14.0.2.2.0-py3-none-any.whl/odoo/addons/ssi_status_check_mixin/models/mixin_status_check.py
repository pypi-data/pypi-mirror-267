# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class MixinStatusCheck(models.AbstractModel):
    _name = "mixin.status_check"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Mixin Object for Status Check"

    _status_check_create_page = False
    _status_check_page_xpath = "//page[last()]"

    status_check_template_id = fields.Many2one(
        string="Status Check Template",
        comodel_name="status.check.template",
        domain=lambda self: [("model", "=", self._name)],
    )
    status_check_ids = fields.One2many(
        string="Status Check",
        comodel_name="status.check",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
        readonly=True,
    )

    @ssi_decorator.insert_on_form_view()
    def _status_check_insert_form_element(self, view_arch):
        if self._status_check_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_status_check_mixin.status_check_page",
                xpath=self._status_check_page_xpath,
                position="after",
            )
        return view_arch

    def _prepare_status_check_data(self, template_id, template_detail_id):
        self.ensure_one()
        data = {
            "res_id": self.id,
            "model": self._name,
            "template_id": template_id,
            "template_detail_id": template_detail_id,
        }
        return data

    def _prepare_status_check_create(self):
        self.ensure_one()
        template = self.status_check_template_id
        allowed_details = template.detail_ids
        self.status_check_ids.filtered(
            lambda r: r.template_detail_id.id not in allowed_details.ids
        ).unlink()
        data = template.detail_ids - self.status_check_ids.mapped("template_detail_id")
        return data

    def _get_status_check_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
            "time": tools.safe_eval.time,
            "datetime": tools.safe_eval.datetime,
            "dateutil": tools.safe_eval.dateutil,
        }

    def _evaluate_status_check(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_status_check_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _get_template_status_check(self):
        result = False
        obj_status_check_template = self.env["status.check.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        template_id = obj_status_check_template.search(
            criteria,
            order="sequence desc",
            limit=1,
        )
        if template_id:
            if self._evaluate_status_check(template_id):
                result = template_id.id
        return result

    def action_reload_status_check_template(self):
        for record in self:
            record.status_check_template_id = False
            record.write(
                {
                    "status_check_template_id": self._get_template_status_check(),
                }
            )
            record._reload_status_check()

    def action_reload_status_check(self):
        for record in self:
            record._reload_status_check()

    def _reload_status_check(self):
        self.ensure_one()
        if self.status_check_template_id:
            to_be_added = self._prepare_status_check_create()
            for detail in to_be_added:
                data = self._prepare_status_check_data(
                    self.status_check_template_id.id, detail.id
                )
                self.status_check_ids.create(data)

    @api.onchange(
        "status_check_template_id",
    )
    def onchange_status_check_ids(self):
        res = []
        if self.status_check_template_id:
            res = self.create_status_check_ids()
        self.status_check_ids = res

    def create_status_check_ids(self):
        self.ensure_one()
        res = []
        obj_status_check = res = self.env["status.check"]
        status_check_ids = self._prepare_status_check_create()
        if status_check_ids:
            for status_check in status_check_ids:
                data = self._prepare_status_check_data(
                    self.status_check_template_id.id, status_check.id
                )
                res += obj_status_check.create(data)
        return res

    @api.model
    def create(self, values):
        _super = super(MixinStatusCheck, self)
        result = _super.create(values)
        if not result.status_check_template_id:
            template_id = result._get_template_status_check()
            if template_id:
                result.write({"status_check_template_id": template_id})
                result.onchange_status_check_ids()
        return result
