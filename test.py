#!flask/bin/python
import os
import unittest
from app import app, db
from app.article.models import Article
from app.authentication.models import User
from app.sections.models import Sections

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class signuptestcase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testsignupget(self):
        test = app.test_client(self)
        response = test.get('/auth/signup/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def testsignuppost(self):
        new_user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(new_user)
        db.session.commit()
        test = app.test_client(self)
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test'
        }
        response = test.post(
            '/auth/signup/',
            data=data
            )
        self.assertTrue(response.status_code == 200)
        usertest = User.query.filter(User.email == 'test@example.com').first()
        self.assertTrue(usertest.username == u'Testuser')

    def testfunctionhashpassword(self):
        new_user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(new_user)
        db.session.commit()
        self.assertTrue(new_user.check_password('test'))


class signintestcase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signin_get(self):
        tester = app.test_client(self)
        response = tester.get('/auth/signin/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_signin_post(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        data = {'email': 'test@example.com',
                'password': 'test'
                }
        tester = app.test_client(self)
        response = tester.post(
            '/auth/signin/',
            data=data
        )
        self.assertTrue(response.status_code == 302)
        usertest = User.query.filter(User.username == 'Testuser').first()
        self.assertTrue(usertest.username == u'Testuser')


class tokentestcase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_generate_token(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        with app.test_request_context():
            token = user.generate_token()
            self.assertTrue(user.verify_token(token) == user)

    def test_verify_token(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        with app.test_request_context():
            token = user.generate_token(expiration=10)
            self.assertIs(user.verify_token(token), user)
            self.assertIsNot(user, usertest.verify_token(token))


class RecoverAccountTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # if you need a test_user use this in your function
    def initialize_test_user(self):
        usertest = User.query.filter(User.username == 'Testuser').first()
        if usertest is None:
            user = User(
                username='testuser',
                email='is2testcms@gmail.com',
                password='test',
                role=1,
                status=1
            )
            db.session.add(user)
            db.session.commit()

    # in this pull request this team haven't a index page
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    # Testing initialization of form recover password
    def test_init_recover_pass(self):
        tester = app.test_client(self)
        response = tester.get(
            '/auth/recover_pass',
            content_type='html/text',
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recuperar Cuenta', response.data)

    # Testing the correct function of recover password
    def test_recover_pass(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        data = {'email': 'is2testcms@gmail.com'}
        response = tester.post(
            '/auth/recover_pass/',
            data=data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Se ha enviado un correo a la direccion', response.data)

    def test_change_password_recover(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        usertest = User.query.filter(User.username == 'Testuser').first()
        token = usertest.generate_token()
        old_password = usertest.password

        # test initialization of form Change Password
        url = '/auth/change_pass/?token='+str(token)
        response = tester.get(
            url,
            content_type='html/text,',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change Password', response.data)

        # Test functionality of Change Password
        data = {
            'password': 'new_test',
            'confirm': 'new_test'
        }
        response_post = tester.post(
             url,
             data=data
        )
        self.assertIn(b'password updated successfully', response_post.data)
        self.assertIsNot(usertest.password, old_password)


class LogoutTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def initialize_test_user(self):
        usertest = User.query.filter(User.username == 'Testuser').first()
        if usertest is None:
            user = User(
                username='testuser',
                email='test@example.com',
                password='test',
                role=1,
                status=1
            )
            db.session.add(user)
            db.session.commit()

    def test_logout_remove_info(self):
        tester = app.test_client(self)
        response = tester.get('/auth/signout', content_type='html/text')
        self.assertEqual(response.status_code, 301)

    def test_logout_redirect(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        response = tester.post(
            '/auth/signout/',
            content_type='html/text',
            follow_redirects=True)
        # TODO: COMPLETE TEST!!!!!!


class createarticlecase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testarticlecreatepost(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        new_article = Article(
            title='testtitle',
            body='testbody',
            user_name=usertest.username,
            user=usertest,
            )
        db.session.add(new_article)
        db.session.commit()
        self.assertTrue(
            new_article.find_by_id(new_article.id) is not None)
        self.assertTrue(
            new_article.find_by_author(new_article.user_name) is not None)


class articlemodelcase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testarticlecreatepost(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        testsection = Sections(
            section_='sectionname',
            description_='section created to test an article')
        db.session.add(testsection)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        testarticle = Article(
            title='testtitle',
            body='testbody',
            section_name=testsection.section_name,
            section=testsection,
            user_name=usertest.username,
            user=usertest,
        )
        db.session.add(testarticle)
        db.session.commit()

        self.assertTrue(testarticle.find_by_id(testarticle.id) is not None)
        self.assertTrue(
            testarticle.find_by_author(testarticle.user_name) is not None)
        self.assertTrue(
            testarticle.find_by_section('testsection')is not None)


class CreateAndViewSectionsTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    # testing view sections
    def test_view_sections(self):

        tester = app.test_client(self)
        response = tester.get('/sec/views_sections/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # testing create sections
    def test_get_create_sections(self):

        tester = app.test_client(self)
        response = tester.get(
            '/sec/create_sections/',
            content_type='html/text'
        )
        self.assertIn(b'Digite el nombre de la nueva seccion', response.data)
        self.assertEqual(response.status_code, 200)

    # now testing the post method to create sections
    def test_post_create_sections(self):
        tester = app.test_client(self)

        data = {
            'section': 'example of test section',
            'description': 'example of description'
        }
        response = tester.post(
             '/sec/create_sections/',
             data=data,
             follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Example Of Test Section', response.data)
        self.assertIn(b'example of description', response.data)


class ModifySectionTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_modify_section_get(self):
        test = app.test_client(self)
        response = test.get('/sec/modify_sections', content_type='html/text')
        self.assertEqual(response.status_code, 301)

    def test_modify_section_post(self):
        test = app.test_client(self)
        section = Sections('testsection', 'testdescription')
        db.session.add(section)
        db.session.commit()
        print section.id
        url = '/sec/modify_sections/?id='+str(section.id)
        data = {
            'section': 'testsection2',
            'description': 'testdescription2'
        }
        response = test.post(
            url,
            data,
            follow_redirects=True
            )
        print response.data


class sectiontestcasedelete(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testsectiondeletepost(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        section_todelete = Sections(
            section_='testname',
            description_='testsection',
            )
        db.session.add(section_todelete)
        db.session.commit()
        test = app.test_client(self)
        response = test.get('sec/delete_sections?id=1')
        self.assertTrue(response.status_code == 301)
        testsection = Sections.query.filter(
            Sections.section_name == 'testname').first()
        self.assertTrue(testsection is None)

if __name__ == '__main__':
    unittest.main()
