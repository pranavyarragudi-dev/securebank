INSERT INTO user_role (id, name, description)
VALUES 
  (1, 'admin', 'Administrator with full access'),
  (2, 'customer', 'Regular banking user')
ON CONFLICT DO NOTHING;

INSERT INTO "user" (username, email, password_hash, first_name, last_name, phone, is_active, role_id)
VALUES 
  ('admin', 'admin@securebank.com', 'scrypt:32768:8:1$x54aXbM5ZFV2ywYK$a7587a55550f2e6a00095e7423feb7d5a6475fee20dad152af703261a3d90d1f3ad1020ae38300ff961a20dd40f10ece1739b497e5cba97f8c33af441a0ae3db', 'System', 'Admin', '9999999999', TRUE, 1)
ON CONFLICT DO NOTHING;
