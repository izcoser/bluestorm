import unittest
import sqlite3
import hashlib
from api import app


class TestEndPoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        instance = app.test_client()
        auth_token = "E4L1DK95K55OZL3"  # Em produção, obter esse token com uma variável de ambiente ou
        # ou arquivo em .gitignore.
        cls.response_patients = instance.get("/patients", headers={"token": auth_token})
        cls.response_patients_no_auth = instance.get("/patients")
        cls.response_patients_bad_auth = instance.get(
            "/patients", headers={"token": "wrong"}
        )
        cls.response_token_creation = instance.post("/create_auth")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_patients(self):
        self.assertEqual(self.response_patients.status_code, 200)
        self.assertEqual(len(self.response_patients.get_json()), 50)

    def test_patients_no_auth(self):
        self.assertEqual(self.response_patients_no_auth.status_code, 401)

    def test_patients_wrong_auth(self):
        self.assertEqual(self.response_patients_bad_auth.status_code, 401)

    def test_token_creation(self):
        self.assertEqual(self.response_token_creation.status_code, 200)
        token = self.response_token_creation.get_json()["token"]
        self.assertEqual(len(token), 15)
        h = hashlib.md5(token.encode("utf-8")).hexdigest()
        conn = sqlite3.connect("backend_test.db", check_same_thread=False)
        self.assertTrue(
            len(
                conn.execute(f"SELECT * FROM auth WHERE token_hash =?", (h,)).fetchall()
            )
            > 0
        )
        conn.execute("DELETE FROM auth WHERE token_hash = ?", (h,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    unittest.main()
