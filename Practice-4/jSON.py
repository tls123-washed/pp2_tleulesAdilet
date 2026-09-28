
import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20}  {'Speed':<6}  {'MTU':<6}")
print(f"{'-' * 50} {'-' * 20}  {'-' * 6}  {'-' * 6}")

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    print(f"{attrs['dn']:<50} {attrs['descr']:<20}  {attrs['speed']:>7}  {attrs['mtu']:>5}")