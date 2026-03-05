# Document your edge case here
# Edge Case

## Updating a student with empty fields

The specification does not clearly define what should happen if a PUT request is sent with empty fields (e.g., name = "" or course = "").

I chose to treat empty strings as "no update" rather than overwriting the existing value with an empty string.

For example:
If a user sends:
{
  "name": "",
  "course": "COMP1531"
}

The name will remain unchanged, and only the course will be updated.

This behaviour is handled inside the db.update_student() function, where empty strings are ignored and the existing value is preserved.

Reasoning:
This prevents accidental data loss and ensures that partial updates behave safely and predictably.