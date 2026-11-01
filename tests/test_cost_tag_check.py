"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export).
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

Use a test double / your own in-memory plan dict where you don't need a real file on disk —
you don't need to shell out to the real script for every case.
"""
from pathlib import Path
from scripts.cost_tag_check import check_plan


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAN_FILE = PROJECT_ROOT / "fixtures" / "plan.json"


def test_cost_tag_check_happy_path(capsys):

    # Execute the cost-tag check
    exit_code = check_plan(str(PLAN_FILE))

    # Capture printed output
    output = capsys.readouterr().out

    # Verify that the check detects missing tags
    assert exit_code == 1

    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output

    # Verify correctly tagged resources are not flagged
    assert "aws_s3_bucket.landlord_media[0]" not in output
    assert "aws_lambda_function.screening_report_export" not in output


def test_cost_tag_check_is_idempotent(capsys):

    # First execution
    first_exit_code = check_plan(str(PLAN_FILE))
    first_output = capsys.readouterr().out

    # Second execution
    second_exit_code = check_plan(str(PLAN_FILE))
    second_output = capsys.readouterr().out

    # Both executions should return the same exit code
    assert first_exit_code == second_exit_code

    # Both executions should produce exactly the same output
    assert first_output == second_output

    # Exactly two missing resources should be reported
    assert first_output.count("MISSING TAG:") == 2
