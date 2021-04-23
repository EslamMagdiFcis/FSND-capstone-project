import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


EXECUTIVE_PRODUCER_TOKEN = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhfMHN2cWpULVA5eFZ1a0NyU2k2cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uYnA5Z3h2cS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA3ZmU2NGVhZWFiNzkwMDY4YjA3ZjRhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTYxOTEzMDgwNCwiZXhwIjoxNjE5MTM4MDA0LCJhenAiOiJPZzR1NFlWNVRiejBjaU9WZ0hYVmhEUDVWbkZVbE5jQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.rEQresdDZ48BX7RU_yPGf5rYDQru17IOaBSoVQZ3rOQNwZxq9BYX1vQGGBHkRp9zPx3awaeoZzP0nKxfkOivInGuJdvOLdJWh_8kHZQUU9IFQhG-hPytoM3pXhVIRwXpndzvOkJm4aPiawe12cQf_RFpY2KIMOOZ-07r7_AvrzlreB-G7dsuC2ymEkNVpvS7OkoJvwz0j5TPFB0hUKa6j01u605u69_fjmWjpq0O73XD__cufyor6GkMVykGlpsA68N9V33F-EtUw0HLvU6YETJ9bJ6J2ZwnJhx_NdR0jMYBP0DsMMD0o_0JZxkOhDQyMYeniSX4EIvOLaG8EU2eFw'
EXECUTIVE_PRODUCER_HEADER = { 'Authorization': EXECUTIVE_PRODUCER_TOKEN }


CASTING_ASSISTANT_TOKEN = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhfMHN2cWpULVA5eFZ1a0NyU2k2cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uYnA5Z3h2cS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA3ZmUxMzM1YzcxNGMwMDZmYjAyZjAxIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTYxOTE2ODc3OSwiZXhwIjoxNjE5MTc1OTc5LCJhenAiOiJPZzR1NFlWNVRiejBjaU9WZ0hYVmhEUDVWbkZVbE5jQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.aovV95Aqti-RTiRKpzqYGcMVZtJIPUU2o9sG4eEah-IMS_uoa7Pcx6Ipsp1mSVA3DJiZ_Idu2B85JiyHaLSnjyt8dtrEET6obtsO9uR_mdI9xP1KBGTM_FHxBVJJhXwRjUgZlycYfsJ3Lt3ebLHx2aMkQiry_rptUKVzaFXO4VgiYujtv-76zlDJsiq_3AdhcZeA8prRLw2I8tt7a7gAExlT_aQc_MHtVbcSHDiUrpvQrPBmp_KYyFlc8bWmfVFU1opeN6iutS1q08lU5DzH7c_DJWnZztU2NoZpZro2qVmx54x3Y8hb2ztCLKNgcKbFy8YyOYFLZnjOBSCJ74i6GQ'

CASTING_ASSISTANT_HEADER = { 'Authorization': CASTING_ASSISTANT_TOKEN }

CASTING_DIRECTOR_TOKEN  = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhfMHN2cWpULVA5eFZ1a0NyU2k2cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uYnA5Z3h2cS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA3ZmUyZGUxMzBjNjUwMDcwZDk3ZmMyIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTYxOTE3MDAzOSwiZXhwIjoxNjE5MTc3MjM5LCJhenAiOiJPZzR1NFlWNVRiejBjaU9WZ0hYVmhEUDVWbkZVbE5jQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.AmwjV5X7lkj50hePsddasdfUhmnpkrsC0SnbiH0EJL9wdbqBsZkCMEwveqjgBYSbLPb9QFuN87x6rdAoe_o5bI3cXCfScl4IIPCBsd1_GzdF19_34B6YIO6Bk9GSlOgU6lWOf6fd9VktqX9mCjnEPHVbciVI_S_P3UNdR48RSkV0FETqprFAziaGg1pEKmS-TspuXLUeSlybmtaCarulhHGLcIG_d56xseVkujJCzHvNSKwnxW9YgUL4yHgcL40_YFfFfLsUksfEiaG-LMURQcHH15uYo7eTNj6nHbx5OONMzT65OXX52LNbazYrxqRcZZqd0pBGKILvDPxDShF_ng'
CASTING_DIRECTOR_HEADER = { 'Authorization': CASTING_DIRECTOR_TOKEN }


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_database.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_name))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_executive_producer_can_get_movies(self):
        res = self.client().get('/movies',  headers=EXECUTIVE_PRODUCER_HEADER)
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])


    def test_get_movie_with_id_1_with_access_token(self):
        res = self.client().get('/movies/1',  headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_get_movie_with_id_1_without_access_token(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_claims')
        self.assertEqual(data['description'], 'Authorization not included in headers')


    def test_post_new_movie(self):
        res = self.client().post('/movies', json={'title': '12 angery men'}, 
        headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_patch_movie(self):
        res = self.client().patch('/movies/3', json={'title': 'mad max'}, 
        headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_movies'])
        

    def test_get_actors(self):
        res = self.client().get('/actors',  headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])


    def test_get_actor_with_id_1_with_access_token(self):
        res = self.client().get('/actors/2',  headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])


    def test_get_actor_with_id_1_without_access_token(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_claims')
        self.assertEqual(data['description'], 'Authorization not included in headers')


    def test_post_new_actor(self):
        res = self.client().post('/actors', json={'name': 'ali', 'age': 30, 'gender': True}, 
        headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])


    def test_patch_actor(self):
        res = self.client().patch('/actors/2', json={'name': 'nader','age':'28', 'gender': True}, 
        headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])


    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=EXECUTIVE_PRODUCER_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_actors'])


    def test_casting_director_can_not_post_new_movie(self):
        res = self.client().post('/movies', json={'title': '12 angery men'}, 
        headers=CASTING_DIRECTOR_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    
    def test_casting_director_can_get_movies(self):
        res = self.client().get('/movies',  headers=CASTING_DIRECTOR_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])


    def test_casting_assistant_can_not_post_new_movie(self):
        res = self.client().post('/movies', json={'title': '12 angery men'}, 
        headers=CASTING_ASSISTANT_HEADER)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    
    def test_casting_assistant_can_get_movies(self):
        res = self.client().get('/movies',  headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()