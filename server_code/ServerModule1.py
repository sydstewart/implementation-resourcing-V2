import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import pulp
from pulp import *


#==========================================================================
#Do LP calculations
#=========================================================================

@anvil.server.callable
def calculate_projects(Scenario):

  model= LpProblem('No of Projects', LpMaximize)
  
  # Construct decision variables
  A = LpVariable('Systems', lowBound=0 , cat=LpInteger)
  B = LpVariable('Standalone Interfaces', lowBound=0 , cat=LpInteger)
  C = LpVariable('Server Moves', lowBound=0 , cat=LpInteger)
  D = LpVariable('Upgrades', lowBound=0 , cat=LpInteger)
  
  
  #Objective Function
  #get data
  projects_row = app_tables.projects.get(projects='Systems',Scenario=Scenario)
  # for row in systems_selling_+price:
  print(projects_row['Selling_price'])
  Systems_Selling_Price = projects_row['Selling_price']
  Systems_Demand = projects_row['Demand']

  projects_row = app_tables.projects.get(projects='Standalone Interfaces',Scenario=Scenario)
  # for row in projects_row:
  print(projects_row['Selling_price'])
  Standalone_Interfaces_Selling_Price = projects_row['Selling_price']
  Standalone_Interfaces_Demand = projects_row['Demand']
  
  projects_row = app_tables.projects.get(projects='Server Moves',Scenario=Scenario)
  # for row in projects_row:
  print(projects_row['Selling_price'])
  Server_Moves_Selling_Price = projects_row['Selling_price']
  Server_Moves_Demand = projects_row['Demand']
  
  projects_row = app_tables.projects.get(projects='Upgrades',Scenario=Scenario)
  # for row in projects_row:
  print(projects_row['Selling_price'])
  Upgrades_Selling_Price = projects_row['Selling_price']
  Upgrades_Demand = projects_row['Demand']

  # A = 1
  # B = 1
  # C= 1
  # D = 1
  model += Systems_Selling_Price*A + Standalone_Interfaces_Selling_Price*B + Server_Moves_Selling_Price*C + Upgrades_Selling_Price*D  #'Objective Function'
  # print('Problem', m)

#Constraints
  print('Days Effort per  project')
  print('Systems days')
  system_days = app_tables.days_effort.get(projects='Systems',Scenario=Scenario)
  print(system_days['PreReqs'],system_days['Interfacing'],system_days['System_config'],system_days['Installing'])
  print('Standalone Interface days')
  interface_days = app_tables.days_effort.get(projects='Standalone Interfaces',Scenario=Scenario)
  print(interface_days['PreReqs'],interface_days['Interfacing'],interface_days['System_config'],interface_days['Installing'])
  print ('Server Move days')
  server_move_days = app_tables.days_effort.get(projects='Server Moves',Scenario=Scenario)
  print(server_move_days['PreReqs'], server_move_days['Interfacing'], server_move_days['System_config'],server_move_days['Installing'])
  print('Upgrade  days')
  upgrade_days = app_tables.days_effort.get(projects='Upgrades',Scenario=Scenario)
  print(upgrade_days['PreReqs'], upgrade_days['Interfacing'], upgrade_days['System_config'],upgrade_days['Installing'])
  print('+++++++++++++++++')
  print('')
  
  print('CONSTRAINTS')
  print('+++++++++++++++++')
  pr_constraint_days = app_tables.constraints.get(Resource='PreReqs',Scenario=Scenario)
  print('Pre Req Constraint Days pa =', pr_constraint_days['Constraint'])
  int_constraint_days = app_tables.constraints.get(Resource='Interfacing',Scenario=Scenario)
  print('Interfacing Constraint Days pa =',int_constraint_days['Constraint'])
  sys_constraint_days = app_tables.constraints.get(Resource='Systems_config',Scenario=Scenario)
  print('System Config Constraint Days pa =',sys_constraint_days['Constraint'])
  install_constraint_days = app_tables.constraints.get(Resource='Installing',Scenario=Scenario)
  print('Installing Constraint Days pa =',install_constraint_days['Constraint'])
  print('+++++++++++++++++')
  print('')
