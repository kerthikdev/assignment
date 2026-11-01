# Terminal Execution Log

## B0 — Terraform Count Problem and Migration

### Final Terraform plan verification

**Command executed:**

```bash
terraform -chdir=terraform plan -refresh=false
```

**Actual terminal output:**

```text
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with
the following symbols:
  + create

Terraform will perform the following actions:

  # aws_s3_bucket.landlord_media[0] has moved to aws_s3_bucket.landlord_media["la-001"]
  # aws_s3_bucket.landlord_media[1] has moved to aws_s3_bucket.landlord_media["la-002"]
  # aws_s3_bucket.landlord_media[2] has moved to aws_s3_bucket.landlord_media["la-003"]
  # aws_s3_bucket.landlord_media[3] has moved to aws_s3_bucket.landlord_media["la-004"]

  # aws_s3_bucket.listing_media will be created

  # aws_s3_bucket_lifecycle_configuration.listing_media_archive will be created

Plan: 2 to add, 0 to change, 0 to destroy.
```

**Observation:**

Terraform successlfully recognizes the four existing landlord media buckets under their new `for_each` addresses using the `moved` blocks. No existing landlord media buckets are planned for destruction.

The two planned creations are the listing media bucket and its lifecycle configuration.


## B1 — S3 Glacier Lifecycle Configuration

### 1. Terraform formatting

**Command executed:**

```bash
terraform -chdir=terraform fmt -check -recursive
```

**Actual terminal output:**

```text
No output. Command completed successfully.
```

### 2. Terraform validation

**Command executed:**

```bash
terraform -chdir=terraform validate
```

**Actual terminal output:**

```text
Success! The configuration is valid.
```

### 3. Terraform plan verification

**Command executed:**

```bash
terraform -chdir=terraform plan -refresh=false
```

**Actual terminal output summary:**

```text
aws_s3_bucket.landlord_media[0] has moved to aws_s3_bucket.landlord_media["la-001"]
aws_s3_bucket.landlord_media[1] has moved to aws_s3_bucket.landlord_media["la-002"]
aws_s3_bucket.landlord_media[2] has moved to aws_s3_bucket.landlord_media["la-003"]
aws_s3_bucket.landlord_media[3] has moved to aws_s3_bucket.landlord_media["la-004"]

aws_s3_bucket.listing_media will be created

aws_s3_bucket_lifecycle_configuration.listing_media_archive will be created

Plan: 2 to add, 0 to change, 0 to destroy.
```

### Observations

1. Terraform successfully validates the lifecycle configuration.
2. The lifecycle rule uses the tag filter `archive_eligible=true`.
3. Eligible objects are configured to transition to S3 Glacier Flexible Retrieval after 30 days.
4. Existing landlord media buckets are preserved through Terraform state migration.
5. No existing resources are planned for destruction.

**Note:** This is a Terraform plan verification. No resources were applied to AWS.

## B2 — Access Control

### 1. Access control test execution

**Command executed:**

```bash
python3 -m pytest tests/test_access_control.py -v
```

**Actual terminal output:**

```text
================================================ test session starts =================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 2 items

tests/test_access_control.py::test_manager_cannot_access_another_landlords_report PASSED [ 50%]
tests/test_access_control.py::test_manager_can_access_own_landlords_report PASSED [100%]

================================================= 2 passed in 0.01s ==================================================
```

**Observation:**

- A PropertyManager belonging to `la-001` is denied access to a screening report belonging to `la-002`.
- The same PropertyManager is allowed to access a screening report belonging to `la-001`.
- Both access-control test cases passed successfully.


### 2. Cost Tag Checker — First Execution

**Command executed:**

```bash
python3 scripts/cost_tag_check.py fixtures/plan.json
```

**Actual terminal output:**

```text
MISSING TAG: aws_s3_bucket.listing_media - landlord_account_id
MISSING TAG: aws_lambda_function.mls_feed_sync - landlord_account_id
```

**Observation:**

The checker identified two resources missing the required `landlord_account_id` billing tag:

1. `aws_s3_bucket.listing_media`
2. `aws_lambda_function.mls_feed_sync`

The correctly tagged resources were not reported.

The script returned a validation failure because two resources are missing the required tag.

### 3. Cost Tag Checker — Second Execution (Idempotency Verification)

**Command executed:**

```bash
python3 scripts/cost_tag_check.py fixtures/plan.json
```

**Actual terminal output:**

```text
MISSING TAG: aws_s3_bucket.listing_media - landlord_account_id
MISSING TAG: aws_lambda_function.mls_feed_sync - landlord_account_id
```

**Observation:**

The checker was executed twice against the same Terraform plan file.

Both executions produced identical output and identified the same two resources missing the required `landlord_account_id` tag.

No additional duplicate findings appeared.

This verifies deterministic and repeatable behavior across executions. The checker does not modify the Terraform plan file.


## Final Test Suite Verification

### Complete Python test suite

**Command executed:**

```bash
python3 -m pytest -v
```

**Actual terminal output:**

```text
================================================ test session starts =================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/kerthik/Downloads/Playground/haven-platform-assessment
collected 4 items

tests/test_access_control.py::test_manager_cannot_access_another_landlords_report PASSED [ 25%]
tests/test_access_control.py::test_manager_can_access_own_landlords_report PASSED [ 50%]
tests/test_cost_tag_check.py::test_cost_tag_check_happy_path PASSED [ 75%]
tests/test_cost_tag_check.py::test_cost_tag_check_is_idempotent PASSED [100%]

================================================= 4 passed in 0.01s ==================================================
```

**Observation:**

All four tests passed successfully.

- Access-control authorization and denial scenarios passed.
- Cost-tag validation correctly identified missing billing tags.
- Repeated cost-tag checks produced consistent results.

The complete Python test suite finished without failures.