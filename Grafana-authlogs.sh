

 #!/bin/bash

 LOGFILE="/var/lib/docker/containers/5560ef880de15bb6932db192ce2524a185c59d21d17b93ee901f9243ea5e514c/5560ef880de15bb6932db192ce2524a185c59d21d17b93ee901f9243ea5e514c-json.l
og"
PATTERN="Successful Login"
THRESHOLD=3
EMAIL="olusholaayoade1@gmail.com"

COUNT=$(tail -n 1000 "$LOGFILE" | grep -c "$PATTERN")

if [ "$COUNT" -ge "$THRESHOLD" ]; then
    echo "Alert: $COUNT successful logins detected in the last 5 minutes." | \
    mail -s "Grafana Login Alert - $(hostname)" "$EMAIL"
    fi

 # Example log line:
 # {"log":"t=2023-10-10T12:34:56+0000 lvl=info msg=\"Successful Login\" User=admin@localhost\n","stream":"stdout","time":"2023-10-10T12:34:56.789012345Z"}
 # Extracted relevant part:
 # "t=2023-10-10T12:34:56+0000 lvl=info