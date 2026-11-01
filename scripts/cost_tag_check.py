"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or changed (skip anything not in
    change.actions, e.g. a pure "no-op" / "read" change).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""


import json
import sys


REQUIRED_TAG = "landlord_account_id"


def check_plan(plan_path: str) -> int:
    """
    Read a Terraform JSON plan and check whether every resource
    being created or updated has the required landlord billing tag.

    Returns:
        0: All checked resources have the required tag.
        1: One or more resources are missing the required tag.
    """

    # Step 1: Open and read the Terraform JSON file
    with open(plan_path, "r") as file:
        plan = json.load(file)

    # Step 2: Get all resource changes
    resource_changes = plan.get("resource_changes", [])

    # Step 3: Create a list to store missing resources
    missing_resources = []

    # Step 4: Create a set to prevent duplicate findings
    reported_addresses = set()

    # Step 5: Check each resource one by one
    for resource in resource_changes:

        # Get the change information
        change = resource.get("change", {})

        # Get Terraform actions
        actions = change.get("actions", [])

        # Check only resources being created or updated
        if not any(action in actions for action in ("create", "update")):
            continue

        # Get the resource address
        address = resource.get("address", "<unknown>")

        # Get the resource details after the change
        after = change.get("after") or {}

        # Get the resource tags
        tags = after.get("tags") or {}

        # Check whether landlord_account_id exists
        if not tags.get(REQUIRED_TAG):

            # Avoid reporting the same resource twice
            if address not in reported_addresses:

                # Store the missing resource
                missing_resources.append(address)

                # Remember that this address was reported
                reported_addresses.add(address)

    # Step 6: Print resources missing the required tag
    for address in missing_resources:
        print(f"MISSING TAG: {address} - {REQUIRED_TAG}")

    # Step 7: Return the exit code
    if missing_resources:
        return 1

    print("SUCCESS: All checked resources have the required tag.")
    return 0


# Execute the function when running this file directly
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/cost_tag_check.py <plan.json>")
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))
