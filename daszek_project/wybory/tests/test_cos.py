
import datetime
import httplib
import json
import unittest

import django.core.urlresolvers
import django.test

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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


def ajax_complete(driver):
	try:
		return 0 == driver.execute_script("return jQuery.active")
	except WebDriverException:
		pass

def compare_source(driver):
	try:
		return source != driver.page_source
	except WebDriverException:
		pass

class MySeleniumTests(django.test.LiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.nazwa_gminy = "gmina1"
		self.nazwa_obwodu = "obwod11"
		wybory.daszek_common.add_item(self.nazwa_gminy, self.nazwa_obwodu)
		self.obwody_url = django.core.urlresolvers.reverse('wybory:obwody', kwargs = {'nazwa_gminy': self.nazwa_gminy})

	def test_search_in_python_org(self):
		driver = self.driver
		driver.get(self.live_server_url + self.obwody_url)
		#self.assertIn("Python", driver.title)
		edit = driver.find_element_by_name('editbutton')

		hover = ActionChains(driver).move_to_element(edit)
		hover.perform()
		edit.click()

		#TODO wait
		wait = WebDriverWait(driver, 10)
		element = wait.until(EC.visibility_of((By.Name,'editbutton')))

		WebDriverWait(driver, 10).until(compare_source)
		#WebDriverWait(driver, 10).until(ajax_complete,  "Timeout waiting for page to load")

		field = driver.find_element_by_name("kart_do_glosowania")
		field.send_keys("500")

		submit = driver.find_element_by_name('placeholder2')
		submit.click()

		#TODO wait2
		WebDriverWait(driver, 10).until(compare_source)

		#TODO: check value is on DB
		self.obwod = Obwod.objects.get(nazwa = self.nazwa_obwodu)
		self.assertEquals(obwod.kart_do_glosowania, 500)

	def tearDown(self):
		self.driver.close()

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

