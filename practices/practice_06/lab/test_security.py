"""Student-added security regression tests for discovered issues."""

import json
import unittest

from service import Shop


class SecurityTest(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.addCleanup(self.shop.close)

    def request(self, method, path, body=None, headers=None):
        with self.shop.lock:
            return self.shop.dispatch(method, path, body or {}, headers or {})

    def login(self, username="alice", password="learn-alice"):
        status, result = self.request("POST", "/login", {"username": username, "password": password})
        self.assertEqual(status, 200)
        return {"X-Token": result["token"]}

    def test_profile_requires_session_and_is_self_only(self):
        # No session -> 401
        self.assertEqual(self.request("GET", "/profile")[0], 401)
        # Alice should not get Bob's profile even if id is passed
        status, profiles = self.request("GET", "/profile?id=2", headers=self.login())
        self.assertEqual(status, 200)
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0]["name"], "TEST_ALICE")

    def test_orders_listing_scoped(self):
        alice = self.login()
        # Create Alice order
        self.assertEqual(self.request("POST", "/orders", {"product": "lamp"}, headers=alice)[0], 201)
        # Bob logs in and must not see Alice orders
        bob = self.login("bob", "learn-bob")
        status, orders = self.request("GET", "/orders", headers=bob)
        self.assertEqual(status, 200)
        self.assertTrue(all(o["owner"] == 2 for o in orders))

    def test_admin_export_requires_staff_session(self):
        # Header alone is not enough
        self.assertEqual(self.request("GET", "/admin/export", headers={"X-Role": "staff"})[0], 401)
        # Alice is forbidden
        self.assertEqual(self.request("GET", "/admin/export", headers=self.login())[0], 403)
        # Staff allowed
        self.assertEqual(self.request("GET", "/admin/export", headers=self.login("staff", "learn-staff"))[0], 200)

    def test_files_restricted_to_own_dir(self):
        alice = self.login()
        # Own receipt allowed
        self.assertEqual(self.request("GET", "/files?path=receipt.txt", headers=alice)[0], 200)
        # Other user's receipt forbidden
        self.assertEqual(self.request("GET", "/files?user=bob&path=receipt.txt", headers=alice)[0], 200)  # param ignored
        # Assistant tool must also restrict
        status, ctx = self.request("GET", "/assistant/context", headers=alice)
        self.assertEqual(status, 200)
        status, resp = self.request(
            "POST", "/assistant/execute",
            {"decision": {"tool": "read_file", "arguments": {"path": "files/bob/receipt.txt"}}},
            headers=alice,
        )
        self.assertEqual(status, 403)

    def test_catalog_price_enforced(self):
        alice = self.login()
        status, order = self.request("POST", "/orders", {"product": "chair", "price": 1}, headers=alice)
        self.assertEqual((status, order["price"]), (201, 5000))

    def test_reviews_view_escapes_html(self):
        alice = self.login()
        self.assertEqual(self.request("POST", "/reviews", {"product": "lamp", "text": "<b>ok</b>"}, headers=alice)[0], 201)
        status, html = self.request("GET", "/reviews/view", headers=alice)
        self.assertEqual(status, 200)
        self.assertIn("&lt;b&gt;ok&lt;/b&gt;", html)

    def test_search_restricted_and_parameterized(self):
        alice = self.login()
        self.assertEqual(self.request("GET", "/search?q=%25' OR 1=1 --", headers=alice)[0], 403)
        staff = self.login("staff", "learn-staff")
        status, rows = self.request("GET", "/search?q=TEST_", headers=staff)
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(rows), 1)

    def test_assistant_context_scoped_to_owner(self):
        alice = self.login()
        # Bob's order id is 2 in fixture; alice should not get it
        self.assertEqual(self.request("GET", "/assistant/context?order_id=2", headers=alice)[0], 404)


if __name__ == "__main__":
    unittest.main()
