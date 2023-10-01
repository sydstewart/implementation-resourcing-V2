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
@anvil.server.callable
def ingredients():
      # Instantiate our problem class
      
      model = pulp.LpProblem("Cost_minimising_blending_problem", pulp.LpMinimize)
  
# Construct our decision variable lists
      sausage_types = ['economy', 'premium']
      ingredients = ['pork', 'wheat', 'starch']
  
      # Each of these decision variables will have similar characteristics
      # (lower bound of 0, continuous variables). Therefore we can use PuLP’s LpVariable object’s dict functionality, we can provide our tuple indices.
        # 6 decision variables
      ing_weight = pulp.LpVariable.dicts("weight kg",
                                          ((i, j) for i in sausage_types for j in ingredients),
                                          lowBound=0,
                                          cat='Continuous')
      
      # Objective Function
      model += (pulp.lpSum([
                    4.32 * ing_weight[(i, 'pork')]
                    + 2.46 * ing_weight[(i, 'wheat')]
                    + 1.86 * ing_weight[(i, 'starch')]
                    for i in sausage_types]))   
               
      # Constraints
      # 350 economy and 500 premium sausages at 0.05 kg i.e. 50g
      model += pulp.lpSum([ing_weight['economy', j] for j in ingredients]) == 350 * 0.05
      model += pulp.lpSum([ing_weight['premium', j] for j in ingredients]) == 500 * 0.05
      
      # Economy has >= 40% pork, premium >= 60% pork
      model += ing_weight['economy', 'pork'] >= (
          0.4 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))
      model += ing_weight['premium', 'pork'] >= (
          0.6 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))
      
      # Sausages must be <= 25% starch
      model += ing_weight['economy', 'starch'] <= (
          0.25 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))
      model += ing_weight['premium', 'starch'] <= (
          0.25 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))
      
      # We have at most 30 kg of pork, 20 kg of wheat and 17 kg of starch available
      model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) <= 30
      model += pulp.lpSum([ing_weight[i, 'wheat'] for i in sausage_types]) <= 20
      model += pulp.lpSum([ing_weight[i, 'starch'] for i in sausage_types]) <= 17
      
      # We have at least 23 kg of pork to use up
      model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) >= 23
            
      # Solve our problem
      model.solve()
      pulp.LpStatus[model.status]

  # print decision variables
      decisions= {}
      ingred = ''
      ingredsum =''
      for var in ing_weight:
          var_value = ing_weight[var].varValue
          print ("The weight of {0} in {1} sausages is {2} kg".format(var[1], var[0], var_value))
          print(ing_weight[var], ing_weight[var].varValue)
          # decisions.append(ing_weight[var].varValue)
          decisions.update({ing_weight[var]:ing_weight[var].varValue})
          ingred = (("The weight of {0} in {1} sausages is {2} kg".format(var[1], var[0], var_value)) +'\n')
          ingredsum = ingredsum + ingred
      print(' as built',decisions)
      # ingred = (("The weight of {0} in {1} sausages is {2} kg".format(var[1], var[0], var_value)))
      # ingredsum = ingredsum + ingred
      total_cost = pulp.value(model.objective)
 
    
      print ("The total cost is €{} for 350 economy sausages and 500 premium sausages".format(round(total_cost, 2)))
      answer = ("The total cost is €{} for 350 economy sausages and 500 premium sausages".format(round(total_cost, 2)))
      # Printing keys and values separately
      # print("Keys:", list(ing_weight.keys()))
      # print("Values:", list(ing_weight.values()))
      # Printing a dictionary using a loop and the items() method
      return ingredsum, answer
      # for key, value in ing_weight.items():
      #     print(key, ":", value)
      # print (decisions)
      # df = pd.DataFrame(decisions)
      # print(df)
      # # decisions= df.to_dict(orient='records')
      # print (decisions)
      # return ingred, decisions

@anvil.server.callable
def spreadsheet():
    import openpyxl
    from openpyxl import Workbook
    
    filename = "hello_world.xlsx"
    
    workbook = Workbook()
    sheet = workbook.active
    
    sheet["A1"] = "hello"
    sheet["B1"] = "world!"
    
    workbook.save(filename=filename)


@anvil.server.callable
def resources():

  resources = ['PreReqs','Interfacing','System Config', 'Installing']  # j
  project_type = ['Systems','Standalone Interfaces','Server Moves', 'Upgrades']   #i
    
# Each of these decision variables will have similar characteristics
# (lower bound of 0, continuous variables). Therefore we can use PuLP’s LpVariable object’s dict functionality, we can provide our tuple indices.
# 6 decision variables
  project_resource = pulp.LpVariable.dicts("days_work",
                                          ((i, j) for i in project_types for j in resources),
                                          lowBound=0,
                                          cat='Continuous')

