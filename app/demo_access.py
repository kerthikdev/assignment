from app.models import PropertyManager, Property, Tenant, ScreeningReport
from app.access_control import can_access_screening_report


# 1. Create property managers
property_managers = [
    PropertyManager(
        id="pm-001",
        name="Asha Rao",
        landlord_account_id="la-001"
    ),
    PropertyManager(
        id="pm-002",
        name="Leo Fontaine",
        landlord_account_id="la-002"
    )
]


# 2. Create properties
properties = [
    Property(
        id="prop-001",
        landlord_account_id="la-001",
        address="Chennai Property"
    ),
    Property(
        id="prop-002",
        landlord_account_id="la-002",
        address="Salem Property"
    )
]


# 3. Create tenants
tenants = [
    Tenant(
        id="ten-001",
        name="Tenant One",
        property_id="prop-001"
    ),
    Tenant(
        id="ten-002",
        name="Tenant Two",
        property_id="prop-002"
    )
]


# 4. Create screening reports
screening_reports = [
    ScreeningReport(
        id="rep-001",
        tenant_id="ten-001",
        ssn_last4="1234",
        credit_score=710
    ),
    ScreeningReport(
        id="rep-002",
        tenant_id="ten-002",
        ssn_last4="5678",
        credit_score=690
    )
]


# 5. Ask the user for input
manager_id = input("Enter Manager ID: ")
report_id = input("Enter Report ID: ")


# 6. Find manager
manager = next(
    (m for m in property_managers if m.id == manager_id),
    None
)

# 7. Find report
report = next(
    (r for r in screening_reports if r.id == report_id),
    None
)


# 8. Check access
if manager is None:
    print("Manager not found")

elif report is None:
    print("Report not found")

else:
    result = can_access_screening_report(
        manager,
        report,
        properties=properties,
        tenants=tenants
    )

    print("\n----- ACCESS CONTROL RESULT -----")

    print("Manager:", manager.name)
    print("Report:", report.id)
    print("Access Allowed:", result)

    if result:
        print("Status: ACCESS GRANTED")
    else:
        print("Status: ACCESS DENIED")