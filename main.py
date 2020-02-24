# -*- coding: utf-8 -*-

import sys
import schedule_design

from selenium import webdriver
from time import sleep

from PyQt5 import QtWidgets

class Schedule:
	"""Класс расписания учебного процесса."""
	def __init__(self):
		# Инициализация веб-драйвера Chrome.
		self.driver = webdriver.Chrome()
		self.driver.get('https://lk.ugatu.su/raspisanie/#timetable')
		self.driver.fullscreen_window()

	def getGroupList(self, faculty, course):
		# Ввод факультета и курса.
		self.driver.find_element_by_xpath(f"//*[@id='id_faculty']/option[@value='{faculty}']").click()
		self.driver.find_element_by_xpath(f"//*[@id='id_klass']/option[@value='{course}']").click()
		sleep(1)
		group_list = self.driver.find_element_by_xpath(f"//*[@id='id_group']").text.split("\n")[1:]
		return group_list

	def getSemestrList(self):
		semestr_list = [elem[2:] for elem in self.driver.find_element_by_xpath(f"//*[@id='SemestrSchedule']").text.split("\n")[1:]]
		return semestr_list

	def dataInput(self, group, schedule_type, week, semestr):
		# Ввод группы, типа расписания, недели и семестра.
		self.driver.find_element_by_xpath(f"//*[@id='id_group']/option[.='{group}']").click()
		self.driver.find_element_by_xpath(f"//*[@id='id_ScheduleType']/li[{schedule_type}]/label").click()
		self.driver.find_element_by_xpath(f"//*[@id='WeekSchedule']/option[{week}]").click()
		self.driver.find_element_by_xpath(f"//*[@id='SemestrSchedule']/option[{semestr}]").click()
		self.driver.find_element_by_xpath("//input[@name='view'][@value='ПОКАЗАТЬ']").click() # Кнопка показа расписания.

		print("Данные введены!")


	def parseShedule(self):
		parse_data = {}
		buff = []

		for column in range(2, 8):
			buff.clear()
			day = self.driver.find_element_by_xpath(f"//*[@id='schedule']/thead/tr/th[{column}]").text.split("\n") # День недели и дата.
			for row in range(1, 8):
				uniwork = self.driver.find_element_by_xpath(f"//*[@id='schedule']/tbody/tr[{row}]/td[{column}]").text
				if uniwork != "":
					buff.append(f"\n{row} пара\n" + uniwork)
			parse_data[day[0]] = [{day[1]:buff[:]}]

		print("Данные расписания получены!")

		return parse_data

class ScheduleForm(QtWidgets.QMainWindow, schedule_design.Ui_MainWindow):
	""" Доступ к переменным, методам и т.д. в файле schedule_design.py. """
	def __init__(self):
		super().__init__()
		self.setupUi(self) # Инициализация дизайна.

		schedule = Schedule()
		for item in schedule.getSemestrList():
			self.comboBox_semestr.addItem(item)

		self.pushButton.clicked.connect(self.showSchedule) # Выполнение функции showSchedule, при нажатии кнопки.

	def showSchedule(self):
		self.textBrowser.clear()
		
		

def _main():

	# data = {
	# 	'faculty': None,
	# 	'course': None,
	# 	'group': None,
	# 	'schedule_type': None,
	# 	'week': None,
	# 	'semestr': None
	# }

	app = QtWidgets.QApplication(sys.argv) # Новый экземпляр QApplication.
	window = ScheduleForm() # Создание объекта класса.
	window.show() # Показ окна.
	app.exec_() # Запуск приложения.

	# schedule = Schedule()
	# schedule.getGroupList(data['faculty'], data['course'])
	# schedule.getSemestrList()
	# schedule.dataInput(data['group'], data['schedule_type'], data['week'], data['semestr'])
	# parses = schedule.parseShedule()
	# print(parses)

if __name__ == "__main__":
	_main()