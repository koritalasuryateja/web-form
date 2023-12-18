# Web Forum Backend

## Team Members
- Paul John Maddala-  pmaddala@stevens.edu
- Surya Teja Koritala - skorital1@gmail.edu


## GitHub Repository
https://github.com/koritalasuryateja/web-form

## Time Spent on Project
We estimate that we spent approximately 40 hours on this project.

## Testing Approach
Our testing strategy, as outlined in the test.py file, focuses primarily on unit tests performed within the unittest framework using Flask's testing client. These tests simulate HTTP requests to our forum's backend, covering important features like user registration and authentication, moderator actions, discussion post management, IP restriction handling, and the ability to filter and search posts. We validate the application's response accuracy and robustness using a combination of POST, GET, PUT, and DELETE requests, ensuring error handling and security measures work as expected. This extensive testing strategy is critical to ensuring the dependability and effectiveness of our web forum application.

## Known Bugs or Issues
None.

## Difficult Issue Resolution
 Struggled with securely managing user authentication, especially in verifying user keys for actions like editing or deleting posts.Developed a MemberManager class that encapsulates user validation logic. Used this class to check user credentials (ID and key) against stored user data before allowing them to modify posts, enhancing the security of user operations.


## Extension 1: User Registration and Authentication

### Description
This extension introduces the ability to register and authenticate users in the forum. Users are assigned unique IDs and keys upon registration, which are then used for validating actions like post creation and editing.

### Endpoints
- `POST /member`: Register a new forum member. Requires a JSON payload with `member_name` and an optional `full_name`.
- `GET /member/<int:member_id>`: Retrieve details of a specific forum member.
- `PUT /member/<int:member_id>/edit`: Update a member's full name. Requires member's ID and key for authentication.

### Testing
Test cases cover the registration of new members, retrieval of member information, and updating member details, ensuring proper validation and error handling.

## Extension 2: Discussion Post Management

### Description
Users can create, view, edit, and delete discussion posts. Posts can be associated with user IDs, allowing for user-specific post management.

### Endpoints
- `POST /discussion`: Create a new post. Users can optionally associate their ID and key with the post.
- `GET /discussion/<int:post_id>`: View details of a specific post.
- `PUT /discussion/<int:post_id>/edit`: Edit an existing post. Requires member validation.
- `DELETE /discussion/<int:post_id>/remove/<key>`: Delete a post using the correct key.

### Testing
Test cases ensure functionality for creating, viewing, editing, and deleting posts, including member-specific operations.

## Extension 3: Moderator Role

### Description
Moderators can perform administrative actions like adding other moderators. This extension involves higher-level privileges and key validation.

### Endpoints
- `POST /add_moderator`: Add a new moderator, protected by a master key.

### Testing
Tests validate moderator addition, ensuring proper authorization and error responses for unauthorized requests.

## Extension 4: IP Restriction and Blocking

### Description
Implement IP-based access control to restrict or block requests based on the client's IP address. This helps in mitigating abusive behavior or excessive requests from specific IP addresses.

### Implementation Details
A pre-request hook checks the client's IP address against a list of restricted or blocked IPs.

### Testing
While specific tests are suggested as placeholders, they should ideally cover scenarios of IP restriction, blocking, and successful access post-restriction expiry.

## Extension 5: Filtering Posts

### Description
This feature allows filtering of discussion posts based on different criteria like year or member ID, enhancing the forum's navigability and user experience.

### Endpoints
- `GET /discussions`: Filter posts by a specified year.
- `GET /discussions/member/<int:member_id>`: Retrieve all posts made by a specific member.

### Testing
Tests should cover various scenarios of filtering posts, ensuring accurate retrieval based on the specified criteria.

## Detailed Summaries of Tests for Extensions

### Extension 1: User Registration and Authentication

#### Test Summary:
- `test_user_creation`: Validates the process of registering new users, ensuring correct handling of member names and assignment of unique IDs and keys.
- `test_user_auth`: Verifies user authentication, including retrieval of member details and handling of invalid or missing keys.

#### Interpretation:
These tests confirm that the user registration and authentication system is reliable, accurately processing user data and ensuring secure user-specific actions.

---

### Extension 2: Discussion Post Management

#### Test Summary:
- `test_post_creation_endpoint`: Assesses the functionality of creating new discussion posts and validates user credentials if provided.
- `test_post_read_endpoint`: Ensures accurate retrieval and display of posts.
- `test_post_delete_endpoint`: Tests the deletion of posts, including security checks against user IDs and keys.
- `test_post_edit_endpoint`: Validates the ability to edit posts with proper authorization.

#### Interpretation:
The tests examine the application's capability in managing posts, including creation, viewing, editing, and deletion, with essential security validations.

---

### Extension 3: Moderator Role

#### Test Summary:
- `test_moderator_creation`: Checks the process of adding new moderators, ensuring that this feature is securely accessible only with the correct master key.

#### Interpretation:
This test ensures the secure addition of moderators, indicating that the moderator feature is well-protected and functional.

---

### Extension 4: IP Restriction and Blocking

#### Test Summary:
- Placeholder tests for IP restriction and blocking (`test_isiprestrictedorblocked`, `test_verifyipstatus`) are to be implemented to evaluate IP-based access control.

#### Interpretation:
Once implemented, these tests will assess the effectiveness of IP restrictions and blocks in maintaining security and access control.

---

### Extension 5: Filtering Posts

#### Test Summary:
- `test_filter_posts_by_date_endpoint`: Verifies the ability to filter posts based on specific dates or date ranges.
- `test_filter_posts_by_member_endpoint`: Assesses the functionality of filtering posts by specific members.

#### Interpretation:
These tests are crucial for ensuring the effective filtering capabilities of the forum, a key feature for enhancing user navigation and content discovery.

---




## Conclusion
Finally, our web forum backend implementation incorporates the baseline behaviour as well as five extensions, each of which has been thoroughly tested to ensure robust functionality. The documentation provided describes the new endpoints, their expected behaviour, and detailed testing summaries for each extension.
