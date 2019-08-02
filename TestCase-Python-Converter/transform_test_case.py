class GenerateTestCase(object):
    def __init__(self, test_file):
        self.test_file = test_file
        self.current_test_case = None # Keeps track of our current test case number
        self.res = {} # stores mapping of test case number to each test case. Furthermore divides them into parameters: info pairing

        self.num_of_parameters = 0 # Number of parameters that will be in the result variable
        self.current_parameter_num = None # The current parameter we're on
        self.list_test_case = None # Determines if the info inside one parameter should belong in a list if > 1 info
        self.until_next_parameter = 0 # The count until we know to go to the next parameter in our dictionary
        
        self.parameters = [] #Containing all of our parameters 

    def generate_test_case(self):
        tc_file = open(self.test_file, "r")
        content = tc_file.readlines()
        for idx, line in enumerate(content):
            x = line.strip()
            if x == "":
                #Move on to the next tese case and reset global variables
                self.current_test_case = 0 if self.current_test_case == None else self.current_test_case + 1
                self.current_parameter_num = None
                self.list_test_case = None
                self.until_next_parameter = 0
                continue
            
            # Setting up res dictionary
            if idx == 0:
                test_case_amount = int(x)
                for i in range(test_case_amount):
                    self.res[i] = {}
                continue
            
            # Setting up number of parameters
            elif idx == 1:
                self.num_of_parameters = int(x)
                continue

            # Appending parameters to list
            elif idx > 1 and idx < 2 + self.num_of_parameters:
                self.parameters.append(x)
                continue

            elif x != "":
                # Setting up variables to determine how big the parameter field's list should be or if the value is just a single string
                if not self.until_next_parameter:
                    self.until_next_parameter = int(x)
                    self.current_parameter_num = 0 if self.current_parameter_num == None else self.current_parameter_num + 1
                    self.list_test_case = False
                    continue
                else:
                    current_param = self.parameters[self.current_parameter_num]
                    if self.until_next_parameter == 1 and not self.list_test_case: #For parameters that have only one field
                        # For values that are meant to be booleans, set them to be the correct type
                        if x == "False":
                            self.res[self.current_test_case][current_param] = False
                        elif x == "True":
                            self.res[self.current_test_case][current_param] = True
                        else:
                            self.res[self.current_test_case][current_param] = x
                    else:
                        self.res[self.current_test_case].setdefault(current_param, []).append(x) #For parameters with multiple fields 
                        self.list_test_case = True 

                    self.until_next_parameter -= 1

        return self.res

if __name__ == "__main__":
    generateTestCase = GenerateTestCase("test.txt")
    print(generateTestCase.generate_test_case())


