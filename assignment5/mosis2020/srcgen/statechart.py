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
			main_region_at__home,
			main_region_at__work,
			main_region_at__work_working_at__shift,
			main_region_at__work_working_at__shift_shift_unloading,
			main_region_at__work_working_at__shift_shift_unloading_main_at_stock,
			main_region_at__work_working_at__shift_shift_unloading_main_at_truck,
			main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying,
			main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying,
			main_region_at__work_working_at__shift_shift_assembly,
			main_region_at__work_working_at__shift_shift_assembly_r1_at_stock,
			main_region_at__work_working_at__shift_shift_loading,
			main_region_at__work_working_at__shift_shift_loading_r1_at_truck,
			main_region_at__work_working_at__shift_shift_loading_r1_at_stock,
			main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying,
			main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying,
			main_region_at__work_working_at__shift_energy_tiring,
			main_region_at__work_working_at__shift_energy_tired,
			main_region_at__work_working_at__shift_button_button_released,
			main_region_at__work_working_at__shift_button_button_pressed,
			main_region_at__work_working_grace__period,
			main_region_at__work_working_grace__period_r1_alternative__chosen,
			main_region_at__work_working_grace__period_r1_leave__day,
			main_region_at__work_working_toilet__break,
			null_state
		) = range(24)
	


	
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
		self.__assigned_shift = None
		self.__current_action = None
		
		# enumeration of all states:
		self.__State = Statechart.State
		self.__state_conf_vector_changed = None
		self.__next_state_index = None
		self.__state_vector = [None] * 3
		for __state_index in range(3):
			self.__state_vector[__state_index] = self.State.null_state
		
		# for timed statechart:
		self.timer_service = None
		self.__time_events = [None] * 4
		
		# history vector:
		self.__history_vector = [None] * 1
		for __history_index in range(1):
			self.__history_vector[__history_index] = self.State.null_state
		
		# initializations:
		self.__assigned_shift = 0
		self.__current_action = ""
		self.__is_executing = False
	
	def is_active(self):
		""" @see IStatemachine#is_active()
		"""
		return self.__state_vector[0] is not self.__State.null_state or self.__state_vector[1] is not self.__State.null_state or self.__state_vector[2] is not self.__State.null_state
	
	def is_final(self):
		"""Always returns 'false' since this state machine can never become final.
		@see IStatemachine#is_final()
		"""
		return False
			
	def is_state_active(self, state):
		""" Returns True if the given state is currently active otherwise false.
		"""
		s = state
		if s == self.__State.main_region_at__home:
			return self.__state_vector[0] == self.__State.main_region_at__home
		if s == self.__State.main_region_at__work:
			return (self.__state_vector[0] >= self.__State.main_region_at__work)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_toilet__break)
		if s == self.__State.main_region_at__work_working_at__shift:
			return (self.__state_vector[0] >= self.__State.main_region_at__work_working_at__shift)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_at__shift_button_button_pressed)
		if s == self.__State.main_region_at__work_working_at__shift_shift_unloading:
			return (self.__state_vector[0] >= self.__State.main_region_at__work_working_at__shift_shift_unloading)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying)
		if s == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock
		if s == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck
		if s == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying
		if s == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying
		if s == self.__State.main_region_at__work_working_at__shift_shift_assembly:
			return (self.__state_vector[0] >= self.__State.main_region_at__work_working_at__shift_shift_assembly)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock)
		if s == self.__State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock
		if s == self.__State.main_region_at__work_working_at__shift_shift_loading:
			return (self.__state_vector[0] >= self.__State.main_region_at__work_working_at__shift_shift_loading)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying)
		if s == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck
		if s == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock
		if s == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying
		if s == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying
		if s == self.__State.main_region_at__work_working_at__shift_energy_tiring:
			return self.__state_vector[1] == self.__State.main_region_at__work_working_at__shift_energy_tiring
		if s == self.__State.main_region_at__work_working_at__shift_energy_tired:
			return self.__state_vector[1] == self.__State.main_region_at__work_working_at__shift_energy_tired
		if s == self.__State.main_region_at__work_working_at__shift_button_button_released:
			return self.__state_vector[2] == self.__State.main_region_at__work_working_at__shift_button_button_released
		if s == self.__State.main_region_at__work_working_at__shift_button_button_pressed:
			return self.__state_vector[2] == self.__State.main_region_at__work_working_at__shift_button_button_pressed
		if s == self.__State.main_region_at__work_working_grace__period:
			return (self.__state_vector[0] >= self.__State.main_region_at__work_working_grace__period)\
				and (self.__state_vector[0] <= self.__State.main_region_at__work_working_grace__period_r1_leave__day)
		if s == self.__State.main_region_at__work_working_grace__period_r1_alternative__chosen:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_grace__period_r1_alternative__chosen
		if s == self.__State.main_region_at__work_working_grace__period_r1_leave__day:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_grace__period_r1_leave__day
		if s == self.__State.main_region_at__work_working_toilet__break:
			return self.__state_vector[0] == self.__State.main_region_at__work_working_toilet__break
		return False
		
	def time_elapsed(self, event_id):
		""" Add time events to in event queue
		"""
		if event_id in range(4):
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
	
	
	def __check_main_region__at__work_working__at__shift_shift__choice_0_tr0_tr0(self):
		return self.__assigned_shift == 2
		
	def __check_main_region__at__work_working__at__shift_shift__choice_0_tr1_tr1(self):
		return self.__assigned_shift == 1
		
	def __check_main_region__at__work_working__grace__period_r1__choice_0_tr0_tr0(self):
		return self.employee.shift_clicked
		
	def __effect_main_region__at__work_working__at__shift_shift__choice_0_tr0(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_default()
		
	def __effect_main_region__at__work_working__at__shift_shift__choice_0_tr1(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__assembly_default()
		
	def __effect_main_region__at__work_working__at__shift_shift__choice_0_tr2(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default()
		
	def __effect_main_region__at__work_working__grace__period_r1__choice_0_tr0(self):
		self.__enter_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen_default()
		
	def __effect_main_region__at__work_working__grace__period_r1__choice_0_tr1(self):
		self.__enter_sequence_main_region__at__work_working__grace__period_r1__leave__day_default()
		
	def __entry_action_main_region__at__home(self):
		self.ui.operation_callback.shifts_hide()
		
	def __entry_action_main_region__at__work(self):
		self.__assigned_shift = self.util.operation_callback.get_random_integer(3)
		self.ui.operation_callback.shift_highlight_assigned(self.__assigned_shift)
		
	def __entry_action_main_region__at__work_working__at__shift(self):
		self.timer_service.set_timer(self, 0, (10 * 1000), False)
		self.ui.operation_callback.shifts_hide()
		self.ui.operation_callback.shift_highlight_clear()
		self.ui.operation_callback.shift_highlight_active(self.__assigned_shift)
		
	def __entry_action_main_region__at__work_working__at__shift_shift__unloading(self):
		self.ui.operation_callback.set_msg("Unloading Shift")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_stock(self):
		self.ui.operation_callback.set_actions("Walk, Toilet Break")
		self.ui.operation_callback.set_msg("In stock.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_truck(self):
		self.ui.operation_callback.set_actions("Walk, Pick Up")
		self.ui.operation_callback.set_msg("At truck.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying(self):
		self.ui.operation_callback.set_actions("Walk, Drop")
		self.ui.operation_callback.set_msg("In stock.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying(self):
		self.ui.operation_callback.set_actions("Walk")
		self.ui.operation_callback.set_msg("At truck.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__assembly(self):
		self.ui.operation_callback.set_msg("Assembly Shift")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock(self):
		self.ui.operation_callback.set_actions("Assemble")
		self.ui.operation_callback.set_msg("At Assembly.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__loading(self):
		self.ui.operation_callback.set_msg("Loading Shift")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_truck(self):
		self.ui.operation_callback.set_actions("Walk")
		self.ui.operation_callback.set_msg("At truck.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_stock(self):
		self.ui.operation_callback.set_actions("Walk, Pick Up, Toilet Break")
		self.ui.operation_callback.set_msg("In stock.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying(self):
		self.ui.operation_callback.set_actions("Walk, Drop")
		self.ui.operation_callback.set_msg("At truck.")
		
	def __entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying(self):
		self.ui.operation_callback.set_actions("Walk")
		self.ui.operation_callback.set_msg("In stock.")
		
	def __entry_action_main_region__at__work_working__at__shift_energy__tiring(self):
		self.timer_service.set_timer(self, 1, (2 * 1000), False)
		
	def __entry_action_main_region__at__work_working__at__shift_energy__tired(self):
		self.ui.operation_callback.set_msg("I\'m too tired!!!!")
		
	def __entry_action_main_region__at__work_working__at__shift_button_button_pressed(self):
		self.timer_service.set_timer(self, 2, 500, False)
		
	def __entry_action_main_region__at__work_working__grace__period(self):
		self.timer_service.set_timer(self, 3, (4 * 1000), False)
		self.ui.operation_callback.set_msg("Grace period...")
		self.ui.operation_callback.shifts_show()
		
	def __entry_action_main_region__at__work_working__grace__period_r1__alternative__chosen(self):
		self.__assigned_shift = self.employee.shift_clicked_value
		self.ui.operation_callback.set_msg("Chose another shift")
		
	def __entry_action_main_region__at__work_working__grace__period_r1__leave__day(self):
		self.ui.operation_callback.set_msg("Going Home")
		
	def __entry_action_main_region__at__work_working__toilet__break(self):
		self.ui.operation_callback.set_actions("Done")
		self.ui.operation_callback.set_msg("In toilet.")
		
	def __exit_action_main_region__at__work_working__at__shift(self):
		self.timer_service.unset_timer(self, 0)
		self.employee.operation_callback.increase_pay(10)
		
	def __exit_action_main_region__at__work_working__at__shift_energy__tiring(self):
		self.timer_service.unset_timer(self, 1)
		
	def __exit_action_main_region__at__work_working__at__shift_button_button_pressed(self):
		self.timer_service.unset_timer(self, 2)
		
	def __exit_action_main_region__at__work_working__grace__period(self):
		self.timer_service.unset_timer(self, 3)
		
	def __exit_action_main_region__at__work_working__grace__period_r1__alternative__chosen(self):
		self.ui.operation_callback.shift_highlight_assigned(self.__assigned_shift)
		
	def __enter_sequence_main_region__at__home_default(self):
		self.__entry_action_main_region__at__home()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__home
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_default(self):
		self.__entry_action_main_region__at__work()
		self.__enter_sequence_main_region__at__work_working_default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_default(self):
		self.__entry_action_main_region__at__work_working__at__shift()
		self.__enter_sequence_main_region__at__work_working__at__shift_shift_default()
		self.__enter_sequence_main_region__at__work_working__at__shift_energy_default()
		self.__enter_sequence_main_region__at__work_working__at__shift_button_default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__unloading()
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main_default()
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_stock()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__assembly_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__assembly()
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__assembly_r1_default()
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__loading()
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1_default()
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_truck()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_energy__tiring_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_energy__tiring()
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.main_region_at__work_working_at__shift_energy_tiring
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_energy__tired_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_energy__tired()
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.main_region_at__work_working_at__shift_energy_tired
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_button_button_released_default(self):
		self.__next_state_index = 2
		self.__state_vector[2] = self.State.main_region_at__work_working_at__shift_button_button_released
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__at__shift_button_button_pressed_default(self):
		self.__entry_action_main_region__at__work_working__at__shift_button_button_pressed()
		self.__next_state_index = 2
		self.__state_vector[2] = self.State.main_region_at__work_working_at__shift_button_button_pressed
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__grace__period_default(self):
		self.__entry_action_main_region__at__work_working__grace__period()
		self.__enter_sequence_main_region__at__work_working__grace__period_r1_default()
		
	def __enter_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen_default(self):
		self.__entry_action_main_region__at__work_working__grace__period_r1__alternative__chosen()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_grace__period_r1_alternative__chosen
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__grace__period_r1__leave__day_default(self):
		self.__entry_action_main_region__at__work_working__grace__period_r1__leave__day()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_grace__period_r1_leave__day
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region__at__work_working__toilet__break_default(self):
		self.__entry_action_main_region__at__work_working__toilet__break()
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.main_region_at__work_working_toilet__break
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_default(self):
		self.__react_main_region__entry__default()
		
	def __enter_sequence_main_region__at__work_working_default(self):
		self.__react_main_region__at__work_working__entry__default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift_default(self):
		self.__react_main_region__at__work_working__at__shift_shift__entry__default()
		
	def __shallow_enter_sequence_main_region__at__work_working__at__shift_shift(self):
		state = self.__history_vector[0]
		if state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__assembly_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_default()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
			self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main_default(self):
		self.__react_main_region__at__work_working__at__shift_shift__unloading_main__entry__default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__assembly_r1_default(self):
		self.__react_main_region__at__work_working__at__shift_shift__assembly_r1__entry__default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1_default(self):
		self.__react_main_region__at__work_working__at__shift_shift__loading_r1__entry__default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_energy_default(self):
		self.__react_main_region__at__work_working__at__shift_energy__entry__default()
		
	def __enter_sequence_main_region__at__work_working__at__shift_button_default(self):
		self.__react_main_region__at__work_working__at__shift_button__entry__default()
		
	def __enter_sequence_main_region__at__work_working__grace__period_r1_default(self):
		self.__react_main_region__at__work_working__grace__period_r1__entry__default()
		
	def __exit_sequence_main_region__at__home(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work(self):
		self.__exit_sequence_main_region__at__work_working()
		
	def __exit_sequence_main_region__at__work_working__at__shift(self):
		self.__exit_sequence_main_region__at__work_working__at__shift_shift()
		self.__exit_sequence_main_region__at__work_working__at__shift_energy()
		self.__exit_sequence_main_region__at__work_working__at__shift_button()
		self.__exit_action_main_region__at__work_working__at__shift()
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_energy__tiring(self):
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.null_state
		self.__exit_action_main_region__at__work_working__at__shift_energy__tiring()
		
	def __exit_sequence_main_region__at__work_working__at__shift_energy__tired(self):
		self.__next_state_index = 1
		self.__state_vector[1] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_button_button_released(self):
		self.__next_state_index = 2
		self.__state_vector[2] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__at__shift_button_button_pressed(self):
		self.__next_state_index = 2
		self.__state_vector[2] = self.State.null_state
		self.__exit_action_main_region__at__work_working__at__shift_button_button_pressed()
		
	def __exit_sequence_main_region__at__work_working__grace__period(self):
		self.__exit_sequence_main_region__at__work_working__grace__period_r1()
		self.__exit_action_main_region__at__work_working__grace__period()
		
	def __exit_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		self.__exit_action_main_region__at__work_working__grace__period_r1__alternative__chosen()
		
	def __exit_sequence_main_region__at__work_working__grace__period_r1__leave__day(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region__at__work_working__toilet__break(self):
		self.__next_state_index = 0
		self.__state_vector[0] = self.State.null_state
		
	def __exit_sequence_main_region(self):
		state = self.__state_vector[0]
		if state == self.State.main_region_at__home:
			self.__exit_sequence_main_region__at__home()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying()
		elif state == self.State.main_region_at__work_working_grace__period_r1_alternative__chosen:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen()
			self.__exit_action_main_region__at__work_working__grace__period()
		elif state == self.State.main_region_at__work_working_grace__period_r1_leave__day:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__leave__day()
			self.__exit_action_main_region__at__work_working__grace__period()
		elif state == self.State.main_region_at__work_working_toilet__break:
			self.__exit_sequence_main_region__at__work_working__toilet__break()
		state = self.__state_vector[1]
		if state == self.State.main_region_at__work_working_at__shift_energy_tiring:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tiring()
		elif state == self.State.main_region_at__work_working_at__shift_energy_tired:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tired()
		state = self.__state_vector[2]
		if state == self.State.main_region_at__work_working_at__shift_button_button_released:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_released()
			self.__exit_action_main_region__at__work_working__at__shift()
		elif state == self.State.main_region_at__work_working_at__shift_button_button_pressed:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_pressed()
			self.__exit_action_main_region__at__work_working__at__shift()
		
	def __exit_sequence_main_region__at__work_working(self):
		state = self.__state_vector[0]
		if state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying()
		elif state == self.State.main_region_at__work_working_grace__period_r1_alternative__chosen:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen()
			self.__exit_action_main_region__at__work_working__grace__period()
		elif state == self.State.main_region_at__work_working_grace__period_r1_leave__day:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__leave__day()
			self.__exit_action_main_region__at__work_working__grace__period()
		elif state == self.State.main_region_at__work_working_toilet__break:
			self.__exit_sequence_main_region__at__work_working__toilet__break()
		state = self.__state_vector[1]
		if state == self.State.main_region_at__work_working_at__shift_energy_tiring:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tiring()
		elif state == self.State.main_region_at__work_working_at__shift_energy_tired:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tired()
		state = self.__state_vector[2]
		if state == self.State.main_region_at__work_working_at__shift_button_button_released:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_released()
			self.__exit_action_main_region__at__work_working__at__shift()
		elif state == self.State.main_region_at__work_working_at__shift_button_button_pressed:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_pressed()
			self.__exit_action_main_region__at__work_working__at__shift()
		
	def __exit_sequence_main_region__at__work_working__at__shift_shift(self):
		state = self.__state_vector[0]
		if state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
		elif state == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
			self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying()
		
	def __exit_sequence_main_region__at__work_working__at__shift_energy(self):
		state = self.__state_vector[1]
		if state == self.State.main_region_at__work_working_at__shift_energy_tiring:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tiring()
		elif state == self.State.main_region_at__work_working_at__shift_energy_tired:
			self.__exit_sequence_main_region__at__work_working__at__shift_energy__tired()
		
	def __exit_sequence_main_region__at__work_working__at__shift_button(self):
		state = self.__state_vector[2]
		if state == self.State.main_region_at__work_working_at__shift_button_button_released:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_released()
		elif state == self.State.main_region_at__work_working_at__shift_button_button_pressed:
			self.__exit_sequence_main_region__at__work_working__at__shift_button_button_pressed()
		
	def __exit_sequence_main_region__at__work_working__grace__period_r1(self):
		state = self.__state_vector[0]
		if state == self.State.main_region_at__work_working_grace__period_r1_alternative__chosen:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__alternative__chosen()
		elif state == self.State.main_region_at__work_working_grace__period_r1_leave__day:
			self.__exit_sequence_main_region__at__work_working__grace__period_r1__leave__day()
		
	def __react_main_region__at__work_working__at__shift_shift__choice_0(self):
		if self.__check_main_region__at__work_working__at__shift_shift__choice_0_tr0_tr0():
			self.__effect_main_region__at__work_working__at__shift_shift__choice_0_tr0()
		elif self.__check_main_region__at__work_working__at__shift_shift__choice_0_tr1_tr1():
			self.__effect_main_region__at__work_working__at__shift_shift__choice_0_tr1()
		else:
			self.__effect_main_region__at__work_working__at__shift_shift__choice_0_tr2()
		
	def __react_main_region__at__work_working__grace__period_r1__choice_0(self):
		if self.__check_main_region__at__work_working__grace__period_r1__choice_0_tr0_tr0():
			self.__effect_main_region__at__work_working__grace__period_r1__choice_0_tr0()
		else:
			self.__effect_main_region__at__work_working__grace__period_r1__choice_0_tr1()
		
	def __react_main_region__entry__default(self):
		self.__enter_sequence_main_region__at__home_default()
		
	def __react_main_region__at__work_working__at__shift_shift__unloading_main__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_default()
		
	def __react_main_region__at__work_working__at__shift_shift__entry__default(self):
		self.__react_main_region__at__work_working__at__shift_shift__choice_0()
		
	def __react_main_region__at__work_working__at__shift_shift__assembly_r1__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock_default()
		
	def __react_main_region__at__work_working__at__shift_shift__loading_r1__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_default()
		
	def __react_main_region__at__work_working__at__shift_shift_hist(self):
		"""
		Enter the region with shallow history
		"""
		if self.__history_vector[0] is not self.State.null_state:
			self.__shallow_enter_sequence_main_region__at__work_working__at__shift_shift()
		else:
				self.__react_main_region__at__work_working__at__shift_shift__choice_0()
		
	def __react_main_region__at__work_working__at__shift_energy__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_energy__tiring_default()
		
	def __react_main_region__at__work_working__at__shift_button__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__at__shift_button_button_released_default()
		
	def __react_main_region__at__work_working__grace__period_r1__entry__default(self):
		self.__react_main_region__at__work_working__grace__period_r1__choice_0()
		
	def __react_main_region__at__work_working__entry__default(self):
		self.__enter_sequence_main_region__at__work_working__grace__period_default()
		
	def __react(self):
		return False
	
	
	def __main_region__at__home_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__react() == False:
				if self.employee.go_to_work:
					self.__exit_sequence_main_region__at__home()
					self.__enter_sequence_main_region__at__work_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__react() == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_react(try_transition) == False:
				if (self.__time_events[0]) and (self.employee.operation_callback.get_energy() > 25):
					self.__exit_sequence_main_region__at__work_working__at__shift()
					self.__enter_sequence_main_region__at__work_working__at__shift_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__unloading_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_react(try_transition) == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__unloading_main__at_stock_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__unloading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_default()
				elif (self.ui.action_pressed) and (("Toilet Break" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Toilet Break")):
					self.__exit_sequence_main_region__at__work_working__at__shift()
					self.__enter_sequence_main_region__at__work_working__toilet__break_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__unloading_main__at_truck_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__unloading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Pick Up" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Pick Up")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying_default()
				elif (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__unloading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying_default()
				elif (self.ui.action_pressed) and (("Drop" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Drop")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying()
					self.factory.operation_callback.increase_material(1)
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__unloading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__assembly_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_react(try_transition) == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__assembly_r1__at_stock_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__assembly_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Assemble" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Assemble") and self.factory.operation_callback.get_material() > 0):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock()
					self.factory.operation_callback.increase_finished(1)
					self.factory.operation_callback.increase_material(-1)
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__assembly_r1__at_stock_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__loading_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_react(try_transition) == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__loading_r1__at_truck_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__loading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__loading_r1__at_stock_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__loading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Pick Up" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Pick Up") and self.factory.operation_callback.get_finished() > 0):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
					self.factory.operation_callback.increase_finished(-1)
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying_default()
				elif (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_default()
				elif (self.ui.action_pressed) and (("Toilet Break" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Toilet Break")):
					self.__exit_sequence_main_region__at__work_working__at__shift()
					self.__enter_sequence_main_region__at__work_working__toilet__break_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__loading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying_default()
				elif (self.ui.action_pressed) and (("Drop" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Drop")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__at__shift_shift__loading_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Walk" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Walk")):
					self.__exit_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying()
					self.__enter_sequence_main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_energy__tiring_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__time_events[1]:
				self.__exit_sequence_main_region__at__work_working__at__shift_energy__tiring()
				self.employee.operation_callback.increase_energy(-2)
				self.__enter_sequence_main_region__at__work_working__at__shift_energy__tiring_default()
			elif self.employee.operation_callback.get_energy() <= 25:
				self.__exit_sequence_main_region__at__work_working__at__shift_energy__tiring()
				self.__enter_sequence_main_region__at__work_working__at__shift_energy__tired_default()
			else:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_energy__tired_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if ((self.employee.operation_callback.get_energy() + 50)) < 100:
				self.__exit_sequence_main_region__at__work()
				self.employee.operation_callback.increase_energy(50)
				self.__enter_sequence_main_region__at__home_default()
			else:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_button_button_released_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.ui.action_pressed:
				self.__exit_sequence_main_region__at__work_working__at__shift_button_button_released()
				self.__enter_sequence_main_region__at__work_working__at__shift_button_button_pressed_default()
			else:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__at__shift_button_button_pressed_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.ui.action_released:
				self.__exit_sequence_main_region__at__work_working__at__shift_button_button_pressed()
				self.__enter_sequence_main_region__at__work_working__at__shift_button_button_released_default()
			elif self.__time_events[2]:
				self.__exit_sequence_main_region__at__work_working__at__shift_button_button_pressed()
				self.ui.operation_callback.set_msg(self.ui.action_pressed_value)
				self.__enter_sequence_main_region__at__work_working__at__shift_button_button_pressed_default()
			else:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__grace__period_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_react(try_transition) == False:
				if self.__time_events[3]:
					self.__exit_sequence_main_region__at__work_working__grace__period()
					self.__enter_sequence_main_region__at__work_working__at__shift_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__grace__period_r1__alternative__chosen_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__grace__period_react(try_transition) == False:
				did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__grace__period_r1__leave__day_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_working__grace__period_react(try_transition) == False:
				if self.employee.go_home:
					self.__exit_sequence_main_region__at__work()
					self.__enter_sequence_main_region__at__home_default()
				else:
					did_transition = False
		return did_transition
	
	
	def __main_region__at__work_working__toilet__break_react(self, try_transition):
		did_transition = try_transition
		if try_transition:
			if self.__main_region__at__work_react(try_transition) == False:
				if (self.ui.action_pressed) and (("Done" is None) if (self.ui.action_pressed_value is None) else (self.ui.action_pressed_value == "Done")):
					self.__exit_sequence_main_region__at__work_working__toilet__break()
					self.__entry_action_main_region__at__work_working__at__shift()
					self.__react_main_region__at__work_working__at__shift_shift_hist()
					self.__enter_sequence_main_region__at__work_working__at__shift_energy_default()
					self.__enter_sequence_main_region__at__work_working__at__shift_button_default()
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
		self.__time_events[1] = False
		self.__time_events[2] = False
		self.__time_events[3] = False
	
	
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
				if self.__state_vector[self.__next_state_index] == self.State.main_region_at__home:
					self.__main_region__at__home_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock:
					self.__main_region__at__work_working__at__shift_shift__unloading_main__at_stock_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck:
					self.__main_region__at__work_working__at__shift_shift__unloading_main__at_truck_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_stock_carrying:
					self.__main_region__at__work_working__at__shift_shift__unloading_main__at_stock_carrying_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_unloading_main_at_truck_carrying:
					self.__main_region__at__work_working__at__shift_shift__unloading_main__at_truck_carrying_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_assembly_r1_at_stock:
					self.__main_region__at__work_working__at__shift_shift__assembly_r1__at_stock_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck:
					self.__main_region__at__work_working__at__shift_shift__loading_r1__at_truck_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock:
					self.__main_region__at__work_working__at__shift_shift__loading_r1__at_stock_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_truck_carrying:
					self.__main_region__at__work_working__at__shift_shift__loading_r1__at_truck_carrying_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_shift_loading_r1_at_stock_carrying:
					self.__main_region__at__work_working__at__shift_shift__loading_r1__at_stock_carrying_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_energy_tiring:
					self.__main_region__at__work_working__at__shift_energy__tiring_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_energy_tired:
					self.__main_region__at__work_working__at__shift_energy__tired_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_button_button_released:
					self.__main_region__at__work_working__at__shift_button_button_released_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_at__shift_button_button_pressed:
					self.__main_region__at__work_working__at__shift_button_button_pressed_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_grace__period_r1_alternative__chosen:
					self.__main_region__at__work_working__grace__period_r1__alternative__chosen_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_grace__period_r1_leave__day:
					self.__main_region__at__work_working__grace__period_r1__leave__day_react(True)
				elif self.__state_vector[self.__next_state_index] == self.State.main_region_at__work_working_toilet__break:
					self.__main_region__at__work_working__toilet__break_react(True)
				self.__next_state_index += 1
			self.__clear_in_events()
			next_event = self.__get_next_event()
			if next_event is not None:
				self.__execute_queued_event(next_event)
			condition_0 = self.employee.go_to_work or self.employee.go_home or self.employee.shift_clicked or self.ui.action_pressed or self.ui.action_released or self.__time_events[0] or self.__time_events[1] or self.__time_events[2] or self.__time_events[3]
		self.__is_executing = False
	
	
	
	
