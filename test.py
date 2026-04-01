import json
import re
import urllib.error
import urllib.request


# Replace this with your Make.com custom webhook URL.
WEBHOOK_URL = "https://hook.eu1.make.com/your-webhook-id"


def is_valid_email(email: str) -> bool:
	"""Basic email validation for common formats."""
	pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
	return re.match(pattern, email) is not None


def send_lead_to_make(name: str, email: str, message: str, webhook_url: str = WEBHOOK_URL) -> None:
	"""Send lead data to Make.com webhook as JSON."""
	payload = {
		"Name": name,
		"Email": email,
		"Message": message,
	}

	data = json.dumps(payload).encode("utf-8")
	request = urllib.request.Request(
		webhook_url,
		data=data,
		headers={"Content-Type": "application/json"},
		method="POST",
	)

	try:
		with urllib.request.urlopen(request, timeout=15) as response:
			status_code = response.getcode()
			body = response.read().decode("utf-8", errors="replace")
			print(f"Lead sent successfully. Status: {status_code}")
			if body:
				print(f"Response: {body}")
	except urllib.error.HTTPError as error:
		error_body = error.read().decode("utf-8", errors="replace")
		print(f"HTTP error: {error.code} - {error.reason}")
		if error_body:
			print(f"Details: {error_body}")
	except urllib.error.URLError as error:
		print(f"Connection error: {error.reason}")


def main() -> None:
	name = input("Enter lead name: ").strip()
	email = input("Enter lead email: ").strip()
	message = input("Enter lead message: ").strip()

	if not name or not email or not message:
		print("All fields are required: Name, Email, Message.")
		return

	if not is_valid_email(email):
		print("Please enter a valid email address.")
		return

	if "your-webhook-id" in WEBHOOK_URL:
		print("Please set WEBHOOK_URL to your actual Make.com webhook URL first.")
		return

	send_lead_to_make(name, email, message)


if __name__ == "__main__":
	main()
