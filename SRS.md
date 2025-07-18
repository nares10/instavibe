# 📄 Software Requirements Specification (SRS)

### Project: Instagram Clone Web Application

### Version: 1.0

### Date: July 18, 2025

---

## 1. **Introduction**

### 1.1 Purpose

The purpose of this document is to specify the functional and non-functional requirements for the Instagram Clone Web Application. This app replicates core features of Instagram such as user registration, image sharing, likes, comments, and user following.

### 1.2 Scope

This application allows users to:

- Create accounts and log in
- Post images and captions
- Like and comment on posts
- Follow/unfollow other users
- View a feed of posts from followed users
- Edit profile and manage posts

### 1.3 Intended Audience

- Developers
- Testers
- Project managers
- UI/UX designers

### 1.4 Definitions

- **Post**: An image uploaded by a user with optional caption.
- **Feed**: A chronological stream of posts from followed users.
- **Like**: A user interaction indicating appreciation.
- **Comment**: A textual remark on a post.

---

## 2. **Overall Description**

### 2.1 Product Perspective

This is a standalone web application developed using:

- **Frontend**: Simple htmL , tailwind-css and JAVAScipt.
- **Backend**: Django
- **Database**: PostgreSQL

### 2.2 Product Functions

- User account management
- Image upload and display
- Post interactions (like, comment)
- Follower/following system
- Feed generation
- Notifications (optional)

### 2.3 User Classes

- **Registered User**: Can post, like, comment, follow others
- **Guest**: Can only browse limited public content (if enabled)
- **Admin**: Has access to manage content and users

### 2.4 Operating Environment

- Web Browsers: Chrome, Firefox, Safari

---

## 3. **System Features and Requirements**

### 3.1 User Registration and Authentication

**Description**: Users can sign up and log in via email/password and social integration via google and facebook.

**Functional Requirements**:

- FR1: Users can register with a valid email and password
- FR1.5: User can in or register with other social account Google and Facebook.
- FR2: Users can log in securely
- FR3: Passwords are stored hashed

### 3.2 Profile Management

**Description**: Users can view and update their profile.

**Functional Requirements**:

- FR4: Users can upload profile pictures
- FR5: Users can update bio and other profile info

### 3.3 Post Creation and Management

**Description**: Users can create and delete posts.

**Functional Requirements**:

- FR6: Users can upload images with captions
- FR7: Posts can be deleted or edited by the owner

### 3.4 Feed

**Description**: A timeline of posts from followed users.

**Functional Requirements**:

- FR8: Feed is sorted in reverse chronological order
- FR9: Users see posts from followed users only

### 3.5 Like and Comment

**Description**: Users can like and comment on posts.

**Functional Requirements**:

- FR10: Each user can like/unlike a post
- FR11: Users can add and delete their own comments

### 3.6 Follow System

**Description**: Users can follow/unfollow others.

**Functional Requirements**:

- FR12: Users can follow/unfollow users
- FR13: Follower and following counts are shown

### 3.7 Notifications (Optional)

**Description**: Users are notified of likes, follows, comments

**Functional Requirements**:

- FR14: Real-time or queued notifications for user interactions related you.-

---

## 4. **Non-Functional Requirements**

## 5. **External Interface Requirements**

### 5.1 UI/UX

- Built with HTMX, tailwind-css and vanila JS
- Modern, minimal design similar to Instagram

### 5.2 Backend technology:

- framework: Django

### 5.3 Hardware Interfaces

- Not applicable (cloud hosted)

---

## 6. **Appendix**

- A. Use Case Diagrams
- B. ER Diagram for database schema
- C. API Documentation (Swagger/Postman)