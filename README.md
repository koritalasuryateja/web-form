# Web Forum Backend

## Team Members
- paul john maddala
- surya teja koritala


## GitHub Repository
[Web Forum Backend Repository](https://github.com/your-username/web-forum-backend)

## Time Spent on Project
We estimate that we spent approximately 40 hours on this project.

## Testing Approach
To test our code, we employed a combination of manual testing and automated testing using Postman. We created comprehensive Postman collections for each extension, covering both positive and negative scenarios. Additionally, we wrote shell scripts to automate the testing process and ensure reproducibility.

## Known Bugs or Issues


## Difficult Issue Resolution
One challenging issue we faced was related to handling file uploads in base64 format. After thorough research and testing, we implemented a solution using a combination of base64 encoding and decoding to ensure data integrity and proper handling of file attachments.

## Extensions Implemented

### 1. Users and User Keys
#### Endpoint Added
- **POST** /user
  - Creates a new user with a private user key.
  - Request Body: `{ "username": "john_doe", "email": "john@example.com", "password": "securepassword" }`
  - Response: `{ "id": 1, "key": "randomstring", "timestamp": "2023-12-17T12:00:00Z" }`

### 2. User Profiles
#### Endpoints Added
- **GET** /user/{{id}}
  - Retrieves user metadata by user id.
  - Response: `{ "id": 1, "username": "john_doe", "email": "john@example.com", "timestamp": "2023-12-17T12:00:00Z" }`
- **PUT** /user/{{id}}/edit
  - Edits user metadata.
  - Request Body: `{ "key": "userkey", "new_username": "john_smith" }`
  - Response: `{ "id": 1, "username": "john_smith", "email": "john@example.com", "timestamp": "2023-12-17T12:30:00Z" }`

### 3. Threaded Replies
#### Modification to Existing Endpoint
- **POST** /post
  - Modified to allow specifying a post id to which the new post is replying.
  - Request Body: `{ "msg": "Replying to post", "reply_to": 1, "user_id": 1, "user_key": "userkey" }`
  - Response: `{ "id": 2, "key": "randomstring", "timestamp": "2023-12-17T13:00:00Z" }`

### 4. Date- and Time-Based Range Queries
#### Endpoint Added
- **GET** /posts/bydatetime
  - Retrieves posts based on date and time range.
  - Query Parameters: `start_datetime=2023-12-17T12:00:00Z&end_datetime=2023-12-17T13:00:00Z`
  - Response: `[ { "id": 1, "msg": "Post 1", "timestamp": "2023-12-17T12:30:00Z" }, { "id": 2, "msg": "Replying to post", "timestamp": "2023-12-17T13:00:00Z" } ]`

### 5. User-Based Range Queries
#### Endpoint Added
- **GET** /posts/byuser/{{user_id}}
  - Retrieves posts by a given user.
  - Response: `[ { "id": 1, "msg": "Post 1", "timestamp": "2023-12-17T12:30:00Z" }, { "id": 2, "msg": "Replying to post", "timestamp": "2023-12-17T13:00:00Z" } ]`

## Testing Summary

### 1. Users and User Keys
- **Positive Test**
  - Created a new user and verified the returned user id, key, and timestamp.
- **Negative Test**
  - Attempted to create a user without providing a required field, ensuring a 400 Bad Request response.

### 2. User Profiles
- **Positive Test**
  - Retrieved user metadata by user id and verified the correctness of the returned data.
- **Negative Test**
  - Attempted to edit user metadata without providing a key, ensuring a 403 Forbidden response.

### 3. Threaded Replies
- **Positive Test**
  - Created a post as a reply to an existing post and verified the correctness of the response.
- **Negative Test**
  - Attempted to create a post reply without specifying the required parameters, ensuring a 400 Bad Request response.

### 4. Date- and Time-Based Range Queries
- **Positive Test**
  - Retrieved posts within a specified date and time range and validated the correctness of the returned data.
- **Negative Test**
  - Attempted to use the date and time range query without providing the required parameters, ensuring a 400 Bad Request response.

### 5. User-Based Range Queries
- **Positive Test**
  - Retrieved posts by a given user id and verified the correctness of the returned data.
- **Negative Test**
  - Attempted to use the user-based range query without providing the required parameters, ensuring a 400 Bad Request response.

## Conclusion
In conclusion, our web forum backend implementation successfully incorporates the baseline behavior and five extensions, each thoroughly tested to ensure robust functionality. The provided documentation outlines the added endpoints, their expected behavior, and detailed testing summaries for each extension.
