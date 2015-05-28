
import datetime
import httplib
import json
import unittest

import django.core.urlresolvers
import django.test

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import wybory.daszek_common
from wybory.models import Gmina, Obwod

class ClientTests(django.test.TestCase):
	def setUp(self):
		self.client = django.test.Client()
		self.nazwa_gminy = "gmina1"
		self.nazwa_obwodu = "obwod11"
		wybory.daszek_common.add_item(self.nazwa_gminy, self.nazwa_obwodu)
		self.obwod = Obwod.objects.get(nazwa = self.nazwa_obwodu)

		self.cokolwiek_404 = "BZDURA"
		self.gminy_url = django.core.urlresolvers.reverse('wybory:gminy')
		self.obwody_url = django.core.urlresolvers.reverse('wybory:obwody', kwargs = {'nazwa_gminy': self.nazwa_gminy})
		self.obwody_url_404 = django.core.urlresolvers.reverse('wybory:obwody', kwargs = {'nazwa_gminy': self.cokolwiek_404})
		self.zapytanie_ajax_url = django.core.urlresolvers.reverse('wybory:zapytanie_ajax', kwargs = {'nazwa_gminy': self.nazwa_gminy})
		self.zapytanie_ajax_url_404 = django.core.urlresolvers.reverse('wybory:zapytanie_ajax', kwargs = {'nazwa_gminy': self.cokolwiek_404})

	def test_data_modyfikacji(self):
		string = wybory.daszek_common.datetime_to_string(self.obwod.data_modyfikacji)
		self.assertTrue(len(string) > 10)

	def test_lista_gmin(self):
		response = self.client.get(self.gminy_url)
		self.assertEqual(response.status_code, httplib.OK)
		self.assertContains(response, self.nazwa_gminy)

	def test_obwody_404(self):
		response = self.client.get(self.obwody_url_404)
		self.assertEqual(response.status_code, httplib.NOT_FOUND)

	def test_obwody(self):
		response = self.client.get(self.obwody_url)
		self.assertEqual(response.status_code, httplib.OK)
		self.assertContains(response, self.nazwa_gminy)
		self.assertContains(response, self.nazwa_obwodu)

	def test_ajax_404(self):
		response = self.client.get(self.zapytanie_ajax_url_404)
		self.assertEqual(response.status_code, httplib.NOT_FOUND)

	def test_ajax(self):
		response = self.client.post(self.zapytanie_ajax_url, {'id': self.obwod.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, httplib.OK)
		self.assertJSONEqual(response.content, json.dumps({"kart_do_glosowania": 0, "wyborcow": 0, "data_modyfikacji":wybory.daszek_common.datetime_to_string(self.obwod.data_modyfikacji)}))

	@unittest.skip("demonstrating skipping")
	def test_concurrent_users(self):
		self.driver = webdriver.Firefox()

		self.driver.get("http://www.python.org")
		self.assertIn("Python", self.driver.title)
		elem = self.driver.find_element_by_name("q")
		elem.send_keys("pycon")
		elem.send_keys(Keys.RETURN)
		assert "No results found." not in self.driver.page_source

		self.driver.close()

	def tearDown(self):
		wybory.daszek_common.wipe_database()

#TODO

#class MySeleniumTests(django.test.LiveServerTestCase):
	#def setUp(self):
		#self.driver = webdriver.Firefox()
		#self.driver_2 = webdriver.Firefox()

	#def test_search_in_python_org(self):
		#driver = self.driver
		#driver.get("http://www.python.org")
		#self.assertIn("Python", driver.title)
		#elem = driver.find_element_by_name("q")
		#elem.send_keys("pycon")
		#elem.send_keys(Keys.RETURN)
		#assert "No results found." not in driver.page_source

		#driver_2 = self.driver
		#driver_2.get("http://www.python.org")
		#self.assertIn("Python", driver.title)
		#elem = driver_2.find_element_by_name("q")
		#elem.send_keys("pycon")
		#elem.send_keys(Keys.RETURN)
		#assert "No results found." in driver_2.page_source

	#def tearDown(self):
		#self.driver.close()
		#self.driver_2.close()

#class PythonOrgSearch(unittest.TestCase):

	#def setUp(self):
		#self.driver = webdriver.Firefox()
		#self.driver_2 = webdriver.Firefox()

	#def test_search_in_python_org(self):
		#driver = self.driver
		#driver.get("http://www.python.org")
		#self.assertIn("Python", driver.title)
		#elem = driver.find_element_by_name("q")
		#elem.send_keys("pycon")
		#elem.send_keys(Keys.RETURN)
		#assert "No results found." not in driver.page_source

		#driver_2 = self.driver
		#driver_2.get("http://www.python.org")
		#self.assertIn("Python", driver.title)
		#elem = driver_2.find_element_by_name("q")
		#elem.send_keys("pycon")
		#elem.send_keys(Keys.RETURN)
		#assert "No results found." in driver_2.page_source

	#def tearDown(self):
		#self.driver.close()
		#self.driver_2.close()

if __name__ == "__main__":
	unittest.main()

