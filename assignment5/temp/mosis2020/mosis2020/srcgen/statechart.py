# Implementation of statechart statechart.


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import queue


class Statechart:
	"""Implementation of the state machine Statechart.
	"""

	class State:
		""" State Enum
		"""
		(
			main_region_example,
			main_region_example_r1_spending,
			main_region_example_r3_at_home,
			null_state
		) = range(4)
	


	
	class Util:
	
		"""Implementation of scope Util.
		"""
		
		def __init__(self, statemachine):
			self.operation_callback = None
			
			self.statemachine = statemachine
		
	
	class Employee:
	
		"""Implementation of scope Employee.
		"""
		
		def __init__(self, statemachine):
			self.go_to_work = None
			self.go_home = None
			self.shift_clicked = None
			self.shift_clicked_value = None
			self.operation_callback = None
			
			self.statemachine = statemachine
		
		def raise_go_to_work(self):
			self.statemachine._Statechart__in_event_queue.put(self.raise_go_to_work_call)
			self.statemachine.run_cycle()
		
		def raise_go_to_work_call(self):
			self.go_to_work = True
		
		def raise_go_home(self):
			self.statemachine._Statechart__in_event_queue.put(self.raise_go_home_call)
			self.statemachine.run_cycle()
		
		def raise_go_home_call(self):
			self.go_home = True
		
		def raise_shift_clicked(self, value):
			self.statemachine._Statechart__in_event_queue.put(lambda: self.raise_shift_clicked_call(value))
			self.statemachine.run_cycle()
		
		def raise_shift_clicked_call(self, value):
			self.shift_clicked = True
			self.shift_clicked_value = value
		
	
	class Factory:
	
		"""Implementation of scope Factory.
		"""
		
		def __init__(self, statemachine):
			self.operation_callback = None
			
			self.statemachine = statemachine
		
	
	class Ui:
	
		"""Implementation of scope Ui.
		"""
		
		def __init__(self, statemachine):
			self.action_pressed = None
			self.action_pressed_value = None
			self.action_released = None
			self.action_released_value = None
			self.operation_callback = None
			
			self.statemachine = statemachine
		
		def raise_action_pressed(self, value):
			self.statemachine._Statechart__in_event_queue.put(lambda: self.raise_action_pressed_call(value))
			self.statemachine.run_cycle()
		
		def raise_action_pressed_call(self, value):
			self.action_pressed = True
			self.action_pressed_value = value
		
		def raise_action_released(self, value):
			self.statemachine._Statechart__in_event_queue.put(lambda: self.raise_action_released_call(value))
			self.statemachine.run_cycle()
		
		def raise_action_released_call(self, value):
			self.action_released = True
			self.action_released_value = value
		
	
	def __init__(self):
		""" Declares all necessary variables including list of states, histories etc. 
		"""
		self.util = Statechart.Util(self)
		self.employee = Statechart.Employee(self)
		self.factory = Statechart.Factory(self)
		self.ui = Statechart.Ui(self)
		
		self.__in_event_queue = queue.Queue()
		
		# enumeration of all states:
		self.__State = Statechart.State
		self.__state_conf_vector_changed = None
		self.__next_state_index = None
		self.__state_vector = [None] * 2
		for __state_index in range(2):
			self.__state_vector[__state_index] = self.State.null_state
		
		# for timed statechart:
		self.timer_service = None
		self.__time_events = [None] * 1
		
		# initializations:
		self.__is_executing = False
	
	def is_active(self):
		""" @see IStatemachine#is_active()
		"""
		return self.__state_vector[0] is not self.__State.null_state or self.__state_vector[1] is not self.__State.null_state
	
	def is_final(self):
		"""Always returns 'false' since this state machine can never become final.
		@see IStatemachine#is_final()
		"""
		return False
			
	def is_state_active(self, state):
		""" Returns True if the given state is currently active otherwise false.
		"""
		s = state
		if s == self.__State.main_region_example:
			return (self.__state_vector[0] >= self.__State.main_region_example)\
				and (self.__state_vector[0] <= self.__State.main_region_example_r3_at_home)
		if s == self.__State.main_region_example_r1_spending:
			return self.__state_vector[0] == self.__State.main_region_example_r1_spending
		if s == self.__State.main_region_example_r3_at_home:
			return self.__state_vector[1] == self.__State.main_region_example_r3_at_home
		return False
		
	def time_elapsed(self, event_id):
		""" Add time events to in event queue
		"""
		if event_id in range(1):
			self.__in_event_queue.put(lambda: self.raise_time_event(event_id))
			self.run_cycle()
	
	def raise_time_event(self, event_id):
		self.__time_events[event_id] = True
	
	def __execute_queued_event(self, func):
		func()
	
	def __get_next_event(self):
		if not self.__in_event_queue.empty():
			return self.__in_event_queue.get()
		return None
	
	
	def __entry_action_main_region__example(self):
		self.ui.operation_callback.set_msg("You are at home.")
		
	def __entry_action_main_region__example_r1__spending(self):
		self.timer_service.set_timer(self, 0, 100, False)
		
	def __exit_action_main_region__example_r1__spending(self):
		self.timer_service.unset_timer(self, 0)
		
	def __enter_sequence_main_region__example_default(self):
		self.__entry_action_main_region__example()
		self.__enter_sequence_main_region__example_r1_default()
		self.__enter_sequence_main_region__example_r3_default()
		
	def __enter_sequence_main_region__example_r1__spending_default(self):
		self.__entry_action_main_region__example_r1__spending()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_example_r1_spending
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__example_r3__at_home_default(self):
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.main_region_example_r3_at_home
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_default(self):
		self.__react_main_region__entry__default()
		
	def __enter_sequence_main_region__example_r1_default(self):
		self.__react_main_region__example_r1__entry__default()
		
	def __enter_sequence_main_region__example_r3_default(self):
		self.__react_main_region__example_r3__entry__default()
		
	def __exit_sequence_main_region__example_r1__spending(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		self.__exit_action_main_region__example_r1__spending()
		
	def __exit_sequence_main_region__example_r3__at_home(self):
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.null_state
		
	def __exit_sequence_main_region(self):
		state = self.__state_vector[0]
		if state == self.State.main_region_example_r1_spending:
			self.__exit_sequence_main_region__example_r1__spending()
		state = self.__state_vector[1]
		if state == self.State.main_region_example_r3_at_home:
			self.__exit_sequence_main_region__example_r3__at_home()
		
	def __react_main_region__example_r1__entry__default(self):
		self.__enter_sequence_main_region__example_r1__spending_default()
		
	def __react_main_region__example_r3__entry__default(self):
		self.__enter_sequence_main_region__example_r3__at_home_default()
		
	def __react_main_region__entry__default(self):
		self.__enter_sequence_main_region__example_default()
		
	def __react(self):
		return False
	
	
	def __main_region__example_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__react() == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__example_r1__spending_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__example_react(try_transition) == False:
				if self.__time_events[0]:
					self.__exit_sequence_main_region__example_r1__spending()
					self.employee.operation_callback.increase_pay(1)
					self.__enter_sequence_main_region__example_r1__spending_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__example_r3__at_home_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.employee.go_to_work:
				self.__exit_sequence_main_region__example_r3__at_home()
				self.ui.operation_callback.set_msg("I refuse to go to work.")
				self.__enter_sequence_main_region__example_r3__at_home_default()
			elif self.employee.go_home:
				self.__exit_sequence_main_region__example_r3__at_home()
				self.ui.operation_callback.set_msg("Already at home.")
				self.__enter_sequence_main_region__example_r3__at_home_default()
			else:
				did_transition = False
		return did_transition
	
	
	def __clear_in_events(self):
		self.employee.go_to_work = False
		self.employee.go_home = False
		self.employee.shift_clicked = False
		self.ui.action_pressed = False
		self.ui.action_released = False
		self.__time_events[0] = False
	
	
	def enter(self):
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.util.operation_callback is None:
			raise ValueError("Operation callback for interface Util must be set.")
		
		if self.employee.operation_callback is None:
			raise ValueError("Operation callback for interface Employee must be set.")
		
		if self.factory.operation_callback is None:
			raise ValueError("Operation callback for interface Factory must be set.")
		
		if self.ui.operation_callback is None:
			raise ValueError("Operation callback for interface Ui must be set.")
		
		if self.__is_executing:
			return
		self.__is_executing = True
		self.__enter_sequence_main_region_default()
		self.__is_executing = False
	
	
	def exit(self):
		if self.__is_executing:
			return
		self.__is_executing = True
		self.__exit_sequence_main_region()
		self.__is_executing = False
	
	
	def run_cycle(self):
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.util.operation_callback is None:
			raise ValueError("Operation callback for interface Util must be set.")
		
		if self.employee.operation_callback is None:
			raise ValueError("Operation callback for interface Employee must be set.")
		
		if self.factory.operation_callback is None:
			raise ValueError("Operation callback for interface Factory must be set.")
		
		if self.ui.operation_callback is None:
			raise ValueError("Operation callback for interface Ui must be set.")
		
		if self.__is_executing:
			return
		self.__is_executing = True
		next_event = self.__get_next_event()
		if next_event is not None:
			self.__execute_queued_event(next_event)
		condition_0 = True
		while condition_0:
			self.__next_state_index = 0
			while self.__next_state_index < len(self.__state_vector):
				if self.__state_vector[self.__next_state_index] == self.State.main_region_example_r1_spending:
					self.__main_region__example_r1__spending_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_example_r3_at_home:
					self.__main_region__example_r3__at_home_react(True)
				self.__next_state_index += 1
			self.__clear_in_events()
			next_event = self.__get_next_event()
			if next_event is not None:
				self.__execute_queued_event(next_event)
			condition_0 = self.employee.go_to_work or self.employee.go_home or self.employee.shift_clicked or self.ui.action_pressed or self.ui.action_released or self.__time_events[0]
		self.__is_executing = False
	
	
	
	
