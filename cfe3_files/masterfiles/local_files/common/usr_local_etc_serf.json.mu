{
  "tags": {
    "role": "{{vars.example.role}}"
  },
  {{^classes.am_role_loadbalancer}}
  "retry_join": {{%vars.example.node_ips}},
  {{/classes.am_role_loadbalancer}}
  "retry_max_attempts": 60,
  "retry_interval": "1s",
  "bind": "{{vars.example.eth_ip}}",
  "snapshot_path": "/var/lib/misc/serf-snapshot",
  "rejoin_after_leave": true
}
