import time
import urllib
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
 
class bca(object):
	__url = 'https://ibank.klikbca.com/'
	def __init__(self):
		self.formLogin()

	def formLogin(self):
		''' webdriver : Chrome() Firefox() PhantomJS() '''
		username = raw_input('Masukkan username: ')
		password = getpass.getpass('Masukkan password: ')
		self.__driver = webdriver.PhantomJS()
		self.__driver.wait = WebDriverWait(self.__driver, 3)
		self.__username = username
		self.__password = password
		self.authLogin()

	def authLogin(self):
		try:
			self.__driver.get(self.__url)
			username = self.__driver.wait.until(EC.presence_of_element_located((By.ID, "user_id")))
			password = self.__driver.wait.until(EC.element_to_be_clickable((By.ID, "pswd")))
			loginBTN = self.__driver.wait.until(EC.presence_of_element_located((By.NAME, "value(Submit)")))
			username.send_keys(self.__username)
			password.send_keys(self.__password)
			loginBTN.send_keys(webdriver.common.keys.Keys.SPACE)

			try:
				self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"header\"]"))
				self.__driver.switch_to_default_content();
				self.showMenu()
			except:
				alert = self.__driver.switch_to_alert()
				print(alert.text)
				alert.accept()
		except:
			print("please check your connection...")

	def showMenu(self):
		print ("""
	       1. Cek Saldo
	       2. Cek Mutasi Hari ini
	       3. Exit/Quit

	       *************************************************************************
	       (Script ini masih beta, hanya bisa pilih 1 menu kemudian otomatis logout)
	       """)

		menu = raw_input("Pilih Menu : ")
		if (menu =='1') :
			self.cekSaldo()
			self.logout()
		elif (menu == '2'):
			self.cekMutasi()
			self.logout()
		elif (menu == '3'):
			self.logout()

		self.__driver.quit()
		exit()

	def logout(self):
		try :
			self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"header\"]"))
			logout = self.__driver.wait.until(EC.presence_of_element_located((By.XPATH,"//a[@onclick=\"javascript:goToPage('authentication.do?value(actions)=logout');return false;\"]")))
			logout.click();
			print("Anda berhasil logout")
		except TimeoutException:
		    print("Session timeout. please login again")

	def cekMutasi(self):
		self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"menu\"]"))
		menuMutasi = self.__driver.wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href=\"account_information_menu.htm\"]")))
		menuMutasi.click()
		cek_mutasi = self.__driver.wait.until(EC.presence_of_element_located((By.XPATH,"//a[@onclick=\"javascript:goToPage('accountstmt.do?value(actions)=acct_stmt');return false;\"]")))
		cek_mutasi.click()
		self.__driver.switch_to_default_content();
		self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"atm\"]"));

		#using manual date
		# select = Select(self.__driver.find_element_by_id("startDt"))
		# select.select_by_visible_text("01")

		mutasiBTN = self.__driver.wait.until(EC.presence_of_element_located((By.NAME, "value(submit1)")))
		mutasiBTN.click()
		try:
			mutasi = self.__driver.find_element_by_xpath("//table[3]//tbody//tr[2]//td//table")
			self.__mutasiData = self.mutasiParse(mutasi)
			self.showMutasi()
		except:
			print("Tidak ada mutasi hari ini")
		
		self.__driver.switch_to_default_content()

	def mutasiParse(self,table):
		table_mutasi = BeautifulSoup(table.get_attribute('innerHTML'),"html.parser")
		# print(table_mutasi.prettify())
		data = []
		table_body = table_mutasi.find('tbody')
		rows = table_body.find_all('tr')
		for row in rows :
			cols = row.find_all('td')
			cols = [ele.text.strip() for ele in cols]
			data.append([ele for ele in cols if ele])
		return data[1:]

	def showMutasi(self) :
		if len(self.__mutasiData) > 0 :
			print("Tgl \tMutasi \tDebit/Kredit \tKet")
			for transaction in self.__mutasiData:
				print("%s \t%s \t%s \t%s"%(transaction[0], transaction[3], transaction[4], transaction[1]))
		else:
			print("Tidak ada Mutasi Hari ini")

	def cekSaldo(self):
		try:
			self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"menu\"]"))
			mutasi = self.__driver.wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href=\"account_information_menu.htm\"]")))
			mutasi.click()
			cek_saldo = self.__driver.wait.until(EC.presence_of_element_located((By.XPATH,"//a[@onclick=\"javascript:goToPage('balanceinquiry.do');return false;\"]")))
			cek_saldo.click()
			self.__driver.switch_to_default_content();
			self.__driver.switch_to.frame(self.__driver.find_element_by_xpath("//frame[@name=\"atm\"]"));
			saldo = self.__driver.find_element_by_xpath("//table[3]/tbody//tr[2]//td[4]").text
			print("Saldo BCA saat ini adalah %s"%saldo)
			self.__driver.switch_to_default_content()
		except TimeoutException:
		    print("Session timeout. please login again")
 
 
if __name__ == "__main__":
	bca()