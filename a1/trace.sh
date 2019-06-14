read NUM

echo "Tracing route..."
traceroute www.utoronto.ca > "trace_utoronto_$NUM.txt"
echo "Route traced."
echo -e "\nPrinting date/time..."
echo -e "\nDate traced:" >> "trace_utoronto_$NUM.txt"
date >> "trace_utoronto_$NUM.txt"
echo "Date/time printed. End trace."