from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..Module1 import update_form
from ..Module2  import update_form

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('start')
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
    data = app_tables.days_effort.search(Scenario=Scen_row)
    for row in data:
      print(row['projects'],row['PreReqs'],row['Interfacing'],row['System_config'],row['Installing'])
      if row['projects'] == 'Systems':
        self.Sys_PR.text = row['PreReqs']
        self.Sys_Int.text = row['Interfacing']
        self.Sys_Sys.text = row['System_config']
        self.Sys_Ins.text = row['Installing']

      if row['projects'] == 'Standalone Interfaces':
        self.SI_PR.text = row['PreReqs']
        self.SI_Int.text = row['Interfacing']
        self.SI_Sys.text = row['System_config']
        self.SI_Ins.text = row['Installing']
        
      if row['projects'] == 'Server Moves':
        self.SM_PR.text = row['PreReqs']
        self.SM_Int.text = row['Interfacing']
        self.SM_Sys.text = row['System_config']
        self.SM_Ins.text = row['Installing']
        
      if row['projects'] == 'Upgrades':
        self.UP_PR.text = row['PreReqs']
        self.UP_Int.text = row['Interfacing']
        self.UP_Sys.text = row['System_config']
        self.UP_Ins.text = row['Installing']
    pass
    
    # load constraints
    #++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.constraints.search(Scenario=Scen_row)
    for row in data:
        if row['Resource'] == 'PreReqs':
            self.CON_PR.text =row['Constraint'] 
            self.PR_USED.text = row['Used'] 
        if row['Resource'] == 'Interfacing':
            self.CON_INT.text  = row['Constraint']
            self.INT_USED.text = row['Used'] 
        if row['Resource'] == 'Systems_config':
            self.CON_SYS.text = row['Constraint'] 
            self.SYS_USED.text = row['Used'] 
        if row['Resource'] == 'Installing': 
            self.CON_INS.text = row['Constraint'] 
            self.INS_USED.text = row['Used'] 
  
    # Load projects info
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.projects.search(Scenario=Scen_row)
    for row in data:
        if row['projects'] == 'Systems':
            self.SELL_SYS.text =row['Selling_price'] 
            self.DM_SYS.text = row['Demand']
            self.SYS_PRJ.text = row['Projected']
        if row['projects'] == 'Standalone Interfaces':
            self.SELL_INT.text  = row['Selling_price']
            self.DM_INT.text = row['Demand']
            self.INT_PRJ.text = row['Projected']
        if row['projects'] == 'Server Moves':
            self.SELL_SM.text = row['Selling_price'] 
            self.DM_SM.text = row['Demand']
            self.SM_PRJ.text = row['Projected']
        if row['projects'] == 'Upgrades': 
            self.SELL_UPG.text = row['Selling_price'] 
            self.DM_UP.text = row['Demand']
            self.UPG_PRJ.text = row['Projected']
 # Load Objective
    obj_row =  app_tables.objective.get()
    obj_num =  obj_row['objective']
    self.Objective.text = '£' + str('{:,}'.format(obj_num))
    # self.Objective.text ='£' + str( self.Objective.text)
    # self.Objective.text = {:,.2f}".format(self.Objective.text ))
    # "$" + str(round(float(dollar_value),2)) ${:,.2f}".format(total_amount))
  def create_scenario_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Sys_PR = self.Sys_PR.text
    Sys_Int = self.Sys_Int.text
    Sys_Sys = self.Sys_Sys.text
    Sys_Ins= self.Sys_Ins.text
    
    print(str(Sys_PR) + ' ' + str(Sys_Int) + ' ' + str(Sys_Sys) + ' ' + str(Sys_Ins))
    
    SI_PR = self.SI_PR.text
    SI_Int = self.SI_Int.text
    SI_Sys = self.SI_Sys.text
    SI_Ins= self.SI_Ins.text

    SM_PR = self.SM_PR.text
    SM_Int = self.SM_Int.text
    SM_Sys = self.SM_Sys.text
    SM_Ins= self.SM_Ins.text
    
    UP_PR = self.UP_PR.text
    UP_Int = self.UP_Int.text
    UP_Sys = self.UP_Sys.text
    UP_Ins= self.UP_Ins.text
    
    DM_SYS = self.DM_SYS.text
    DM_INT = self.DM_INT.text
    DM_SM = self.DM_SM.text
    DM_UP = self.DM_UP.text


    
    app_tables.days_effort.add_row(projects= "Systems",
                          PreReqs = Sys_PR,
                          Interfacing = Sys_Int,
                          System_config= Sys_Sys,
                          Installing = Sys_Ins)
                       
    app_tables.days_effort.add_row(projects= "Standalone Interfaces",
                          PreReqs = SI_PR,
                          Interfacing = SI_Int,
                          System_config= SI_Sys,
                          Installing = SI_Ins)

    app_tables.days_effort.add_row(projects= "Server Moves",
                          PreReqs = SM_PR,
                          Interfacing = SM_Int,
                          System_config= SM_Sys,
                          Installing = SM_Ins)
    app_tables.days_effort.add_row(projects= "Upgrades",
                          PreReqs = UP_PR,
                          Interfacing = UP_Int,
                          System_config= UP_Sys,
                          Installing = UP_Ins)


  
  
