clusterName: ${cluster_name}
clusterLocation: ${cluster_location}
%{ if gcp_service_account_secret != "" }
gcpServiceAccountSecret:
  enabled: true
  name: ${gcp_service_account_secret}
  key: application_default_credentials.json
%{ endif ~}
image:
  pullPolicy: ${pull_policy}
resources:
  limits:
    cpu: 300m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi
tolerations:
- operator: Exists
  effect: NoSchedule
