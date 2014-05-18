# -*- coding: utf-8 -*-
import os
import meals
import unittest
import tempfile


class MealsTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, meals.app.config['DATABASE'] = tempfile.mkstemp()
        meals.app.config['TESTING'] = True
        self.app = meals.app.test_client()
        meals.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(meals.app.config['DATABASE'])

    # testing functions

    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/')
        assert b'No active meals here so far' in rv.data, "Not an empty DB initially - ERROR"

    def test_post_active_meal(self):
        """Test that posting active meals and listing work"""
        rv = self.app.post('/save_meals', data=dict(
            title='American Chopseuy',
            description='I like it',
            active=1
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data, "DB entries fetch failed - ERROR"
        assert b'New entry was successfully posted' in rv.data, "New active entry post failed - ERROR"
        assert b'AMerican Chopseuy' in rv.data, "Active entry not listed - ERROR"

    def test_post_inactive_meal(self):
        """Test that posting inactive meals and not being listed work"""
        rv = self.app.post('/save_meals', data=dict(
            title='Chinese Chopseuy',
            description='I don\'t like it',
            active=0
        ), follow_redirects=True)
        assert b'New entry was successfully posted' in rv.data, "New inactive entry post failed - ERROR"
        assert b'Chinese Chopseuy' not in rv.data, "Inactive entry listed - ERROR"

    def test_add_meal_page(self):
        """Test for checking the add meal page"""
        rv = self.app.get('/add_meals_page')
        assert b'Add you meal' in rv.data, 'form not rendered in rv data - ERROR'
        assert b'<input type=submit value=Save>' in rv.data, "form not rendered in rv data - ERROR"

    def test_get_detail_page(self):
        """ Test for checking the detail page of a meal"""
        self.app.post('/save_meals', data=dict(
            title='Noodles',
            description='I may like it',
            active=1
        ), follow_redirects=True)
        with meals.app.app_context():
            db = meals.get_db()
            cur = db.execute(
                'select id, title, description from meal_entries where active=1 order by id desc')
            my_meal = cur.fetchone()  # since we added only one
        my_meal_id = my_meal[0]  # get the element at 0th index, it is an sqlite3.Row type object
        rv = self.app.get('/meal_detail_page/' + str(my_meal_id))
        assert b'<h1>Noodles</h1>' in rv.data, "detail page doesn't contain saved data- ERROR"
        assert b"<h2 class='add-entry'>I may like it</h2>" in rv.data, "detail page doesn't contain saved data- ERROR"

if __name__ == '__main__':
    unittest.main()