#==============================================================
  # Update Tables from Form
#==========================================================

   
  def update_scenario_button_click(self, **event_args):
      # """This method is called when the button is clicked"""
    # if self.scenario_dropdown.selected_value != None:
    
          Scen_row = app_tables.scenario.get(ScenarioID = 1)
          days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Systems')
          days_effort_row['PreReqs'] = self.Sys_PR.text
          days_effort_row['Interfacing'] = self.Sys_Int.text 
          days_effort_row['System_config'] = self.Sys_Sys.text   
          days_effort_row['Installing'] = self.Sys_Ins.text
          
          days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Standalone Interfaces')
          days_effort_row['PreReqs'] = self.SI_PR.text
          days_effort_row['Interfacing'] = self.SI_Int.text 
          days_effort_row['System_config'] = self.SI_Sys.text   
          days_effort_row['Installing'] = self.SI_Ins.text   
      
          constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='PreReqs')
          constraint_row['Constraint'] = self.CON_PR.text
          constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Interfacing')
          constraint_row['Constraint'] = self.CON_INT.text
          constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Systems_config')
          constraint_row['Constraint'] = self.CON_SYS.text
          constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Installing')
          constraint_row['Constraint'] = self.CON_INS.text
      
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Systems')
          projects_row['Selling_price'] = self.SELL_SYS.text
          projects_row['Demand'] = self.DM_SYS.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Standalone Interfaces')
          projects_row['Selling_price'] = self.SELL_INT.text
          projects_row['Demand'] = self.DM_INT.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Server Moves')
          projects_row['Selling_price'] = self.SELL_SM.text
          projects_row['Demand'] = self.DM_SM.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Upgrades')
          projects_row['Selling_price'] = self.SELL_UPG.text
          projects_row['Demand'] = self.DM_UP.text
          pass
    # else:
    #         clear_form(self)
      
  def calculate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
     
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Systems')
    days_effort_row['PreReqs'] = self.Sys_PR.text
    days_effort_row['Interfacing'] = self.Sys_Int.text 
    days_effort_row['System_config'] = self.Sys_Sys.text   
    days_effort_row['Installing'] = self.Sys_Ins.text
    
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Standalone Interfaces')
    days_effort_row['PreReqs'] = self.SI_PR.text
    days_effort_row['Interfacing'] = self.SI_Int.text 
    days_effort_row['System_config'] = self.SI_Sys.text   
    days_effort_row['Installing'] = self.SI_Ins.text  
    
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Server Moves')
    days_effort_row['PreReqs'] = self.SM_PR.text
    days_effort_row['Interfacing'] = self.SM_Int.text 
    days_effort_row['System_config'] = self.SM_Sys.text   
    days_effort_row['Installing'] = self.SM_Ins.text
    
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Upgrades')
    days_effort_row['PreReqs'] = self.UP_PR.text
    days_effort_row['Interfacing'] = self.UP_Int.text 
    days_effort_row['System_config'] = self.UP_Sys.text   
    days_effort_row['Installing'] = self.UP_Ins.text   
    

    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='PreReqs')
    constraint_row['Constraint'] = self.CON_PR.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Interfacing')
    constraint_row['Constraint'] = self.CON_INT.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Systems_config')
    constraint_row['Constraint'] = self.CON_SYS.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Installing')
    constraint_row['Constraint'] = self.CON_INS.text

    projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Systems')
    projects_row['Selling_price'] = self.SELL_SYS.text
    projects_row['Demand'] = self.DM_SYS.text
    projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Standalone Interfaces')
    projects_row['Selling_price'] = self.SELL_INT.text
    projects_row['Demand'] = self.DM_INT.text
    projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Server Moves')
    projects_row['Selling_price'] = self.SELL_SM.text
    projects_row['Demand'] = self.DM_SM.text
    projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Upgrades')
    projects_row['Selling_price'] = self.SELL_UPG.text
    projects_row['Demand'] = self.DM_UP.text

    anvil.server.call('calculate_projects', Scen_row)
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
    data = app_tables.days_effort.search(Scenario=Scen_row)
    for row in data:
      print(row['projects'],row['PreReqs'],row['Interfacing'],row['System_config'],row['Installing'])
      if row['projects'] == 'Systems':
        self.Sys_PR.text = row['PreReqs']
        self.Sys_Int.text = row['Interfacing']
        self.Sys_Sys.text = row['System_config']
        self.Sys_Ins.text = row['Installing']

      if row['projects'] == 'Standalone Interfaces':
        self.SI_PR.text = row['PreReqs']
        self.SI_Int.text = row['Interfacing']
        self.SI_Sys.text = row['System_config']
        self.SI_Ins.text = row['Installing']
        
      if row['projects'] == 'Server Moves':
        self.SM_PR.text = row['PreReqs']
        self.SM_Int.text = row['Interfacing']
        self.SM_Sys.text = row['System_config']
        self.SM_Ins.text = row['Installing']
        
      if row['projects'] == 'Upgrades':
        self.UP_PR.text = row['PreReqs']
        self.UP_Int.text = row['Interfacing']
        self.UP_Sys.text = row['System_config']
        self.UP_Ins.text = row['Installing']
    pass
    
    # load constraints
    #++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.constraints.search(Scenario=Scen_row)
    for row in data:
        if row['Resource'] == 'PreReqs':
            self.CON_PR.text =row['Constraint'] 
            self.PR_USED.text = row['Used'] 
        if row['Resource'] == 'Interfacing':
            self.CON_INT.text  = row['Constraint']
            self.INT_USED.text = row['Used'] 
        if row['Resource'] == 'Systems_config':
            self.CON_SYS.text = row['Constraint'] 
            self.SYS_USED.text = row['Used'] 
        if row['Resource'] == 'Installing': 
            self.CON_INS.text = row['Constraint'] 
            self.INS_USED.text = row['Used'] 
  
    # Load projects info
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.projects.search(Scenario=Scen_row)
    for row in data:
        if row['projects'] == 'Systems':
            self.SELL_SYS.text =row['Selling_price'] 
            self.DM_SYS.text = row['Demand']
            self.SYS_PRJ.text = row['Projected']
        if row['projects'] == 'Standalone Interfaces':
            self.SELL_INT.text  = row['Selling_price']
            self.DM_INT.text = row['Demand']
            self.INT_PRJ.text = row['Projected']
        if row['projects'] == 'Server Moves':
            self.SELL_SM.text = row['Selling_price'] 
            self.DM_SM.text = row['Demand']
            self.SM_PRJ.text = row['Projected']
        if row['projects'] == 'Upgrades': 
            self.SELL_UPG.text = row['Selling_price'] 
            self.DM_UP.text = row['Demand']
            self.UPG_PRJ.text = row['Projected']

      # Set background if deficiency          
        if self.SYS_PRJ.text < self.DM_SYS.text:
              self.SYS_PRJ.background = '#faebeb'
        else: 
              self.SYS_PRJ.background = ''
          
        if self.INT_PRJ.text < self.DM_INT.text:
              self.INT_PRJ.background = '#faebeb'
        else: 
              self.INT_PRJ.background = ''
          
        if self.SM_PRJ.text < self.DM_SM.text:
              self.SM_PRJ.background = '#faebeb'
        else: 
              self.SM_PRJ.background = ''
          
        if self.UPG_PRJ.text < self.DM_UP.text:
              self.UPG_PRJ.background = '#faebeb'
        else: 
              self.UPG_PRJ.background = ''
       
        if self.PR_USED.text == self.CON_PR.text:
              self.PR_USED.background = '#faebeb'
        else: 
              self.PR_USED.background = ''
          
        if self.INT_USED.text == self.CON_INT.text:
              self.INT_USED.background = '#faebeb'
        else: 
              self.INT_USED.background = ''
          
        if self.SYS_USED.text == self.CON_SYS.text:
              self.SYS_USED.background = '#faebeb'
        else: 
              self.SYS_USED.background = ''
          
        if self.INS_USED.text >= 0.95 * self.CON_INS.text:
              self.INS_USED.background = '#faebeb'
        else: 
              self.INS_USED.background = ''
    pass
# Load Objective and format for currency
    obj_row =  app_tables.objective.get()
    obj_num =  obj_row['objective']
    self.Objective.text = '£' + str('{:,}'.format(obj_num))

 
     



  









 


