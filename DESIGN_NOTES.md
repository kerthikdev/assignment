# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide a plan has already been
checked/reported on. Use the word "idempotency" in your explanation.



I use a Python set called `reported_addresses` to keep track of resource addresses that have already been reported during the current execution. If the same resource address appears again, it will not be reported twice.

For idempotency across repeated executions, the script does not modify the Terraform plan or maintain a separate database or tracking file. It reads the same plan and produces the same findings and exit code every time it runs.

One limitation is that the script does not persist a record of previously checked plans. Its duplicate prevention is limited to a single execution, while repeated executions remain deterministic.

## Any other decision with a non-obvious alternative

One important decision in `cost_tag_check.py` is that I check only resources with `create` or `update` actions.

I do not check resources that are only being deleted because a resource being removed does not need to receive a new billing tag. Checking deletion-only resources could produce unnecessary warnings.

I also check the resource's `after` values because they represent the resource configuration after Terraform applies the planned change. This helps verify whether the required `landlord_account_id` tag will exist after the operation.

Another important decision in access control is to compare the PropertyManager's `landlord_account_id` with the ScreeningReport's `landlord_account_id`, rather than relying only on a property ID or manager ID. This follows the domain model because the LandlordAccount is the main ownership and billing boundary.

These decisions keep the checks aligned with the actual business rules of the application.
