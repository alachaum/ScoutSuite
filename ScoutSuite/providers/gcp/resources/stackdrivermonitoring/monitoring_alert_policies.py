from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class MonitoringAlertPolicies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_alert_policies = await self.facade.stackdrivermonitoring.get_alert_policies(self.project_id)
        alert_policy = self._parse_alert_policy(raw_alert_policies)
        self[self.project_id] = alert_policy

    def _parse_alert_policy(self, raw_alert_policies):
        alert_policy_dict = {}
        alert_policy_dict['cloud_storage_iam_permission_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-cloud-storage-iam-permission-changes')
        alert_policy_dict['audit_config_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-configuration-changes')
        alert_policy_dict['custom_role_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-custom-role-changes')
        alert_policy_dict['project_ownership_assignments'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-project-ownership-assignments-changes')
        alert_policy_dict['sql_instance_conf_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-sql-instance-configuration-changes')
        alert_policy_dict['vpc_network_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-vpc-network-changes')
        alert_policy_dict['vpc_network_firewall_rule_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-vpc-network-firewall-rule-changes')
        alert_policy_dict['vpc_network_route_change'] = self._specific_alert_policy_present(raw_alert_policies, 'audit-vpc-network-route-changes')
        return alert_policy_dict

    def _specific_alert_policy_present(self, alert_policies, logging_metric_name):
        for alert_policy in alert_policies:
            for condition in alert_policy.conditions:
                if (f'metric.type = "logging.googleapis.com/user/{logging_metric_name}"' in condition.condition_threshold.filter) and alert_policy.enabled.value:
                    return True
        return False
