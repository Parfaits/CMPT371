read -p "Port number >" PORTNUM

kill $(lsof -t -i:$PORTNUM)