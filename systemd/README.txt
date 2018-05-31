Installation instructions

NOTE: You will need superuser privileges to complete these operations

1. Edit atlantis.service file to make sure both path and user are correctly set
2. Copy atlantis.service to /etc/systemd/system
3. Execute:
  $ systemctl daemon-reload
  $ systemctl enable atlantis.service
  $ systemctl start atlantis.service