# Create constraints

  model += system_days['PreReqs'] * A + interface_days['PreReqs']* B + server_move_days['PreReqs'] * C + upgrade_days['PreReqs'] * D <= pr_constraint_days['Constraint']  # "PreReqs"
  model += system_days['Interfacing'] * A + interface_days['Interfacing']* B + server_move_days['Interfacing'] * C + upgrade_days['Interfacing'] * D <= int_constraint_days['Constraint'] # "Interfacing"
  model += system_days['System_config'] * A + interface_days['System_config']* B + server_move_days['System_config'] * C + upgrade_days['System_config'] * D <= sys_constraint_days['Constraint'] # "Systems_config"
  model += system_days['Installing'] * A + interface_days['Installing']* B + server_move_days['Installing'] * C + upgrade_days['Installing'] * D <= install_constraint_days['Constraint'] # "Installing"
  #Demand
  model += D <= Upgrades_Demand, 'Upgrades'
  model += C <= Server_Moves_Demand, 'Server Moves'
  model += B <= Standalone_Interfaces_Demand, 'Standalone Interfaces'
  model += A <= Systems_Demand, 'Systems'
  
  print('')
  print('DEMAND')
  print('+++++++++++++++++')
  print('Systems Demand = ',Systems_Demand)
  print('Standalone_Interfaces_Demand = ',Standalone_Interfaces_Demand)
  print('Server_Moves_Demand = ',Server_Moves_Demand )
  print('Upgrades_Demand= ',Upgrades_Demand )
# The problem is solved using PuLP's choice of Solver
  model.solve()
  print('')

# Each of the variables is printed with it's resolved optimum value
  print('PROJECTS PROJECTED')
  print('+++++++++++++++++')
  for v in model.variables():
      print(v.name, "=", v.varValue)
  
  total_sales = value(model.objective)
  print("Total Sales: ", value(model.objective))
  obj_row = app_tables.objective.get()  
  obj_row['objective'] = total_sales
  
  no_of_systems= model.variablesDict()['Systems'].value()
  print('No of systems = ',no_of_systems)
  no_of_standalone_interfaces= model.variablesDict()['Standalone_Interfaces'].value()
  print('No_of_standalone_interfaces = ', no_of_standalone_interfaces)
  no_of_server_moves= model.variablesDict()['Server_Moves'].value()
  # print(model.variablesDict()['Server_Moves'].value())
  print('No_of_server_moves = ',no_of_server_moves)
  no_of_upgrades= model.variablesDict()['Upgrades'].value()
  print('No_of_upgrades = ',no_of_upgrades)
  print('')
  
# Update projects table with Projected projects
  projects_row = app_tables.projects.get(Scenario = Scenario, projects='Systems')
  projects_row['Projected'] = no_of_systems
  projects_row = app_tables.projects.get(Scenario = Scenario, projects='Standalone Interfaces')
  projects_row['Projected'] = no_of_standalone_interfaces
  projects_row = app_tables.projects.get(Scenario = Scenario, projects='Server Moves')
  projects_row['Projected'] = no_of_server_moves
  projects_row = app_tables.projects.get(Scenario = Scenario, projects='Upgrades')
  projects_row['Projected'] = no_of_upgrades
 
  
  print('DAYS USED')
  print('++++++++++++++++++++++++')
  total_pre_days_used = (system_days['PreReqs'] * no_of_systems + interface_days['PreReqs']* no_of_standalone_interfaces + server_move_days['PreReqs'] * no_of_server_moves +  \
    upgrade_days['PreReqs'] * no_of_upgrades )
  print('No of Pre Req days used',total_pre_days_used )
  
  total_interfacing_days_used = system_days['Interfacing'] * no_of_systems + interface_days['Interfacing']* no_of_standalone_interfaces + server_move_days['Interfacing'] * \
   no_of_server_moves + upgrade_days['Interfacing'] * no_of_upgrades
  print('No of Interfacing days used',total_interfacing_days_used )
  
  total_system_config_days_used = system_days['System_config'] * no_of_systems + interface_days['System_config']* no_of_standalone_interfaces+ server_move_days['System_config'] * no_of_server_moves + \
  upgrade_days['System_config'] *no_of_upgrades 
  print('No of System_Config_days used',total_system_config_days_used )
  
  
  total_installing_days_used = system_days['Installing'] * no_of_systems + interface_days['Installing']* no_of_standalone_interfaces + server_move_days['Installing'] * no_of_server_moves + \
    upgrade_days['Installing'] * no_of_upgrades
  print('No of Installing_days used',total_installing_days_used )
  # print( model.variablesDict()['Standalone_Interfaces'].value())
  # return value(model.objective),

# Update Constraints table with used
  Constraints_row = app_tables.constraints.get(Scenario = Scenario, Resource='PreReqs')
  Constraints_row['Used'] = total_pre_days_used
  Constraints_row = app_tables.constraints.get(Scenario = Scenario, Resource='Interfacing')
  Constraints_row['Used'] = total_interfacing_days_used
  Constraints_row = app_tables.constraints.get(Scenario = Scenario, Resource='Systems_config')
  Constraints_row['Used'] = total_system_config_days_used
  Constraints_row = app_tables.constraints.get(Scenario = Scenario, Resource='Installing')
  Constraints_row['Used'] = total_installing_days_used 