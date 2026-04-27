# Nexus UI Testing Guide

## Overview

Two comprehensive test suites have been created for testing the Nexus social media application:

1. **tests_ui.py** - Django test client tests (Form & View testing)
2. **tests_selenium.py** - Selenium browser automation tests

---

## Running Tests

### Django UI Tests (Recommended for CI/CD)

Run all UI tests:
```bash
./venv/bin/python manage.py test nexusapp.tests_ui -v 2
```

Run specific test class:
```bash
./venv/bin/python manage.py test nexusapp.tests_ui.UIAuthenticationTests -v 2
```

Run a single test:
```bash
./venv/bin/python manage.py test nexusapp.tests_ui.UIAuthenticationTests.test_login_flow -v 2
```

### Django UI Test Coverage

The following test cases are available:

#### **Authentication Tests** (`UIAuthenticationTests`)
- ✅ test_registration_page_loads - Verify registration page renders
- ✅ test_user_registration_flow - Complete registration flow
- ✅ test_login_page_loads - Verify login page renders
- ✅ test_user_login_flow - Complete login flow
- ✅ test_login_with_invalid_credentials - Verify error handling
- ✅ test_logout_flow - User logout functionality

#### **Profile Tests** (`UIProfileTests`)
- ✅ test_profile_page_loads - View user profile
- ✅ test_edit_profile_page_loads - Edit profile page
- ✅ test_edit_profile_updates_bio - Update profile information
- ✅ test_home_feed_loads - Home feed page

#### **Post Tests** (`UIPostTests`)
- ✅ test_create_post_page_loads - Create post page
- ✅ test_create_post_flow - Create a new post
- ✅ test_post_detail_page_loads - View post details
- ✅ test_edit_post_page_loads - Edit post page
- ✅ test_delete_post_flow - Delete a post

#### **Follow Tests** (`UIFollowTests`)
- ✅ test_follow_user_flow - Follow a user
- ✅ test_unfollow_user_flow - Unfollow a user
- ✅ test_view_followers_page - View followers list
- ✅ test_view_following_page - View following list

#### **Interaction Tests** (`UIInteractionTests`)
- ✅ test_like_post_flow - Like a post
- ✅ test_comment_on_post_flow - Comment on a post

#### **Explore Tests** (`UIExploreTests`)
- ✅ test_explore_page_loads - Explore page
- ✅ test_notifications_page_loads - Notifications page

---

## Selenium Browser Tests

### Setup

1. Install Selenium and webdriver-manager:
```bash
./venv/bin/python -m pip install selenium webdriver-manager
```

2. Run Selenium tests:
```bash
./venv/bin/python manage.py test nexusapp.tests_selenium -v 2
```

### Browser Test Coverage

#### **Selenium Authentication Tests**
- test_login_with_browser - Real browser login
- test_logout_with_browser - Real browser logout

#### **Selenium Profile Tests**
- test_view_profile_in_browser - View profile in real browser
- test_edit_profile_in_browser - Edit profile in real browser

#### **Selenium Post Tests**
- test_create_post_in_browser - Create post with file upload

#### **Selenium Navigation Tests**
- test_navigation_menu_in_browser - Test menu navigation

### Running in Headless Mode

For CI/CD or servers without display, uncomment this line in `tests_selenium.py`:
```python
chrome_options.add_argument("--headless")
```

---

## Test Output Example

```
test_login_page_loads (nexusapp.tests_ui.UIAuthenticationTests.test_login_page_loads)
Test login page is accessible ... ok

test_user_login_flow (nexusapp.tests_ui.UIAuthenticationTests.test_user_login_flow)
Test complete user login flow ... ok

Ran 6 tests in 3.501s
OK
```

---

## Manual Testing Checklist

For manual testing, visit: **http://127.0.0.1:8000/**

### Authentication
- [ ] Navigate to `/register/` and create a new account
- [ ] Login with created credentials
- [ ] Logout and verify redirect
- [ ] Try login with wrong password

### Profile
- [ ] View your profile at `/profile/<username>/`
- [ ] Edit profile and update bio
- [ ] Upload profile picture
- [ ] View follower/following lists

### Posts
- [ ] Create a new post with image
- [ ] Edit existing post
- [ ] Delete a post
- [ ] View post details

### Social Features
- [ ] Follow another user
- [ ] Unfollow a user
- [ ] Like a post
- [ ] Comment on a post
- [ ] View notifications
- [ ] Explore feed

### Messages (if implemented)
- [ ] Send message to another user
- [ ] View message history
- [ ] Mark messages as read

---

## Debugging Tests

### Run with more verbose output:
```bash
./venv/bin/python manage.py test nexusapp.tests_ui -v 3
```

### Keep database after tests (for debugging):
```bash
./venv/bin/python manage.py test nexusapp.tests_ui --keepdb
```

### Run with Python debugging:
```bash
./venv/bin/python -m pdb manage.py test nexusapp.tests_ui
```

---

## Adding New Tests

To add new tests, edit `nexusapp/tests_ui.py` and follow this pattern:

```python
def test_new_feature(self):
    """Describe what the test does"""
    response = self.client.get(reverse('nexusapp:view_name'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'nexusapp/template.html')
    # Add your assertions here
```

---

## Test Database

- Tests use an isolated test database
- Database is cleaned up after tests complete
- Use `--keepdb` flag to preserve database between test runs

---

## Continuous Integration

For GitHub Actions or other CI systems:

```yaml
- name: Run Tests
  run: |
    ./venv/bin/python manage.py test nexusapp.tests_ui -v 2
```

---

## Notes

- Django tests don't require a running server (they test views directly)
- Selenium tests require either Chrome/Chromium browser or ChromeDriver installed
- All tests are isolated and can run in any order
- Tests use transactions to ensure database isolation

---

## Troubleshooting

**Issue**: Tests fail with "relation does not exist"
- Solution: Ensure migrations are applied: `./venv/bin/python manage.py migrate`

**Issue**: Selenium tests timeout
- Solution: Increase wait time or check if Chrome/Chromium is installed

**Issue**: "socialaccount is not a registered tag library"
- Solution: Already fixed by uninstalling django-allauth

---

Created: April 27, 2026
Last Updated: April 27, 2026
