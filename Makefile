# API URL
APP_URL = http://localhost:8888/productionplan

# Test payload files
PAYLOAD_FILE1 = ./utils/payload1.json
PAYLOAD_FILE2 = ./utils/payload2.json
PAYLOAD_FILE3 = ./utils/payload3.json


# Start the application
all:
	cd srcs && docker compose up --build

# Stop the application
down:
	cd srcs && docker compose down -v

# Send test requests
send-request1:
	curl -X POST $(APP_URL) -H "Content-Type: application/json" -d @$(PAYLOAD_FILE1)
send-request2:
	curl -X POST $(APP_URL) -H "Content-Type: application/json" -d @$(PAYLOAD_FILE2)
send-request3:
	curl -X POST $(APP_URL) -H "Content-Type: application/json" -d @$(PAYLOAD_FILE3)
