[Unit]
Description=Service orchestration and management tool
After=syslog.target
After=network.target

[Service]
Type=simple
ExecStart=/bin/sh -c "exec &>> /var/log/serf.log /usr/local/bin/serf agent -config-file=/usr/local/etc/serf.json"
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
