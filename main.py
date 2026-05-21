# Import required libraries
import json
import unittest
import datetime


# Load JSON files using UTF-8 encoding
with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


# Convert Format 1 to unified format
def convertFromFormat1(jsonObject):

    # Split location string into parts
    locationParts = jsonObject["location"].split("/")

    # Create unified JSON structure
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# Convert Format 2 to unified format
def convertFromFormat2(jsonObject):

    # Convert ISO timestamp string to datetime object
    dt = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    # Set timezone explicitly to UTC
    dt = dt.replace(tzinfo=datetime.timezone.utc)

    # Convert datetime to milliseconds since epoch
    timestamp = int(dt.timestamp() * 1000)

    # Create unified JSON structure
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }

    return result


# Main conversion function
def main(jsonObject):

    # Detect input format automatically
    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)

    return convertFromFormat2(jsonObject)


# Unit Tests
class TestSolution(unittest.TestCase):

    # Sanity check
    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))

        self.assertEqual(
            result,
            jsonExpectedResult
        )

    # Test conversion from format 1
    def test_dataType1(self):

        result = main(jsonData1)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 1 failed"
        )

    # Test conversion from format 2
    def test_dataType2(self):

        result = main(jsonData2)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 2 failed"
        )


# Run unit tests
if __name__ == "__main__":
    unittest.main()
