"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""
from app.access_control import can_access_screening_report

from app.access_control import can_access_screening_report


def test_manager_cannot_access_another_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    manager = property_managers[0]  
    report = screening_reports[1]  

    result = can_access_screening_report(
        manager,
        report,
        properties=properties,
        tenants=tenants,
    )

    assert result is False


def test_manager_can_access_own_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    manager = property_managers[0] 
    report = screening_reports[0]   

    result = can_access_screening_report(
        manager,
        report,
        properties=properties,
        tenants=tenants,
    )

    assert result is True