# Objective Function
  model += (pulp.lpSum([
                   project_resource[(i, 'PreReqs')]
                    + project_resource[(i, 'Interfacing')]
                    + project_resource[(i, 'System Config')]
                    + project_resource[(i, 'Installing')]
                    for i in project_types]))   

   # Constraints
      # 350 economy and 500 premium sausages at 0.05 kg i.e. 50g
  Model += pulp.lpSum([ing_weight['economy', j] for j in ingredients]) == 350 * 0.05
  model += pulp.lpSum([ing_weight['premium', j] for j in ingredients]) == 500 * 0.05
      
      # Economy has >= 40% pork, premium >= 60% pork
  model += ing_weight['economy', 'pork'] >= (
      0.4 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))
  model += ing_weight['premium', 'pork'] >= (
      0.6 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))
  
  # Sausages must be <= 25% starch
  model += ing_weight['economy', 'starch'] <= (
      0.25 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))
  model += ing_weight['premium', 'starch'] <= (
      0.25 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))
  
  # We have at most 30 kg of pork, 20 kg of wheat and 17 kg of starch available
  model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) <= 30
  model += pulp.lpSum([ing_weight[i, 'wheat'] for i in sausage_types]) <= 20
  model += pulp.lpSum([ing_weight[i, 'starch'] for i in sausage_types]) <= 17
  
  # We have at least 23 kg of pork to use up
  model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) >= 23
        
  # Solve our problem
  model.solve()
  pulp.LpStatus[model.status]

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
  systems_selling_price = app_tables.selling_prices.get(projects='Systems',Scenario=Scenario)
  # for row in systems_selling_+price:
  print(systems_selling_price['Selling_price'])
  Systems_Selling_Price = systems_selling_price['Selling_price']

  systems_selling_price = app_tables.selling_prices.get(projects='Standalone Interfaces',Scenario=Scenario)
  # for row in systems_selling_price:
  print(systems_selling_price['Selling_price'])
  Standalone_Interfaces_Selling_Price = systems_selling_price['Selling_price']
  
  systems_selling_price = app_tables.selling_prices.get(projects='Server Moves',Scenario=Scenario)
  # for row in systems_selling_price:
  print(systems_selling_price['Selling_price'])
  Server_Moves_Selling_Price = systems_selling_price['Selling_price']
  
  systems_selling_price = app_tables.selling_prices.get(projects='Upgrades',Scenario=Scenario)
  # for row in systems_selling_price:
  print(systems_selling_price['Selling_price'])
  Upgrades_Selling_Price = systems_selling_price['Selling_price']

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

  pr_constraint_days = app_tables.constraints.get(Resource='PreReqs',Scenario=Scenario)
  print('Pre Req Constraint Days pa =', pr_constraint_days['Constraint'])
  int_constraint_days = app_tables.constraints.get(Resource='Interfacing',Scenario=Scenario)
  print('Interfacing Constraint Days pa =',int_constraint_days['Constraint'])
  sys_constraint_days = app_tables.constraints.get(Resource='Systems_config',Scenario=Scenario)
  print('System Config Constraint Days pa =',sys_constraint_days['Constraint'])
  install_constraint_days = app_tables.constraints.get(Resource='Installing',Scenario=Scenario)
  print('Installing Constraint Days pa =',install_constraint_days['Constraint'])

# Create constraints

  model += system_days['PreReqs'] * A + interface_days['PreReqs']* B + server_move_days['PreReqs'] * C + upgrade_days['PreReqs'] * D <= pr_constraint_days['Constraint']  # "PreReqs"
  model += system_days['Interfacing'] * A + interface_days['Interfacing']* B + server_move_days['Interfacing'] * C + upgrade_days['Interfacing'] * D <= int_constraint_days['Constraint'] # "Interfacing"
  model += system_days['System_config'] * A + interface_days['System_config']* B + server_move_days['System_config'] * C + upgrade_days['System_config'] * D <= sys_constraint_days['Constraint'] # "Systems_config"
  model += system_days['Installing'] * A + interface_days['Installing']* B + server_move_days['Installing'] * C + upgrade_days['Installing'] * D <= install_constraint_days['Constraint'] # "Installing"
  D <= 15
  
# The problem is solved using PuLP's choice of Solver
  model.solve()
  

# Each of the variables is printed with it's resolved optimum value
  for v in model.variables():
      print(v.name, "=", v.varValue)
  print("Total Sales: ", value(model.objective))
  no_of_systems= model.variablesDict()['Systems'].value()
  print('No of systems = ',no_of_systems)
  no_of_standalone_interfaces= model.variablesDict()['Standalone_Interfaces'].value()
  print('No_of_standalone_interfaces = ', no_of_standalone_interfaces)
  no_of_server_moves= model.variablesDict()['Server_Moves'].value()
  print('No_of_server_moves = ',no_of_server_moves)
  no_of_upgrades= model.variablesDict()['Upgrades'].value()
  print('No_of_upgrades = ',no_of_upgrades)
  
  total_pre_days_used = (system_days['PreReqs'] * no_of_systems + interface_days['PreReqs']* no_of_standalone_interfaces + server_move_days['PreReqs'] * no_of_server_moves +  \
    upgrade_days['PreReqs'] * no_of_upgrades )
  print('No of Pre Req days used',total_pre_days_used )
  
  total_interfacing_days_used = system_days['Interfacing'] * no_of_systems + interface_days['Interfacing']* no_of_standalone_interfaces + server_move_days['Interfacing'] * \
   no_of_server_moves + upgrade_days['Interfacing'] * no_of_upgrades
  print('No of Interfacing days used',total_interfacing_days_used )
  
  total_system_config_days_used = system_days['System_config'] * no_of_systems + interface_days['System_config']* no_of_standalone_interfaces+ server_move_days['System_config'] * n+ upgrade_days['System_config'] * D 
  print('No of System_Config_days used',total_system_config_days_used )
  
  
  total_installing_days_used = system_days['Installing'] * no_of_systems + interface_days['Installing']* no_of_standalone_interfaces + server_move_days['Installing'] * no_of_server_moves + \
    upgrade_days['Installing'] * no_of_upgrades
  print('No of Installing_days used',total_installing_days_used )
  
  # return value(model.objective),